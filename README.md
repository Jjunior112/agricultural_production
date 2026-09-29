# Agricultural Production

Pipeline de dados e experimentos de machine learning sobre produção agrícola de  cana-de-açúcar, com camadas **bronze → silver → gold** e notebooks de análise e modelagem.

O alvo de modelagem é `producao_t` (produção em toneladas). Indicadores derivados (`tch`, `atr`, `art`) são removidos na camada gold para reduzir risco de *data leakage*.

## Requisitos

- Python **3.14**
- [uv](https://docs.astral.sh/uv/) para ambiente e dependências

Dependências principais: pandas, pyarrow, matplotlib, seaborn, scikit-learn.

## Estrutura

```
.
├── main.py                          # orquestra extração e transformações
├── sample/
│   └── agricultural_production_raw.csv   # CSV de entrada (não versionado)
├── data/                            # gerada pela pipeline (não versionada)
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── notebooks/
│   ├── analyses.ipynb               # exploração a partir do bronze
│   └── agriculture_ML.ipynb         # correlação e regressão no gold
└── src/agricultural_production/
    ├── bronze/extract_data.py
    ├── silver/transform_data.py
    └── gold/transform_data.py
```

## Dados de entrada

Coloque o CSV bruto em:

```
sample/agricultural_production_raw.csv
```

O arquivo usa **`;`** como delimitador. Colunas esperadas:

| Coluna | Descrição |
| --- | --- |
| `id_registro` | Identificador do registro |
| `ano` | Ano |
| `safra` | Safra (ex.: `2019/20`) |
| `cultura` | Cultura |
| `estado`, `municipio` | Localização |
| `area_plantada_ha`, `area_colhida_ha` | Área (ha) |
| `chuva_mm`, `temperatura_media_c`, `umidade_media_pct` | Clima |
| `ndvi_medio` | NDVI médio |
| `ph_solo`, `materia_organica_pct` | Solo |
| `fertilizante_kg_ha`, `irrigacao_mm` | Manejo |
| `tch`, `atr`, `art` | Indicadores de qualidade/produtividade (excluídos no gold) |
| `producao_t` | Produção (t) — variável alvo |

## Camadas

| Camada | Função | Saída |
| --- | --- | --- |
| **Bronze** | Lê o CSV e grava Parquet sem transformação de negócio | `data/bronze/agricultural_production.parquet` |
| **Silver** | Padroniza `estado` (maiúsculas), `municipio` (title case) e `cultura` (trim) | `data/silver/agricultural_production_silver.parquet` |
| **Gold** | Preenche nulos de `irrigacao_mm` e `fertilizante_kg_ha` com `0`; remove `tch`, `atr` e `art` | `data/gold/agricultural_production_gold.parquet` |

## Instalação

Na raiz do repositório:

```bash
uv sync
```

Isso cria o ambiente virtual e instala as dependências do `pyproject.toml`.

## Executar a pipeline

Com o CSV em `sample/agricultural_production_raw.csv`:

```bash
uv run python main.py
```

As etapas também podem ser executadas isoladamente:

```bash
uv run python -m agricultural_production.bronze.extract_data
uv run python -m agricultural_production.silver.transform_data
uv run python -m agricultural_production.gold.transform_data
```

## Notebooks

Ative o kernel do ambiente do projeto (após `uv sync`) e rode a partir de `notebooks/`, pois os caminhos usam `Path.cwd().parent`.

- **`analyses.ipynb`**: inspeção do dataset bronze.
- **`agriculture_ML.ipynb`**: mapa de correlação com `producao_t`; treino de regressão linear e *random forest* com split temporal (treino `2018–2023`, teste `2024–2025`) e imputação mediana nas features.

## Licença

Projeto pessoal de estudo; sem licença definida neste repositório.
