# Relatório de Qualidade dos Dados (`fornecedores_erro.csv`)

## 1. Visão Geral da Base
- **Arquivo auditado**: `dados/fornecedores_erro.csv`
- **Colunas declaradas no cabeçalho (5)**: `fornecedor, preco_unitario, prazo_dias, defeitos_pct, suporte_nota`
- **Total de linhas de fornecedores**: 4

## 2. Problemas Encontrados e Evidências Numéricas

Foram identificados **3 problemas críticos** na base:

| Linha | Fornecedor | Problema Detectado | Conteúdo da Linha |
|:---:|:---|:---|:---|
| 2 | Alfa | Inconsistência de colunas (esperadas 5, encontradas 4) | `['Alfa', '90', '2', '8']` |
| 3 | Beta | Valor ausente na coluna 'suporte_nota' | `['Beta', '100', '5', '1', '']` |
| 5 | Delta | Valor ausente na coluna 'preco_unitario' | `['Delta', '', '4', '0.5', '9.5']` |

## 3. Detalhamento dos Erros por Fornecedor

1. **Linha 2 (Alfa)**: A linha contém apenas 4 valores em vez dos 5 esperados (`['Alfa', '90', '2', '8']`). Falta um campo separador ou valor de prazo/defeito, causando deslocamento de colunas.
2. **Linha 3 (Beta)**: O campo `suporte_nota` está vazio (`''`).
3. **Linha 5 (Delta)**: O campo `preco_unitario` está vazio (`''`).
4. **Linha 4 (Gama)**: É a única linha estruturalmente completa e sem campos vazios.

## 4. Tratamentos Propostos

- **Não utilizar esta base diretamente** na matriz de decisão ou em modelos sem correção prévia.
- **Corrigir a Linha 2 (Alfa)**: Alinhar com a fonte dos dados se o valor faltante é o prazo de entrega ou a taxa de defeito.
- **Tratar ausências em Beta e Delta**: Preencher com a fonte correta os valores ausentes de suporte do Beta e preço do Delta antes de rodar os algoritmos.
