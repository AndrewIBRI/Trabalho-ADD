import re
import math

# Arquivos de entrada e saída
arquivo_entrada = 'T3NAPadrao.txt'  # Nome correto do arquivo de entrada
arquivo_saida_dados = 'dadosNA_filtrados.txt'  # Arquivo para os dados filtrados
arquivo_saida_calculos = 'calculosNA_resultados.txt'  # Arquivo para os resultados dos cálculos (média e desvio padrão)

# Variáveis para acumular os valores e realizar os cálculos
tempo_max_total = 0
perda_pacotes_total = 0
oscilacao_total = 0
contador = 0  # Para contar quantas linhas foram processadas

# Para calcular o desvio padrão
tempo_max_quadrado_diff = 0
perda_pacotes_quadrado_diff = 0
oscilacao_quadrado_diff = 0

# Limpa o arquivo de saída antes de escrever novos dados
with open(arquivo_saida_dados, 'w', encoding='utf-8') as f_out:
    # Escreve o cabeçalho do arquivo de saída (colunas)
    f_out.write("Tempo Max | Perda de Pacote | Oscilação de Tempo de Trajeto Completo da Rede\n")

# Leitura e filtragem das informações
with open(arquivo_entrada, 'r', encoding='utf-8') as f_in:
    for linha in f_in:
        # Vamos imprimir a linha para garantir que estamos lendo corretamente
        print("Linha lida:", linha)  # Verifique a linha lida
        
        # Filtrando cada informação usando expressões regulares
        tempo_max = re.search(r'\((\d+ms)\)', linha)  # Tempo entre parênteses
        perda_pacotes = re.search(r'Perdadepacotes:(\d+)%', linha)  # Perda de pacotes
        oscilacao = re.search(r'Oscilac(?:ado|do)?\s*de\s*tempo\s*de\s*trajeto\s*completo\s*da\s*rede?:\s*([\d]+ms|\d+\.\d+ms)', linha)

        linha_filtrada = []

        if tempo_max:
            tempo_max_value = int(tempo_max.group(1).replace('ms', ''))
            tempo_max_total += tempo_max_value
            tempo_max_quadrado_diff += (tempo_max_value - tempo_max_total / (contador + 1)) ** 2  # Acumula a soma dos quadrados das diferenças
            linha_filtrada.append(f"{tempo_max_value}ms")
        
        if perda_pacotes:
            perda_pacotes_value = int(perda_pacotes.group(1))  # Perda de pacotes como inteiro
            perda_pacotes_total += perda_pacotes_value
            perda_pacotes_quadrado_diff += (perda_pacotes_value - perda_pacotes_total / (contador + 1)) ** 2  # Soma dos quadrados das diferenças
            linha_filtrada.append(f"Perda de Pacote:{perda_pacotes_value}%")
        
        if oscilacao:
            oscilacao_value = float(oscilacao.group(1).replace('ms', ''))  # Oscilação como float
            oscilacao_total += oscilacao_value
            oscilacao_quadrado_diff += (oscilacao_value - oscilacao_total / (contador + 1)) ** 2  # Soma dos quadrados das diferenças
            # Corrigindo o erro de digitação e formatando
            oscilacao_texto = oscilacao.group(0).replace("Oscilacdo", "Oscilação").replace("Oscilacado", "Oscilação")
            oscilacao_texto = oscilacao_texto.replace("darede", "da rede")
            linha_filtrada.append(oscilacao_texto)

        # Se encontrou alguma informação, salva no arquivo de saída de dados
        if linha_filtrada:
            with open(arquivo_saida_dados, 'a', encoding='utf-8') as f_out:
                f_out.write(" | ".join(linha_filtrada) + "\n")
            
            # Incrementa o contador
            contador += 1

# Cálculos das médias e desvios padrão
if contador > 0:
    media_tempo_max = tempo_max_total / contador
    media_perda_pacotes = perda_pacotes_total / contador
    media_oscilacao = oscilacao_total / contador

    # Cálculo do desvio padrão
    desvio_tempo_max = math.sqrt(tempo_max_quadrado_diff / contador)
    desvio_perda_pacotes = math.sqrt(perda_pacotes_quadrado_diff / contador)
    desvio_oscilacao = math.sqrt(oscilacao_quadrado_diff / contador)

    # Salva os cálculos em um novo arquivo de texto
    with open(arquivo_saida_calculos, 'w', encoding='utf-8') as f_calculos:
        f_calculos.write(f"Média do Tempo Máximo: {media_tempo_max:.2f} ms\n")
        f_calculos.write(f"Média da Perda de Pacote: {media_perda_pacotes:.2f}%\n")
        f_calculos.write(f"Média da Oscilação: {media_oscilacao:.2f} ms\n\n")
        f_calculos.write(f"Desvio Padrão do Tempo Máximo: {desvio_tempo_max:.2f} ms\n")
        f_calculos.write(f"Desvio Padrão da Perda de Pacote: {desvio_perda_pacotes:.2f}%\n")
        f_calculos.write(f"Desvio Padrão da Oscilação: {desvio_oscilacao:.2f} ms\n")
else:
    print("Nenhuma linha válida foi encontrada para cálculo.")

print("Filtragem e cálculos concluídos! Confira os arquivos:")
print(f"- Dados filtrados: {arquivo_saida_dados}")
print(f"- Cálculos (média e desvio padrão): {arquivo_saida_calculos}")
