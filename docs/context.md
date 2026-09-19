# Contexto do projeto

## Objetivo

Pipelines ETL/ELT do zero no Databricks (PySpark), medalhão bronze/silver/gold, dbt para qualidade e governança.

## Tipo de projeto

[ ] Estudo  [ ] Portfólio  [ ] Produção

## Problema de negócio e consumidores

- Problema que resolve: [...]
- Quem consome o dado final: [Power BI / analistas / ciência de dados / apps...]

## Fontes de dados

| Fonte                                      | Tipo         | Volume                     | Frequência                         | Chave única                                   | CDC? |
| ------------------------------------------ | ------------ | -------------------------- | ----------------------------------- | ---------------------------------------------- | ---- |
| Kaggle: elemento/nyc-yellow-taxi-trip-data | Arquivos CSV | [verificar após download] | Carga única (histórico estático) | [verificar: provavelmente não há PK natural] | Não |

- URL: https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data
- Arquivo(s): [somente `yellow_tripdata_2016-03.csv` ou todos os arquivos do dataset?]
- Schema: a descobrir na Fase 1 (inspecionar o CSV; não assumir colunas)

## Decisões já tomadas

- Extração: baixar o dataset do Kaggle (API/CLI, com credencial fora do repositório)
- Formato local: converter o CSV para Parquet e salvar em `data/` na raiz do repositório
- `data/` no `.gitignore` (arquivos grandes não vão para o Git)

## Pontos em aberto para a Fase 2

- O Parquet em `data/` é apenas landing (cópia local do dado bruto) ou já é a origem que alimenta a bronze no Databricks? Como o arquivo sai da máquina local para o Databricks (upload para Volume do Unity Catalog, DBFS, storage cloud)?

## Ambiente

- Cloud: [AWS / Azure / GCP]
- Databricks: [Unity Catalog sim/não · SQL Warehouse ou cluster · edição]
- Storage: Delta Lake em [S3 / ADLS / GCS]
- Orquestração: [Databricks Workflows / outro / a definir]
- Versionamento e CI/CD: [GitHub / GitLab · a definir]
- Ambientes: [dev / staging / prod]
- Máquina local: [macOS / Windows / Linux] · Python [versão] · gerenciador de pacotes e ambiente: uv

## Qualidade e governança

- Regras de qualidade prioritárias: [...]
- Dados sensíveis / PII / LGPD: [sim/não · quais]
- Controle de acesso por camada: [...]

## Restrições

- Prazo: [...]
- Orçamento de compute: [...]
- Equipe: [...]
- SLA / latência: [...]

## Glossário

[termos de negócio e siglas]
