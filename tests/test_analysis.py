from pathlib import Path
import pandas as pd
import pytest
from analysis import load_data, run_pipeline
FIXTURE=Path(__file__).parents[1]/"data"/"sample_co2.csv"
def test_load_data_calculates_per_capita():
    df=load_data(FIXTURE); brazil_2024=df[(df["country"]=="Brazil")&(df["year"]==2024)].iloc[0]
    assert round(brazil_2024["co2_per_capita"],2)==2.29
def test_pipeline_generates_expected_evidence(tmp_path):
    summary=run_pipeline(FIXTURE,tmp_path)
    assert summary["latest_year"]==2024; assert summary["brazil_co2_mt"]==483.0; assert summary["brazil_yoy_change_pct"]==3.65
    assert (tmp_path/"summary.json").exists(); assert (tmp_path/"latest_indicators.csv").exists(); assert (tmp_path/"co2_trend.svg").exists()
def test_missing_required_column_raises(tmp_path):
    invalid=tmp_path/"invalid.csv"; pd.DataFrame({"country":["Brazil"],"year":[2024]}).to_csv(invalid,index=False)
    with pytest.raises(ValueError,match="Missing required columns"): load_data(invalid)
