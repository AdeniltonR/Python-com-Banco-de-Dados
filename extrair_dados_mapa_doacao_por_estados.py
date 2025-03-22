from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Lista de estados
estados = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", 
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", 
    "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

def coletar_doacao_por_estados_site():
    # URL da página
    url = 'https://www.doearenacorinthians.com.br/acompanhe-doacao'

    # Inicia o WebDriver
    driver = webdriver.Firefox()
    driver.set_window_size(1200, 800)  # Define um tamanho fixo para evitar zoom
    driver.get(url)

    try:
        # Aguarda o carregamento do SVG
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "svg"))
        )

        # Dicionário para armazenar os valores arrecadados
        arrecadacoes = {}

        for estado in estados:
            try:
                # Encontra o elemento pelo atributo state correto
                estado_elemento = driver.find_element(By.XPATH, f"//*[@state='{estado}']")

                # Usa JavaScript para forçar o clique e evitar sobreposição
                driver.execute_script("arguments[0].dispatchEvent(new Event('click', {bubbles: true}));", estado_elemento)

                # Aguarda a arrecadação aparecer
                arrecadacao_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'donation-map__collected-by-state__collection'))
                )

                # Captura o texto da arrecadação
                arrecadacao = arrecadacao_element.text.strip()

                # Salva no dicionário
                arrecadacoes[estado] = arrecadacao

                #print(f"Arrecadação de {estado}: {arrecadacao}")

                # Pequena pausa para evitar problemas de carregamento
                time.sleep(1)

            except Exception as e:
                print(f"Erro ao capturar {estado}: {e}")

    except Exception as e:
        print(f"Erro geral: {e}")

    finally:
        driver.quit()

    #SALVAR EM UM ARQUIVO
    with open("dados/arrecadacoes_estados.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(f"{arrecadacoes}")

    # Exibe os dados coletados
    # print("\nResumo das arrecadações:")
    # for estado, valor in arrecadacoes.items():
    #     print(f"{estado}: {valor}")


if __name__ == "__main__":
    coletar_doacao_por_estados_site()