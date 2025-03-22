from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bd import inserir_arrecadacao, converter_para_float




def arrecadacao_atual():
    # Inicia o WebDriver
    driver = webdriver.Firefox()    
    driver.get('https://www.doearenacorinthians.com.br')    
    try:
        # Aguarda a div carregar
        arrecadacadado = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "goal-raised__moment"))
        )

        # Agora busca a <p> dentro da div
        valor_arrecadado = arrecadacadado.find_element(By.TAG_NAME, "p").text

        #print(valor_arrecadado)        

        inserir_arrecadacao(converter_para_float(valor_arrecadado))

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    arrecadacao_atual()