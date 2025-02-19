import re
import math

# Arquivos de entrada e saída
arquivo_entrada = 'T1BREXIT.txt'
arquivo_saida_dados = 'dadosBR_filtrados2.txt'
arquivo_saida_calculos = 'calculosBR_resultados2.txt'

# Variáveis para cálculos
tempo_max_total = 0
perda_pacotes_total = 0
oscilacao_total = 0
trajeto_total = 0
valores_tempo_max = []
valores_perda_pacotes = []
valores_oscilacao = []
valores_trajeto = []
contador = 0  

# Limpa o arquivo de saída antes de começar
with open(arquivo_saida_dados, 'w', encoding='utf-8') as f_out:
    f_out.write("Tempo Max | Perda de Pacote | Oscilação | Tempo de Trajeto Completo\n")

# Leitura e filtragem dos dados
with open(arquivo_entrada, 'r', encoding='utf-8') as f_in:
    for linha in f_in:
        print("Linha lida:", linha.strip())  # Depuração para ver cada linha lida

        # Expressões regulares para capturar os valores
        tempo_max = re.search(r'\((\d+)ms\)', linha)  
        perda_pacotes = re.search(r'Perdadepacotes:(\d+)%', linha)
        oscilacao = re.search(r'Oscilac(?:ado|do)?\s*de\s*tempo\s*de\s*trajeto.*?([\d]+\.?\d*)ms', linha, re.IGNORECASE)
        trajeto_completo = re.search(r'Média do tempo de trajeto completo.*?(\d+)ms', linha, re.IGNORECASE)

        linha_filtrada = []

        if tempo_max:
            tempo_max_value = int(tempo_max.group(1))
            tempo_max_total += tempo_max_value
            valores_tempo_max.append(tempo_max_value)
            linha_filtrada.append(f"{tempo_max_value}ms")
        
        if perda_pacotes:
            perda_pacotes_value = int(perda_pacotes.group(1))
            perda_pacotes_total += perda_pacotes_value
            valores_perda_pacotes.append(perda_pacotes_value)
            linha_filtrada.append(f"Perda de Pacote:{perda_pacotes_value}%")
        
        if oscilacao:
            oscilacao_value = float(oscilacao.group(1))
            oscilacao_total += oscilacao_value
            valores_oscilacao.append(oscilacao_value)
            linha_filtrada.append(f"{oscilacao_value}ms")

        if trajeto_completo:
            trajeto_value = int(trajeto_completo.group(1))
            trajeto_total += trajeto_value
            valores_trajeto.append(trajeto_value)
            linha_filtrada.append(f"Trajeto: {trajeto_value}ms")

        if linha_filtrada:
            with open(arquivo_saida_dados, 'a', encoding='utf-8') as f_out:
                f_out.write(" | ".join(linha_filtrada) + "\n")
            contador += 1

# Cálculos estatísticos
if contador > 0:
    media_tempo_max = tempo_max_total / contador
    media_perda_pacotes = perda_pacotes_total / contador
    media_oscilacao = oscilacao_total / contador
    media_trajeto = trajeto_total / contador if valores_trajeto else "Sem dados"

    maior_trajeto = max(valores_trajeto) if valores_trajeto else "Sem dados"
    menor_trajeto = min(valores_trajeto) if valores_trajeto else "Sem dados"

    maior_oscilacao = max(valores_oscilacao) if valores_oscilacao else "Sem dados"
    menor_oscilacao = min(valores_oscilacao) if valores_oscilacao else "Sem dados"

    desvio_tempo_max = math.sqrt(sum((x - media_tempo_max) ** 2 for x in valores_tempo_max) / contador)
    desvio_perda_pacotes = math.sqrt(sum((x - media_perda_pacotes) ** 2 for x in valores_perda_pacotes) / contador)
    desvio_oscilacao = math.sqrt(sum((x - media_oscilacao) ** 2 for x in valores_oscilacao) / contador)
    desvio_trajeto = (
        math.sqrt(sum((x - media_trajeto) ** 2 for x in valores_trajeto) / contador)
        if isinstance(media_trajeto, (int, float)) else "Sem dados"
    )

    # Salva os cálculos em um arquivo
    with open(arquivo_saida_calculos, 'w', encoding='utf-8') as f_calculos:
        f_calculos.write(f"Média do Tempo Máximo: {media_tempo_max:.2f} ms\n")
        f_calculos.write(f"Média da Perda de Pacote: {media_perda_pacotes:.2f}%\n")
        f_calculos.write(f"Média da Oscilação: {media_oscilacao:.2f} ms\n")
        f_calculos.write(f"Média do Tempo de Trajeto Completo: {media_trajeto}\n\n")

        f_calculos.write(f"Desvio Padrão do Tempo Máximo: {desvio_tempo_max:.2f} ms\n")
        f_calculos.write(f"Desvio Padrão da Perda de Pacote: {desvio_perda_pacotes:.2f}%\n")
        f_calculos.write(f"Desvio Padrão da Oscilação: {desvio_oscilacao:.2f} ms\n")
        f_calculos.write(f"Desvio Padrão do Tempo de Trajeto Completo: {desvio_trajeto}\n\n")

        f_calculos.write(f"Maior Tempo de Trajeto Completo: {maior_trajeto} ms\n")
        f_calculos.write(f"Menor Tempo de Trajeto Completo: {menor_trajeto} ms\n\n")

        f_calculos.write(f"Maior Oscilação do Tempo de Trajeto: {maior_oscilacao} ms\n")
        f_calculos.write(f"Menor Oscilação do Tempo de Trajeto: {menor_oscilacao} ms\n")

else:
    print("Nenhuma linha válida foi encontrada para cálculo.")

print("✅ Filtragem e cálculos concluídos! Confira os arquivos:")
print(f"- 📂 Dados filtrados: {arquivo_saida_dados}")
print(f"- 📂 Cálculos: {arquivo_saida_calculos}")
