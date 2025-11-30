# Projeto de Treinamento e Rastreamento de Modelos com Docker, MinIO, MLflow e XGBoost

Este projeto implementa um pipeline completo de Machine Learning usando um ambiente totalmente containerizado. Ele inclui ingestão de dados no MinIO, desenvolvimento e execução de experimentos em Jupyter, treinamento com XGBoost, validação repetida e rastreamento dos experimentos e artefatos via MLflow.

O objetivo é simular um fluxo real de MLOps leve usando ferramentas open source e armazenamento S3 compatível.

# Pipeline do Projeto

A pipeline do projeto é composta por quatro etapas principais que funcionam de maneira integrada. Primeiro ocorre a ingestão automática dos dados, onde o serviço ingest coleta os dados do kaggle e envia os dados para o MinIO, que atua como armazenamento S3 local. Em seguida, o Jupyter Notebook é utilizado para análise, preparação dos dados, modelagem e visualização das métricas, incluindo gráficos de desempenho e validação. Durante esse processo, todos os experimentos, parâmetros, métricas e artefatos do modelo são registrados automaticamente no MLflow, permitindo rastreamento completo das execuções. Por fim, os resultados gerados no notebook, como gráficos, métricas e arquivos derivados, podem ser armazenados no MinIO, garantindo versionamento simples e mantendo todo o fluxo centralizado em uma arquitetura leve e fácil de operar.

# relatório do projeto
https://docs.google.com/document/d/1nbMCiJsXzl_S02qg9dC4VQPypDCBnrrvzLyPkpbEr_U/edit?usp=sharing

# Informações sobre a disciplina e o projeto
Membros:
  - Danilo Melo @dan-albuquerque
  - Sofia Valadares @sofiaValadares
  - Joao VIctor Ferraz @JoaovfGoncalves
  - Guilherme Silveira @guiga-sa
  - Maria Luiza Calife @Maria Luiza Calife 


Nome da disciplina: Aprendizado de Máquina - 2025.2.

Nome da instituição de ensino: CESAR School.

# Funcionalidades

* Ambiente totalmente containerizado usando Docker Compose
* MinIO como armazenamento S3 compatível
* MLflow Tracking com backend SQLite e artefatos no MinIO
* Jupyter Notebook com bibliotecas de ML pré-instaladas
* Script de ingestão que cria bucket e envia dataset automaticamente
* Treinamento com SMOTE, StratifiedKFold repetido e XGBoost
* Logging automático de métricas, artefatos e modelo final no MLflow


# Estrutura do Projeto

```text
.
├── docker-compose.yml
├── ingest.py # modulo de ingestão
│   └── ingest.py
│   └── dockerfile
├── notebooks/
│   └── projetoML_cesar (1).ipynb
├── minio_data/  #gerado aós docker compose
├── mlflow/  #gerado aós docker compose
└── README.md
```

# Pré requisitos

* Docker
* Docker Compose
* Portas livres:
  8888 (Jupyter)
  9000 e 9001 (MinIO)
  5000 (MLflow)

# Arquivo `.env` (exemplo recomendado)

Crie um arquivo `.env` na raiz do projeto:

```env
AWS_ACCESS_KEY=minio
AWS_SECRET_KEY=minio123
MINIO_URL=http://minio:9000

MLFLOW_S3_ENDPOINT_URL=http://minio:9000
MLFLOW_TRACKING_URI=http://mlflow:5000

BUCKET_DATA=data-bucket
BUCKET_MLFLOW=mlflow
```

# Passo a passo

## 1. Subir os containers

```bash
docker compose up -d
```

## 2. Criar os buckets no MinIO

Acesse:

[http://localhost:9001](http://localhost:9001)
Usuário: minio
Senha: minio123

Crie os buckets:

* data-bucket
* mlflow

## 3. Rodar ingestão de dados no MinIO

Caso o ingest não rode automaticamente ou retorne algum erro:

```bash
docker compose exec jupyter python ingest.py
```

O script:

* Cria o bucket `data-bucket` caso não exista
* Baixa o dataset do Kaggle
* Envia o CSV para o MinIO

 

# Acessando o Jupyter

Acesse:

[http://localhost:8888/lab?token=mlproject](http://localhost:8888/lab?token=mlproject)

Abra:

`notebooks/projetoML_cesar (1).ipynb`

Execute todas as células.
O MLflow já deve estar rodando no container para registrar os experimentos.

 

# Treinamento e Logging no MLflow

O notebook realiza:

* Limpeza e preparação do dataset
* Validação repetida com StratifiedKFold
* Treinamento do XGBoost com SMOTE
* Geração das métricas
* Logging no MLflow incluindo:

  * Hiperparâmetros
  * Métricas estatísticas
  * Gráficos de boxplot
  * Matriz de confusão
  * Modelo final serializado

Cada execução aparece como um run dentro do experimento `experimento_xgboost`.


# Visualizando Experimentos no MLflow

Acesse:

http://localhost:5000

Você poderá navegar por runs, métricas, parâmetros, gráficos e artefatos.

# Estrutura dos Experimentos

Cada run contém:

* Hiperparâmetros do XGBoost
* Métricas: accuracy, precision, recall, f1
* Intervalos de confiança
* Boxplots das métricas
* Matriz de confusão
* Modelo final salvo no MinIO

# Parar todos os serviços

```bash
docker compose down
```
# Observações sobre o projeto
- decidimos não utilizar Snowflake para tratamento e estruturação dos dados pois o dataset não possui caracteristicas que exigem muitos tratamentos, a estruturação que realizamos está no Jupyter notebook

Aqui vai um parágrafo claro e direto para colocar no README explicando a pipeline.
