import re
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Defina o nome do arquivo manualmente aqui
NOME_ARQUIVO = "NAPadrao100.txt"

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

def gerar_graficos(dados_ping, dados_jitter_perda, nome_arquivo):
    """Gera dois gráficos separados para ping e para jitter/perda de pacotes."""
    
    fig, axs = plt.subplots(2, 1, figsize=(12, 10))
    
    def adicionar_textos(ax, categorias, valores, erros):
        for i, (cat, val, erro) in enumerate(zip(categorias, valores, erros)):
            texto = f'{val:.2f}'
            if erro[0] is not None:
                texto += f'\nIC99%: ({val - erro[0]:.2f}, {val + erro[1]:.2f})'
            ax.text(val, i, texto, ha='left', va='center', fontsize=10, color='black', fontweight='bold')
    
    # Gráfico de Ping
    categorias_ping = list(dados_ping.keys())
    valores_ping = [dados_ping[cat][2] for cat in categorias_ping]
    erros_ping = [(dados_ping[cat][2] - dados_ping[cat][3][0] if dados_ping[cat][3] else 0, 
                   dados_ping[cat][3][1] - dados_ping[cat][2] if dados_ping[cat][3] else 0) 
                  for cat in categorias_ping]
    erro_baixo_ping, erro_alto_ping = zip(*erros_ping)
    
    axs[0].barh(categorias_ping, valores_ping, xerr=[erro_baixo_ping, erro_alto_ping], capsize=10, color='skyblue', alpha=0.7)
    axs[0].set_title(f"Métricas de Ping ({nome_arquivo}) Para 99%")
    axs[0].grid(axis='x', linestyle='--', alpha=0.7)
    adicionar_textos(axs[0], categorias_ping, valores_ping, erros_ping)
    
    # Gráfico de Jitter e Perda de Pacotes
    categorias_jp = list(dados_jitter_perda.keys())
    valores_jp = [dados_jitter_perda[cat][2] for cat in categorias_jp]
    erros_jp = [(dados_jitter_perda[cat][2] - dados_jitter_perda[cat][3][0] if dados_jitter_perda[cat][3] else 0, 
                 dados_jitter_perda[cat][3][1] - dados_jitter_perda[cat][2] if dados_jitter_perda[cat][3] else 0) 
                for cat in categorias_jp]
    erro_baixo_jp, erro_alto_jp = zip(*erros_jp)
    
    axs[1].barh(categorias_jp, valores_jp, xerr=[erro_baixo_jp, erro_alto_jp], capsize=10, color='lightcoral', alpha=0.7)
    axs[1].set_title(f"Métricas de Jitter e Perda de Pacotes ({nome_arquivo}) Para 99%")
    axs[1].grid(axis='x', linestyle='--', alpha=0.7)
    adicionar_textos(axs[1], categorias_jp, valores_jp, erros_jp)
    
    plt.tight_layout()
    plt.savefig(f"Metricas_{nome_arquivo.replace('.txt', '')}.png")
    plt.close()

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
    
    dados_ping = {
        "Ping Máx": (None, None, stats_ping_real[1], None),
        "Ping Mín": (None, None, stats_ping_real[0], None),
        "Ping Médio": stats_ping_medio,
    }
    
    dados_jitter_perda = {
        "Perda de Pacotes": stats_perda_pacotes,
        "Jitter Máx": (None, None, stats_jitter[1], None),
        "Jitter Mín": (None, None, stats_jitter[0], None),
        "Jitter Médio": stats_jitter
    }
    
    gerar_graficos(dados_ping, dados_jitter_perda, nome_arquivo)

processar_arquivo(NOME_ARQUIVO)
