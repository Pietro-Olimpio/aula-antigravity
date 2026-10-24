import os
import csv
import pandas as pd

origem = os.path.join("dados", "fornecedores_erro.csv")
destino = os.path.join("resultados", "fornecedores_corrigido.csv")

# 1. Leitura e correção estrutural linha a linha
linhas_corrigidas = []

with open(origem, "r", encoding="utf-8") as f:
    leitor = csv.reader(f)
    cabecalho = next(leitor)
    
    for linha in leitor:
        fornecedor = linha[0]
        
        # Correção Linha Alfa: vieram 4 campos ['Alfa', '90', '2', '8'], faltava prazo_dias (8)
        if fornecedor == "Alfa" and len(linha) == 4:
            linha_ajustada = ["Alfa", "90", "8", "2", "8"]
        # Correção Linha Beta: suporte_nota vazio -> preenchido com 9
        elif fornecedor == "Beta":
            linha_ajustada = [linha[0], linha[1], linha[2], linha[3], "9"]
        # Correção Linha Delta: preco_unitario vazio -> preenchido com 110
        elif fornecedor == "Delta":
            linha_ajustada = [linha[0], "110", linha[2], linha[3], linha[4]]
        else:
            linha_ajustada = linha
            
        linhas_corrigidas.append(linha_ajustada)

# 2. Criar DataFrame com os tipos de dados adequados
df_limpo = pd.DataFrame(linhas_corrigidas, columns=cabecalho)
df_limpo["preco_unitario"] = df_limpo["preco_unitario"].astype(float)
df_limpo["prazo_dias"] = df_limpo["prazo_dias"].astype(int)
df_limpo["defeitos_pct"] = df_limpo["defeitos_pct"].astype(float)
df_limpo["suporte_nota"] = df_limpo["suporte_nota"].astype(float)

# 3. Garantir diretório resultados/ e salvar arquivo corrigido
os.makedirs("resultados", exist_ok=True)
df_limpo.to_csv(destino, index=False)

print(f"Base corrigida salva com sucesso em: {destino}")
print("\nConteúdo da base tratada:")
print(df_limpo)

# 4. Validação final de qualidade
valores_nulos = df_limpo.isnull().sum().sum()
print(f"\nTotal de valores nulos após tratamento: {valores_nulos}")
if valores_nulos == 0 and len(df_limpo) == 4:
    print("STATUS: Base 100% íntegra e pronta para uso!")

