import pandas as pd

# Carregar os dados do Wireshark exportados em CSV
df = pd.read_csv("LOLPBE-Wireshark.csv")

# Converter a coluna 'Time' para float para cálculos de tempo
df["Time"] = df["Time"].astype(float)

# Definir IP do servidor
ip_servidor = "192.207.0.2"

# Filtrar apenas pacotes UDP de Length = 61 vindos do servidor
pacotes_servidor = df[
    (df["Protocol"] == "UDP") & 
    (df["Length"] == 61) & 
    (df["Source"] == ip_servidor)
]

# Ordenar os pacotes pelo tempo
pacotes_servidor = pacotes_servidor.sort_values(by="Time").reset_index(drop=True)

# Calcular a diferença de tempo entre pacotes consecutivos
pacotes_servidor["Intervalo"] = pacotes_servidor["Time"].diff()

# Remover o primeiro valor NaN (o primeiro pacote não tem um anterior para calcular a diferença)
pacotes_servidor = pacotes_servidor.dropna()

# Converter para milissegundos
pacotes_servidor["Intervalo"] = pacotes_servidor["Intervalo"] * 1000

# Calcular estatísticas
intervalo_medio = pacotes_servidor["Intervalo"].mean()
intervalo_min = pacotes_servidor["Intervalo"].min()
intervalo_max = pacotes_servidor["Intervalo"].max()

# Exibir resultados
print(f"Intervalo Médio entre pacotes: {intervalo_medio:.2f} ms")
print(f"Intervalo Mínimo entre pacotes: {intervalo_min:.2f} ms")
print(f"Intervalo Máximo entre pacotes: {intervalo_max:.2f} ms")
