from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def copiar_conteudo_html_top_doadores():
    url = 'https://www.doearenacorinthians.com.br/acompanhe-doacao'

    # Inicia o WebDriver
    driver = webdriver.Firefox()
    driver.set_window_size(1200, 800)  # Define um tamanho fixo para evitar zoom
    driver.get(url)    

    try:
        # Aguarda a presença da div específica
        elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "top__hundred-donors"))
        )

        # Captura o HTML do bloco específico
        bloco_html = elemento.get_attribute("outerHTML")

        # Salva o HTML em um arquivo
        with open("dados/conteudo_para_extracao_top100doadores.txt", "w", encoding="utf-8") as file:
            file.write(bloco_html)

        print("✅ Bloco salvo com sucesso'")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        # Fecha o navegador
        driver.quit()
