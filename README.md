# RentSmart

Aplicacao de terminal em Python que calcula orcamentos de locacao da R.M Imoveis, detalha aluguel e taxa contratual separadamente e gera uma projecao financeira dos 12 primeiros meses em CSV.

## Requisitos

- Python 3.10 ou superior
- Nenhuma biblioteca externa

## Como executar

```bash
python rentsmart.py
```

Responda as perguntas exibidas no terminal. Ao final, o arquivo `projecao_12_meses.csv` sera criado na pasta atual.

## Como executar os testes

```bash
python -m unittest -v
```

## Estrutura

- `rentsmart.py`: classes, validacoes, interface de terminal e geracao do CSV.
- `test_rentsmart.py`: testes automatizados das principais regras.
- `projecao_12_meses_exemplo.csv`: exemplo produzido pela aplicacao.
- `Documentacao_Teorica_RentSmart.pdf`: analise, algoritmo, fluxograma e estrutura de classes.
- `Roteiro_Pitch_RentSmart.pdf`: roteiro cronometrado para o video de ate quatro minutos.

## Conceitos aplicados

Abstracao, encapsulamento, heranca, polimorfismo, composicao, validacao de entradas e separacao de responsabilidades. Valores monetarios usam `Decimal` para evitar imprecisoes de ponto flutuante.

## Publicacao

Crie um repositorio no GitHub, envie os arquivos desta pasta e substitua abaixo pelo endereco publico ou nao listado do repositorio:

**Repositorio:** INSERIR_LINK_DO_GITHUB

Depois de gravar o pitch, inclua tambem o link:

**Video:** INSERIR_LINK_DO_VIDEO
