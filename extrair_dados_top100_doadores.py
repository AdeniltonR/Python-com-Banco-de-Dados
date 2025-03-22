import re

def top_100_doadores():
    #Conteúdo das informações está aqui: https://www.doearenacorinthians.com.br/acompanhe-doacao
    # Abrir e ler o conteúdo do arquivo txt
    #ESSE ARQUIVO PRECISA SER GERADO
    with open('dados/conteudo_para_extracao_top100doadores.txt', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Regex para capturar todos os rankings e nomes de doadores
    pattern = r'<p[^>]*class="top__hundred-donors-slider__card__state"[^>]*>(\d+°)\s*</p>\s*<p[^>]*class="top__hundred-donors-slider__card__name"[^>]*>(.*?)</p>'

    # Procurar no conteúdo HTML
    matches = re.findall(pattern, html_content)

    # Abrir o arquivo de saída para escrever
    #referência 19/03/2025
    with open('dados/resultado_top_100_doadores.txt', 'w', encoding='utf-8') as output_file:
        for match in matches:
            rank = match[0]  # Rank (1°, 2°, 3°, ...)
            doador_estado = match[1]  # Nome do doador
            doador, estado = doador_estado.split(",")
            doacao_valor = 0.0
            #print(f'{rank} - {doador} - {estado}')
            # resultados direcionado para o arquivo de saída
            #output_file.write(f'{rank.strip()},{doador.strip()},{estado.strip()}\n')    
            output_file.write(f'{(doador.strip()).capitalize()},{estado.strip()},{doacao_valor}\n')    


if __name__ == "__main__":
    top_100_doadores()            