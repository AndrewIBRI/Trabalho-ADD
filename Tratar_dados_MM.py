import re
import os
import numpy as np
import scipy.stats as stats

# Defina o nome do arquivo manualmente aqui
NOME_ARQUIVO = "BRPadrao.txt"


def extrair_metricas(linha):
    """Extrai Ping, perda de pacotes e Jitter da linha fornecida."""
    padrao = re.compile(r'Média do tempo de trajeto completo da rede .*?: (\d+)ms \((\d+)ms\) '
                         r'Perda\s*de\s*pacotes:\s*(\d+)%\s* '
                         r'Oscil(?:a[cç][aã]o|acado|acdo)\s*de\s*tempo\s*de\s*trajeto\s*completo\s*da\s*rede:\s*([\d.]+)ms',
                         re.IGNORECASE)
    
    match = padrao.search(linha)
    if match:
        ping_tempo_real = int(match.group(1))
        ping_medio = int(match.group(2))
        perda_pacotes = int(match.group(3))
        jitter = float(match.group(4))
        return ping_tempo_real, ping_medio, perda_pacotes, jitter
    return None


def calcular_estatisticas(valores):
    """Calcula estatísticas principais e intervalo de confiança de 99%."""
    if not valores:
        return None, None, None, None
    
    min_valor = min(valores)
    max_valor = max(valores)
    media = np.mean(valores)
    desvio_padrao = np.std(valores, ddof=1) if len(valores) > 1 else 0
    
    n = len(valores)
    if n > 1:
        t_critico = stats.t.ppf(0.995, df=n-1)  # t-distribuição para 99%
        margem_erro = t_critico * (desvio_padrao / np.sqrt(n))
        intervalo_confianca = (media - margem_erro, media + margem_erro)
    else:
        intervalo_confianca = (media, media)
    
    return min_valor, max_valor, media, intervalo_confianca


def salvar_resultados(dados_ping, dados_jitter_perda, nome_arquivo):
    """Salva os dados extraídos em um arquivo de texto dentro da pasta resultados_texto."""
    pasta_resultados = "resultados_texto"
    os.makedirs(pasta_resultados, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_resultados, f"Resultados_{nome_arquivo.replace('.txt', '')}.txt")
    
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write("=== Estatísticas de Ping ===\n")
        for chave, valores in dados_ping.items():
            f.write(f"{chave}: {valores}\n")
        
        f.write("\n=== Estatísticas de Jitter e Perda de Pacotes ===\n")
        for chave, valores in dados_jitter_perda.items():
            f.write(f"{chave}: {valores}\n")
    
    print(f"Resultados salvos em: {caminho_arquivo}")


def processar_arquivo(nome_arquivo):
    """Lê o arquivo e processa os dados."""
    ping_tempo_real_valores = []
    ping_medio_valores = []
    perda_pacotes_valores = []
    jitter_valores = []
    
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                dados = extrair_metricas(linha)
                if dados:
                    ping_tempo_real_valores.append(dados[0])
                    ping_medio_valores.append(dados[1])
                    perda_pacotes_valores.append(dados[2])
                    jitter_valores.append(dados[3])
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return
    except UnicodeDecodeError:
        print(f"Erro de codificação ao ler '{nome_arquivo}'. Tente converter para UTF-8.")
        return
    
    if not ping_tempo_real_valores:
        print(f"Erro: Nenhuma métrica válida foi encontrada no arquivo '{nome_arquivo}'.")
        return
    
    stats_ping_real = calcular_estatisticas(ping_tempo_real_valores)
    stats_ping_medio = calcular_estatisticas(ping_medio_valores)
    stats_perda_pacotes = calcular_estatisticas(perda_pacotes_valores)
    stats_jitter = calcular_estatisticas(jitter_valores)
    
    dados_ping = {"Ping Máx": stats_ping_real[:3] + (None,), "Ping Mín": stats_ping_real[:2] + (None,), "Ping Médio": stats_ping_medio}
    dados_jitter_perda = {"Perda de Pacotes": stats_perda_pacotes, "Jitter Máx": stats_jitter[:3] + (None,), "Jitter Mín": stats_jitter[:2] + (None,), "Jitter Médio": stats_jitter}
    
    salvar_resultados(dados_ping, dados_jitter_perda, nome_arquivo)

processar_arquivo(NOME_ARQUIVO)
