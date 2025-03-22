import sqlite3
import json
import datetime
import ast

NAME_BD ="arenacorinthinas.db"

estados = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", 
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", 
    "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

# Função para criar o banco de dados e as tabelas
def criar_tabelas():
    # Conecta ao banco de dados (ou cria um novo se não existir)
    conn = sqlite3.connect(NAME_BD)
    cursor = conn.cursor()

    # Criação da tabela de arrecadacao
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ARRECADACAO_ARENA (
        id INTEGER PRIMARY KEY,
        valor REAL NOT NULL,
        data DATE NOT NULL
    )
    ''')

    # Criação da tabela de estados do brasil
   
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ESTADOS  (
        id INTEGER PRIMARY KEY,
        codigo_ibge INTEGER,
        estado TEXT NOT NULL,
        capital TEXT NOT NULL,
        uf TEXT NOT NULL,
        regiao TEXT NOT NULL,    
        populacao REAL,
        idh REAL,
        expectativa_vida REAL,            
        site TEXT,
        cidades INTEGER,
        bandeira TEXT
    )
    ''')

    # Criação da tabela de estados_doacoes (Ranking de doaçoes dos estados)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ESTADOS_DOACOES (
        id INTEGER PRIMARY KEY,
        estados_id INTEGER,
        valor REAL NOT NULL,
        data DATE NOT NULL,
        FOREIGN KEY (estados_id) REFERENCES ESTADOS(id)
    )
    ''')

    # Criação da tabela de doadores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS DOADORES (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        valor,
        estados_id INTEGER,
        FOREIGN KEY (estados_id) REFERENCES ESTADOS(id)
    )
    ''')

    # Commit para salvar as alterações no banco
    conn.commit()
    print("Tabelas criadas com sucesso!")

    # Fecha a conexão ao banco de dados
    conn.close()

# Função para inserir dados de clientes, produtos, pedidos e itens de pedidos
def inserir_estados():
    # Conecta ao banco de dados
    conn = sqlite3.connect(NAME_BD)
    cursor = conn.cursor()
    # Inserir estados
    
     # Carregar os dados JSON (substitua pelo caminho correto do arquivo JSON)
    with open('dados/dados_estados.json', 'r', encoding='utf-8-sig') as file:
        estados = json.load(file)
        

    # Inserir os dados de cada estado na tabela ESTADOS
    for estado in estados:
        cursor.execute('''
            INSERT INTO ESTADOS (uf, bandeira, estado, capital, regiao, populacao, idh, expectativa_vida, site, cidades, codigo_ibge)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            estado['sigla'].upper(),
            estado['bandeira'],
            estado['estado'],
            estado['capital'],
            estado['regiao'],
            float(estado['populacao'].replace('.', '').replace(',', '.')),  # Convertendo população para REAL
            float(estado['idh'].replace(',', '.')),  # Convertendo IDH para REAL
            float(estado['expectativa_vida'].replace(',', '.')),  # Convertendo Expectativa de Vida para REAL
            estado['site'].strip(),  # Remover espaços extras na URL
            int(estado['cidades']),
            int(estado['codigo_ibge'])
        ))
    # Commit para salvar os dados
    conn.commit()
    print("Dados inseridos com sucesso!")

    # Fecha a conexão
    conn.close()

def iniciar_valor_total_estados_zero(valor=0.0):
    conn = sqlite3.connect(NAME_BD)
    cursor = conn.cursor()
    # Obtém a data e hora no formato desejado
    data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # DD/MM/YYYY HH:MM:SS
    for estado in estados:
        #print(estado)
        # Buscar o id do estado usando a sigla (sigla_estado)
        cursor.execute("SELECT id FROM ESTADOS WHERE uf = ?", (estado.upper(),))  # Adiciona a vírgula para formar uma tupla
        estado_id = cursor.fetchone()
        #print(estado_id)
        cursor.execute('''
                INSERT INTO ESTADOS_DOACOES (valor, data, estados_id)
                VALUES (?, ?, ?)
            ''', (valor, data_atual, estado_id[0]))  

    conn.commit()
    conn.close()
   

def atualizar_valor_total_estados():
    conn = sqlite3.connect(NAME_BD)
    cursor = conn.cursor()

    with open("dados/arrecadacoes_estados.txt", "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()

    # Converter o conteúdo do arquivo de volta para um dicionário Python
    arrecadacoes = ast.literal_eval(conteudo)
    data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # DD/MM/YYYY HH:MM:SS

    for estado, valor_arrecadado in arrecadacoes.items():  # Alterado para `.items()`
        cursor.execute("SELECT id FROM ESTADOS WHERE uf = ?", (estado.upper(),))
        estado_id = cursor.fetchone()

        if estado_id:
            estado_id = estado_id[0]  # Extrai o ID real
            valor_convertido = converter_para_float(valor_arrecadado)

            # Verifica se já existe um registro para o estado na tabela ESTADOS_DOACOES
            cursor.execute("SELECT COUNT(*) FROM ESTADOS_DOACOES WHERE estados_id = ?", (estado_id,))
            existe = cursor.fetchone()[0] > 0  # Se maior que zero, já existe um registro

            if existe:
                # Atualiza o valor e a data do registro existente
                cursor.execute('''
                    UPDATE ESTADOS_DOACOES 
                    SET valor = ?, data = ?
                    WHERE estados_id = ?
                ''', (valor_convertido, data_atual, estado_id))
                print(f"Atualizado: {estado} - R$ {valor_arrecadado}")
            else:
                # Insere um novo registro se não existir
                cursor.execute('''
                    INSERT INTO ESTADOS_DOACOES (valor, data, estados_id)
                    VALUES (?, ?, ?)
                ''', (valor_convertido, data_atual, estado_id))
                print(f"Inserido: {estado} - R$ {valor_arrecadado}")

        else:
            print(f"⚠️ Estado {estado} não encontrado no banco de dados!")

    conn.commit()
    conn.close()

def deletar_todos_doadores():
    conn = sqlite3.connect(NAME_BD)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM DOADORES")  # Remove todos os registros da tabela
    #cursor.execute("DELETE FROM sqlite_sequence WHERE name='DOADORES'")  # Reinicia a contagem de IDs

    conn.commit()  # Salva as alterações no banco de dados
    conn.close()  # Fecha a conexão

    #print("✅ Todos os registros da tabela DOADORES foram deletados.")
    
def inserir_top_100_doadores():
    # Conecta ao banco de dados
    conn = sqlite3.connect(NAME_BD)
    cursor = conn.cursor()

    # Carregar o arquivo de doadores
    with open('dados/resultado_top_100_doadores.txt', 'r', encoding='utf-8') as file:
        doadores = file.readlines()
    
    deletar_todos_doadores()

    # Iterar sobre cada linha do arquivo
    for doador in doadores:
        # Remover espaços em branco no começo e no final
        doador = doador.strip()

        # Separar o nome do doador e o estado
        nome_doador, sigla_estado, valor_doacao = doador.split(',')

        # Buscar o id do estado usando a sigla (sigla_estado)
        cursor.execute("SELECT id FROM ESTADOS WHERE uf = ?", (sigla_estado.strip().upper(),))  # Alterado para "uf"
        estado = cursor.fetchone()

        # Se o estado existir
        if estado:
            estado_id = estado[0]  # O id do estado
            # Inserir o doador na tabela DOADORES
            cursor.execute('''
                INSERT INTO DOADORES (nome, valor, estados_id)
                VALUES (?, ?, ?)
            ''', (nome_doador.capitalize(), valor_doacao, estado_id))  # Inserindo valor fictício (0.0) caso não tenha valor real
        else:
            # Inserir o doador na tabela DOADORES com o estado 0
            cursor.execute('''
                INSERT INTO DOADORES (nome, valor, estados_id)
                VALUES (?, ?, ?)
            ''', (nome_doador, valor_doacao, 0))  # Inserindo valor fictício (0.0) e estado 0
            print(f"Estado não encontrado para a sigla: {sigla_estado.strip()}")

    # Salvar as mudanças e fechar a conexão
    conn.commit()
    conn.close()

    print("Dados de doadores inseridos com sucesso!")


def inserir_arrecadacao(valor):
    # Conecta ao banco de dados
    conn = sqlite3.connect(NAME_BD)
    cursor = conn.cursor()
    
    # Obtém a data e hora no formato desejado
    data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # DD/MM/YYYY HH:MM:SS

    cursor.execute('''
                INSERT INTO ARRECADACAO_ARENA (valor, data)
                VALUES (?, ?)
            ''', (valor, data_atual))  # Inserindo valor fictício (0.0) e estado 0

    conn.commit()
    conn.close()

def converter_para_float(valor_str):
    # Remove "R$" e espaços extras
    valor_str = valor_str.replace("R$", "").strip()
    
    # Remove separadores de milhar (pontos) e substitui vírgula por ponto
    valor_str = valor_str.replace(".", "").replace(",", ".")

    # Converte para float
    return float(valor_str)

import sqlite3


def buscar_ultimas_arrecadacoes(limit=10):
    conn = sqlite3.connect(NAME_BD)
    cursor = conn.cursor()
    
    cursor.execute(f"""
        SELECT valor, data FROM ARRECADACAO_ARENA 
        ORDER BY data DESC 
        LIMIT {limit}
    """)  # Ordena pela data mais recente e pega os últimos 10 registros

    ultimas_arrecadacoes = cursor.fetchall()
    conn.close()

    print(f"📊 Últimas {limit} arrecadações:")
    for arrecadacao in ultimas_arrecadacoes:
        print(f"Data: {arrecadacao[1]} | 💰 Valor: R$ {arrecadacao[0]:,.2f}")


if __name__ == "__main__":
    criar_tabelas()
    inserir_estados()
    iniciar_valor_total_estados_zero()
    inserir_top_100_doadores()