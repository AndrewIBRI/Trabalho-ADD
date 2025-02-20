import re
import matplotlib.pyplot as plt

# Nome do arquivo contendo os dados
arquivo_entrada = "calculosNA_resultados1.txt"

# Expressões regulares para capturar os valores numéricos
regex_valores = {
    "Media do Tempo De Trajeto": r"Média do Tempo Máximo:\s*([\d.]+)",
    "Media da Perda de Pacote": r"Média da Perda de Pacote:\s*([\d.]+)",
    "Media da Oscilacao": r"Média da Oscilação:\s*([\d.]+)",
    "Media do Tempo de Trajeto Completo": r"Média do Tempo de Trajeto Completo:\s*([\d.]+)",
    "Desvio Padrao do Tempo Maximo": r"Desvio Padrão do Tempo Máximo:\s*([\d.]+)",
    "Desvio Padrao da Perda de Pacote": r"Desvio Padrão da Perda de Pacote:\s*([\d.]+)",
    "Desvio Padrao da Oscilacao": r"Desvio Padrão da Oscilação:\s*([\d.]+)",
    "Desvio Padrao do Tempo de Trajeto Completo": r"Desvio Padrão do Tempo de Trajeto Completo:\s*([\d.]+)",
    "Maior Tempo de Trajeto Completo": r"Maior Tempo de Trajeto Completo:\s*([\d.]+)",
    "Menor Tempo de Trajeto Completo": r"Menor Tempo de Trajeto Completo:\s*([\d.]+)",
    "Maior Oscilacao do Tempo de Trajeto": r"Maior Oscilação do Tempo de Trajeto:\s*([\d.]+)",
    "Menor Oscilacao do Tempo de Trajeto": r"Menor Oscilação do Tempo de Trajeto:\s*([\d.]+)"
}

# Dicionario para armazenar os valores extraidos
valores_extraidos = {}

# Ler o arquivo e extrair os valores
with open(arquivo_entrada, "r", encoding="utf-8") as f:
    conteudo = f.read()
    for chave, regex in regex_valores.items():
        match = re.search(regex, conteudo)
        if match:
            valores_extraidos[chave] = float(match.group(1))
        else:
            valores_extraidos[chave] = None

# Exibir os valores extraidos organizados no terminal
print("\n" + "="*40)
print(" DADOS EXTRAIDOS DO ARQUIVO")
print("="*40)
for chave, valor in valores_extraidos.items():
    if valor is not None:
        print(f"{chave.ljust(45)}: {valor:.2f}")
    else:
        print(f"{chave.ljust(45)}: N/A")

# Criando o gráfico com as métricas solicitadas
metricas_selecionadas = [
    "Media do Tempo De Trajeto",
    "Maior Tempo de Trajeto Completo",
    "Menor Tempo de Trajeto Completo",
    "Maior Oscilacao do Tempo de Trajeto",
    "Menor Oscilacao do Tempo de Trajeto"
]

valores_selecionados = [valores_extraidos[m] for m in metricas_selecionadas]

plt.figure(figsize=(10, 6))
bars = plt.bar(metricas_selecionadas, valores_selecionados, color=["blue", "red", "green", "purple", "cyan"])
plt.title("Valores das Métricas Selecionadas")
plt.ylabel("Tempo (ms)")

# Adiciona os valores nas barras
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, f"{yval:.2f} ms", ha="center", va="bottom", fontsize=10, fontweight="bold")

plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.show()
