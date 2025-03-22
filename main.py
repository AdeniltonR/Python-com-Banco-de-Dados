from bd import criar_tabelas, inserir_estados, iniciar_valor_total_estados_zero, inserir_top_100_doadores, atualizar_valor_total_estados, buscar_ultimas_arrecadacoes
from copiar_conteudo_html_top_100_doadores import copiar_conteudo_html_top_doadores
from buscar_arrecadacao_atual import arrecadacao_atual
from extrair_dados_mapa_doacao_por_estados import coletar_doacao_por_estados_site
# Função principal para executar todas as atividades
def menu():
    while True:
        opc = input('''
                Gestão e Acompanhamento do scrapping DoeArenaCorinthians

            1 - Criar tabelas e adicionar dados bases
            2 - Atualizar Top 100 doadores (site -> arquivo)
            3 - Inserir Top 100 doadores (arquivo -> bd)
            4 - Atualizar doações por Estados (arquivo -> bd)
            5 - Buscar arrecadação atual            
            6 - Listas as últimas arrecadações
            7 - Atualizar doações por Estados (site -> arquivo) 
            ? - Para SAIR pressione qualquer outra tecla
            
            ''')
        if opc=="1":
            criar_tabelas()
            inserir_estados()
            iniciar_valor_total_estados_zero()
            inserir_top_100_doadores() #dados que contém no diretorio
        elif opc == "2":
            copiar_conteudo_html_top_doadores()
        elif opc == "3":
            inserir_top_100_doadores()
        elif opc == "4":
            atualizar_valor_total_estados()
        elif opc =='5' :
            arrecadacao_atual()
        elif opc =='6':
            buscar_ultimas_arrecadacoes()
        elif opc =='7':
            coletar_doacao_por_estados_site()
        else:
            break


# Executa o script
if __name__ == "__main__":
    menu()