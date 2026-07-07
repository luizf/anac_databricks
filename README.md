# Azure Lakehouse Data Engineering Pipeline | Databricks, PySpark e Delta Lake

![Python](https://img.shields.io/badge/Python-3.12-blue)

![PySpark](https://img.shields.io/badge/PySpark-4.0-orange)

![Azure](https://img.shields.io/badge/Azure-Cloud-blue)

![Databricks](https://img.shields.io/badge/Databricks-Data%20Engineering-red)

![Delta](https://img.shields.io/badge/Delta%20Lake-Storage-green)

## Objetivo

O projeto simula um cenário corporativo de Engenharia de Dados, realizando ingestão, transformação e disponibilização de dados públicos da ANAC utilizando uma arquitetura Lakehouse baseada em Azure Databricks e Delta Lake.

---

## Arquitetura da Solução

![Arquitetura](docs/arquitetura.png)

O pipeline realiza a ingestão de arquivos JSON, processa os dados utilizando PySpark no Azure Databricks e persiste cada etapa em Delta Lake seguindo a arquitetura Medallion.

---

## Tecnologias

* Azure
* Azure Databricks
* Azure Storage
* Python
* PySpark
* Spark SQL
* Delta Lake

---

## Domínio do Problema

Este projeto utiliza dados públicos de Ocorrências Aeronáuticas disponibilizados pela ANAC.

O conjunto de dados reúne informações sobre ocorrências envolvendo aeronaves civis no Brasil, incluindo características do evento, localização, tipo de ocorrência, fase do voo, aeronave envolvida e demais informações relevantes para análises de segurança operacional.

Embora o foco do projeto seja demonstrar conceitos de Engenharia de Dados, a utilização de um conjunto de dados real permite simular desafios comuns encontrados em ambientes corporativos, como ingestão, tratamento, padronização e disponibilização de dados para consumo analítico.

---

## Organização da Solução

```text
.
├── bronze/        # Camada Bronze (dados brutos)
├── silver/        # Camada Silver (dados tratados)
├── gold/          # Camada Gold (dados para consumo analítico)
├── params/        # Configurações e parâmetros reutilizáveis
├── docs/          # Documentos
└── README.md
```

A organização do projeto segue a arquitetura Medallion, separando as responsabilidades de cada camada do pipeline e facilitando a manutenção, reutilização e evolução da solução.

---

## Fonte dos Dados

Os dados utilizados neste projeto são provenientes do portal de **Dados Abertos da Agência Nacional de Aviação Civil (ANAC)**, disponibilizados para uso público com o objetivo de promover transparência e incentivar análises sobre segurança operacional da aviação civil brasileira.

**Conjunto de dados:** Ocorrências Aeronáuticas

**Fonte oficial:** https://sistemas.anac.gov.br/dadosabertos/Seguranca%20Operacional/Ocorrencia/

Os arquivos são disponibilizados no formato JSON e utilizados como fonte de ingestão para o pipeline implementado neste projeto.

---

## Fluxo do Pipeline

```text
                     Dados Abertos ANAC
                      (Arquivos JSON)
                             │
                             ▼
              Azure Storage (Container)
                 resource/origem (JSON)
                             │
                             ▼
             Azure Databricks + PySpark
                             │
                             ▼
         Bronze (Delta Lake - Container Azure)
        Dados brutos persistidos em Delta
                             │
                             ▼
         Silver (Delta Lake - Container Azure)
      Dados tratados e padronizados
                             │
                             ▼
          Gold (Delta Lake - Container Azure)
      Dados consolidados para Analytics
                             │
                             ▼
               Consumo Analítico / BI
```

---
