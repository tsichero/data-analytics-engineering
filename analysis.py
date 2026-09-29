"""Reproducible CO₂ analytics pipeline."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

DATA_URL="https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
REQUIRED_COLUMNS={"country","year","co2","population"}

def load_data(source: str|Path|None=None)->pd.DataFrame:
    df=pd.read_csv(source or DATA_URL)
    missing=REQUIRED_COLUMNS-set(df.columns)
    if missing: raise ValueError(f"Missing required columns: {sorted(missing)}")
    df=df.copy()
    for c in ["year","co2","population"]: df[c]=pd.to_numeric(df[c],errors="coerce")
    df=df.dropna(subset=["country","year","co2","population"])
    if (df["population"]<=0).any(): raise ValueError("Population must be greater than zero.")
    if (df["co2"]<0).any(): raise ValueError("CO₂ values must be non-negative for this analysis.")
    df["year"]=df["year"].astype(int)
    df["co2_per_capita"]=df["co2"]*1_000_000/df["population"]
    return df

def build_summary(subset:pd.DataFrame)->dict:
    brazil=subset[subset["country"]=="Brazil"].sort_values("year")
    latest_year=int(subset["year"].max())
    if brazil.empty: raise ValueError("Brazil is not available in the selected dataset.")
    start,end=brazil.iloc[0],brazil.iloc[-1]
    summary={"latest_year":latest_year,"brazil_co2_mt":round(float(end["co2"]),3),"brazil_co2_per_capita_t":round(float(end["co2_per_capita"]),3),"brazil_first_year":int(start["year"]),"brazil_first_co2_mt":round(float(start["co2"]),3),"brazil_last_year":int(end["year"]),"brazil_last_co2_mt":round(float(end["co2"]),3),"records_analyzed":int(len(subset))}
    if len(brazil)>1:
        previous=brazil.iloc[-2]
        summary["brazil_yoy_change_pct"]=round((float(end["co2"])/float(previous["co2"])-1)*100,2)
    return summary

def run_pipeline(source:str|Path|None,output_dir:str|Path="output")->dict:
    output=Path(output_dir); output.mkdir(parents=True,exist_ok=True)
    df=load_data(source); subset=df[df["country"].isin(["Brazil","World"])].copy()
    if subset.empty: raise ValueError("No Brazil/World records found.")
    latest=subset[subset["year"]==int(subset["year"].max())].copy()
    latest.to_csv(output/"latest_indicators.csv",index=False)
    summary=build_summary(subset)
    summary["source"]=str(source) if source else DATA_URL
    summary["source_type"]="local_fixture" if source else "public_dataset"
    with (output/"summary.json").open("w",encoding="utf-8") as f: json.dump(summary,f,ensure_ascii=False,indent=2)
    plt.figure(figsize=(10,5))
    for country in ["Brazil","World"]:
        part=subset[subset["country"]==country].sort_values("year")
        plt.plot(part["year"],part["co2"],label=country)
    plt.title("CO₂ emissions — Brazil vs World"); plt.xlabel("Year"); plt.ylabel("CO₂ emissions (million tonnes)"); plt.legend(); plt.tight_layout()
    plt.savefig(output/"co2_trend.png",dpi=160); plt.savefig(output/"co2_trend.svg"); plt.close()
    return summary

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--input"); parser.add_argument("--output-dir",default="output"); args=parser.parse_args()
    summary=run_pipeline(args.input,args.output_dir)
    print(f"Latest year: {summary['latest_year']}"); print(f"Brazil CO₂: {summary['brazil_co2_mt']:.2f} Mt"); print(f"Brazil CO₂ per capita: {summary['brazil_co2_per_capita_t']:.2f} t/person")

if __name__=="__main__": main()
