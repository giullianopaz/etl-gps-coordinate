'''
Arquivo de configuração para auxiliar na execução desde ETL.

Em FILE_SETTINGS estão as configurações relativas aos arquivos de texto
contendo as coordenadas.

Em DATABASE_SETTINGS estão as configurações relativas à Base de Dados,
como dados de conexão e ações.

Em VISUALIZATION_SETTINGS estão as configurações relativas à visualização.

Os dados podem ser modificados aqui neste arquivo ou por parâmetros na hora
da execução.
'''

FILE_SETTINGS = {
    # Diretório onde encontram-se os arquivos com as coordenadas brutas
    'path' : 'data_points',
}

DATABASE_SETTINGS = {
    # Nome do host da Base de Dados
    'host'          :       'localhost',
    # Usuário da Base de Dados
    'user'          :       'root',
    # Senha do usuário da Base de Dados
    'password'      :       'toor',
    # Database criado para armazenar os dados
    'database'      :       'etl',
    # Flag para deletar ou não as tabelas existentes
    'drop_tables'   :       False,
    # Flag para criar as tabelas
    'create_tables' :       False,
    # Flag para executar o ETL e armazenar dados na Base de Dados
    'load_data'     :       False,
     # Valor de inserções até armazenar os dados definitivamente na Base de dados
    'commit'        :       50,
}

VISUALIZATION_SETTINGS = {
    # Flag para visualizar ou não os dados
    'visualize'     :       True,
    'max_rows'      :       None,
    'max_columns'   :       None,
}