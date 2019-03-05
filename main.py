'''
Desafio realizado para a 4all

Teste para avaliação de competências técnicas necessárias
para o desenvolvimento de rotinas ETL utilizando Python como base.

Este projeto usou FAÇADE como Padrão de Projeto Estrutural.
Neste projeto a classe ETL age como a camada intermediária entre a main.py
e os demais subsistemas, como extract, transform e load.

Exemplos de execução:

1 - Deleta tabelas existentes, cria as tabelas novamente, executa o ETL
    e mostra a tabela de resultados

        $ python3 main.py -dt 1 -ct 1 -ld 1 -v 1

2 - Configura data_points como o diretório onde os dados de coordenadas estão,
configura o host como localhost, a senha como 1234 e o database etl

        $ python3 main.py -p data_points -H localhost -P 12345 -D etl

3 - Configura para mostrar apenas 10 linhas e 10 colunas do DataFrame
e configura para realizar a escrita na Base de Dados a cada 10 dados inseridos.

        $ python3 main.py -mr 10 -mc 10 -c 10
'''
import sys
import argparse

from etl import ETL
from settings import FILE_SETTINGS, DATABASE_SETTINGS, VISUALIZATION_SETTINGS

__author__ = "Giulliano Paz"
__email__ = "workgiullianopaz@gmail.com"

# Tratamento de argumentos
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', type=str, help='Diretório com os arquivos de coordenadas')

parser.add_argument('-H', '--host', type=str, help='Host da Base de Dados')
parser.add_argument('-U', '--user', type=str, help='Usuário da Base de Dados')
parser.add_argument('-P', '--password', type=str, help='Senha da Base de Dados')
parser.add_argument('-D', '--database', type=str, help='Database a ser utilizado')
parser.add_argument('-dt', '--droptables', type=int, help='[0/1] Flag para deleção das tabelas existentes')
parser.add_argument('-ct', '--createtables', type=int, help='[0/1] Flag para criar das tabelas')
parser.add_argument('-ld', '--loaddata', type=int, help='[0/1] Flag para realizar o ETL')
parser.add_argument('-c', '--commit', type=int, help='[int] Valor para intervalo de commits na Base de Dados')

parser.add_argument('-mr', '--maxrows', type=int, help='Quantidade de linhas a serem visualizadas')
parser.add_argument('-mc', '--maxcolumns', type=int, help='Quantidade de colunas a serem visualizadas')
parser.add_argument('-v', '--visualize', type=int, help='[0/1] Flag para visualizar os dados')

ARGS = parser.parse_args()

PATH = ARGS.path if ARGS.path else FILE_SETTINGS['path']

HOST = ARGS.host if ARGS.host else DATABASE_SETTINGS['host']
USER = ARGS.user if ARGS.user else DATABASE_SETTINGS['user']
PASSWORD = ARGS.password if ARGS.password else DATABASE_SETTINGS['password']
DATABASE = ARGS.database if ARGS.database else DATABASE_SETTINGS['database']
DROP_TABLES = ARGS.droptables if ARGS.droptables else DATABASE_SETTINGS['drop_tables']
CREATE_TABLES = ARGS.createtables if ARGS.createtables else DATABASE_SETTINGS['create_tables']
LOAD_DATA = ARGS.loaddata if ARGS.loaddata else DATABASE_SETTINGS['load_data']
COMMIT = ARGS.commit if ARGS.commit else DATABASE_SETTINGS['commit']

MAX_ROWS = ARGS.maxrows if ARGS.maxrows else VISUALIZATION_SETTINGS['max_rows']
MAX_COLUMNS = ARGS.maxcolumns if ARGS.maxcolumns else VISUALIZATION_SETTINGS['max_columns']
VISUALIZE = ARGS.visualize if ARGS.visualize else VISUALIZATION_SETTINGS['visualize']

etl = ETL()

# Pega coordenadas dos arquivos
etl.extract_points_from_file(PATH)

# Trata coordenadas 'sujas' obtidas através dos arquivos
etl.clear_points()

# Pega dados da API do OpenStreetView
etl.extract_data_from_API()

# Conecta à Base de Dados
etl.connect(HOST, USER, PASSWORD, DATABASE)

if DROP_TABLES:
    res = input("\nTem certeza que deseja deletar todas as tabelas de '{}'? [S/N]:".format(DATABASE))
    if res.upper() == 'S':
        etl.drop_tables(['Point', 'Suburb', 'City', 'State', 'Country'])

if CREATE_TABLES:
    etl.create_tables()

if LOAD_DATA:
    # Realiza ETL
    etl.load_data(commit=COMMIT)

if VISUALIZE:
    # Mostra tabela de dados
    etl.show(MAX_ROWS, MAX_COLUMNS)

# Fecha conexão com a Base de Dados
etl.close()