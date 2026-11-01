# Pipeline público

Esta pasta contém uma implementação demonstrativa, sem dados e sem dependência da infraestrutura comercial.

## Extração e validação

`extract_validate.py` lê o CSV oficial, aplica filtros, normaliza os campos e gera um JSON dividido em:

- `questions`: itens estruturalmente válidos;
- `review`: itens anulados, incompletos ou que exigem tratamento humano.

Use `--exam-code` quando quiser restringir o processamento a um caderno específico.

## Importação

`import_bundle.py` sempre começa em modo de validação local. A flag `--execute` envia lotes para um endpoint HTTP genérico configurado por:

- `PIPELINE_IMPORT_ENDPOINT`
- `PIPELINE_IMPORT_API_KEY`

Essas variáveis são apenas uma interface de exemplo. Não correspondem aos nomes, URLs ou contratos da infraestrutura privada. Nunca versione valores reais.

Exemplo de validação:

```bash
python pipeline/scripts/import_bundle.py pipeline/data/output/questions.json
```

Exemplo de execução contra uma implementação própria e segura:

```bash
python pipeline/scripts/import_bundle.py \
  pipeline/data/output/questions.json \
  --execute \
  --batch-size 20
```

O endpoint de demonstração deve aceitar `POST` com o corpo `{"questions": [...]}` e responder com JSON. O contrato real da plataforma não é exposto aqui.

