# Data Analytics Lab — CO₂ Emissions

> **Portfolio project · Data Analytics · Python · Reproducibility**

Projeto de análise de dados desenvolvido para demonstrar uma cadeia completa de Analytics: **fonte → validação → transformação → indicadores → visualização → evidência reproduzível**.

## Problema

Como transformar uma base pública de emissões em indicadores que possam ser auditados e reproduzidos por outra pessoa?

Neste projeto, o recorte compara **Brasil e mundo**, calcula emissão per capita e registra indicadores do último ano disponível.

## Fonte de dados

A fonte principal é o conjunto de dados de CO₂ disponibilizado pelo **Our World in Data**, baseado no Global Carbon Budget.

- [Our World in Data — CO₂ emissions](https://ourworldindata.org/co2-emissions)
- [Our World in Data — Brazil CO₂ profile](https://ourworldindata.org/profile/co2/brazil)

Para manter o CI determinístico, o projeto também usa uma pequena fixture local em `data/sample_co2.csv`. **Ela é apenas uma base de teste; não representa o dataset completo.**

## Pipeline

1. Carregamento da fonte pública ou fixture local.
2. Validação das colunas obrigatórias.
3. Conversão e validação dos tipos numéricos.
4. Tratamento de valores ausentes.
5. Validação de população positiva e CO₂ não negativo.
6. Filtragem de Brasil e mundo.
7. Cálculo de CO₂ per capita.
8. Geração de indicadores e visualização.
9. Exportação dos artefatos para auditoria.
10. Testes automatizados.

## Stack

- Python
- Pandas
- Matplotlib
- Pytest
- CSV / JSON
- GitHub Actions

## Como executar

```bash
pip install -r requirements.txt
python analysis.py
```

Para execução determinística/offline:

```bash
python analysis.py --input data/sample_co2.csv
```

Testes:

```bash
pytest -q
```

## Evidências

- [Resumo dos indicadores](output/summary.json)
- [Tabela do último ano](output/latest_indicators.csv)
- [Gráfico SVG](output/co2_trend.svg)
- [Descrição dos artefatos](output/README.md)
- [Testes](tests/test_analysis.py)

## Resultado da fixture

A execução local reproduzível com a fixture contém 2023–2024 e produz:

- Brasil, 2024: **483 Mt de CO₂**
- Brasil, 2024: **2,29 t de CO₂ por pessoa**
- Variação 2023→2024 na fixture: **+3,65%**

Esses números são evidência da **fixture de teste**.

## Decisões técnicas

O projeto aceita uma fonte externa, mas os testes usam uma fixture pequena e versionada. Assim, a lógica pode ser validada no CI sem depender de acesso à internet.

O dataset público completo não é duplicado no repositório; a fonte é documentada e a fixture permite validar a lógica de forma determinística.

## Competências demonstradas

**Data Analytics · Python · Pandas · Data Quality · Data Transformation · KPI Design · Data Visualization · Reproducibility · Testing · GitHub Actions · Technical Documentation**
