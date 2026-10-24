# termometro.py
import os
import matplotlib.pyplot as plt

# 1. Pontos fornecidos: (temperatura, corrente)
x1, y1 = 0, 4
x2, y2 = 100, 20

# 2. Cálculo dos coeficientes a e b (y = ax + b)
a = (y2 - y1) / (x2 - x1)
b = y1 - a * x1

# 3. Valor para teste: x = 50 graus
x = 50
y = a * x + b

print(f"Coeficiente a = {a}")
print(f"Coeficiente b = {b}")
print(f"Temperatura (x): {x} °C")
print(f"Corrente (y): {y} mA")

# 4. Verificação de avisos de faixa
if x < 0 or x > 100:
    print("AVISO: Temperatura fora da faixa esperada (0°C a 100°C)!")
else:
    print("Temperatura dentro da faixa permitida (0-100°C).")

if y < 4 or y > 20:
    print("AVISO: Corrente elétrica fora da faixa padrão (4 mA a 20 mA)!")
else:
    print("Corrente dentro da faixa padrão (4-20 mA).")

# 5. Classificação da temperatura
if x <= 30:
    classificacao = "Baixa"
elif x <= 60:
    classificacao = "Média"
else:
    classificacao = "Alta"

print(f"Classificação da temperatura: {classificacao}")

# 6. Geração do gráfico
faixa_temp = [0, 20, 40, 60, 80, 100]
faixa_corrente = [a * t + b for t in faixa_temp]

plt.figure(figsize=(8, 5))
plt.plot(faixa_temp, faixa_corrente, label="Reta y = ax + b", color="blue")
plt.scatter([x], [y], color="red", zorder=5, label=f"Ponto avaliado ({x}°C, {y}mA)")

plt.title("Termômetro: Corrente Elétrica vs Temperatura")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Corrente Elétrica (mA)")
plt.grid(True)
plt.legend()

# Garantir que a pasta resultados/ existe e salvar o gráfico
os.makedirs("resultados", exist_ok=True)
caminho_grafico = os.path.join("resultados", "grafico_termometro.png")
plt.savefig(caminho_grafico)
plt.close()

print(f"Gráfico salvo com sucesso em: {caminho_grafico}")

if y < 4 or y > 20:
    print("AVISO: Corrente elétrica fora da faixa padrão (4 mA a 20 mA)!")
else:
    print("Corrente dentro da faixa padrão (4-20 mA).")

# 5. Classificação da temperatura
if x <= 30:
    classificacao = "Baixa"
elif x <= 60:
    classificacao = "Média"
else:
    classificacao = "Alta"

print(f"Classificação da temperatura: {classificacao}")

# 6. Geração do gráfico
faixa_temp = [0, 20, 40, 60, 80, 100]
faixa_corrente = [a * t + b for t in faixa_temp]

plt.figure(figsize=(8, 5))
plt.plot(faixa_temp, faixa_corrente, label="Reta y = ax + b", color="blue")
plt.scatter([x], [y], color="red", zorder=5, label=f"Ponto avaliado ({x}°C, {y}mA)")

plt.title("Termômetro: Corrente Elétrica vs Temperatura")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Corrente Elétrica (mA)")
plt.grid(True)
plt.legend()

# Garantir que a pasta resultados/ existe e salvar o gráfico
os.makedirs("resultados", exist_ok=True)
caminho_grafico = os.path.join("resultados", "grafico_termometro.png")
plt.savefig(caminho_grafico)
plt.close()

print(f"Gráfico salvo com sucesso em: {caminho_grafico}")

