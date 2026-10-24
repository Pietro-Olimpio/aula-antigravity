import os
import csv

caminho_csv = os.path.join("dados", "fornecedores_erro.csv")

# 1. Leitura estrutural linha por linha (para detectar erros de formatação/colunas faltando)
linhas_problema = []
linhas_totais = 0
cabecalho = []

with open(caminho_csv, "r", encoding="utf-8") as f:
    leitor = csv.reader(f)
    cabecalho = next(leitor)
    qtd_colunas_esperadas = len(cabecalho)
    
    for i, linha in enumerate(leitor, start=2):
        linhas_totais += 1
        # Verificar se faltam colunas na linha
        if len(linha) != qtd_colunas_esperadas:
            linhas_problema.append({
                "linha": i,
                "fornecedor": linha[0] if len(linha) > 0 else "N/A",
                "tipo_erro": f"Inconsistência de colunas (esperadas {qtd_colunas_esperadas}, encontradas {len(linha)})",
                "conteudo": linha
            })
        else:
            # Verificar campos vazios
            for idx_col, valor in enumerate(linha):
                if valor.strip() == "":
                    linhas_problema.append({
                        "linha": i,
                        "fornecedor": linha[0],
                        "tipo_erro": f"Valor ausente na coluna '{cabecalho[idx_col]}'",
                        "conteudo": linha
                    })

print(f"Colunas esperadas ({len(cabecalho)}): {cabecalho}")
print(f"Total de registros de dados: {linhas_totais}")
print(f"Total de problemas detectados: {len(linhas_problema)}")

# 2. Gerar relatório resultados/qualidade.md conforme a skill conferir-csv
os.makedirs("resultados", exist_ok=True)
relatorio_qualidade = os.path.join("resultados", "qualidade.md")

with open(relatorio_qualidade, "w", encoding="utf-8") as f:
    f.write("# Relatório de Qualidade dos Dados (`fornecedores_erro.csv`)\n\n")
    f.write("## 1. Visão Geral da Base\n")
    f.write(f"- **Arquivo auditado**: `dados/fornecedores_erro.csv`\n")
    f.write(f"- **Colunas declaradas no cabeçalho ({len(cabecalho)})**: `{', '.join(cabecalho)}`\n")
    f.write(f"- **Total de linhas de fornecedores**: {linhas_totais}\n\n")
    
    f.write("## 2. Problemas Encontrados e Evidências Numéricas\n\n")
    f.write(f"Foram identificados **{len(linhas_problema)} problemas críticos** na base:\n\n")
    f.write("| Linha | Fornecedor | Problema Detectado | Conteúdo da Linha |\n")
    f.write("|:---:|:---|:---|:---|\n")
    for p in linhas_problema:
        f.write(f"| {p['linha']} | {p['fornecedor']} | {p['tipo_erro']} | `{p['conteudo']}` |\n")
    
    f.write("\n## 3. Detalhamento dos Erros por Fornecedor\n\n")
    f.write("1. **Linha 2 (Alfa)**: A linha contém apenas 4 valores em vez dos 5 esperados (`['Alfa', '90', '2', '8']`). Falta um campo separador ou valor de prazo/defeito, causando deslocamento de colunas.\n")
    f.write("2. **Linha 3 (Beta)**: O campo `suporte_nota` está vazio (`''`).\n")
    f.write("3. **Linha 5 (Delta)**: O campo `preco_unitario` está vazio (`''`).\n")
    f.write("4. **Linha 4 (Gama)**: É a única linha estruturalmente completa e sem campos vazios.\n\n")
    
    f.write("## 4. Tratamentos Propostos\n\n")
    f.write("- **Não utilizar esta base diretamente** na matriz de decisão ou em modelos sem correção prévia.\n")
    f.write("- **Corrigir a Linha 2 (Alfa)**: Alinhar com a fonte dos dados se o valor faltante é o prazo de entrega ou a taxa de defeito.\n")
    f.write("- **Tratar ausências em Beta e Delta**: Preencher com a fonte correta os valores ausentes de suporte do Beta e preço do Delta antes de rodar os algoritmos.\n")

print(f"Relatório de qualidade salvo em: {relatorio_qualidade}")

