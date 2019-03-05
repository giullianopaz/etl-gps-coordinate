import pandas as pd

import extract as exct
import transform as trm
from load import Model

class ETL:
    '''
    Classe responsável por fazer a interface entre a Main e os demais
    subsistemas, como Extract, Transform e Load
    '''
    def __init__(self):
        self.data = None
        self.model = Model()

    def extract_points_from_file(self, files_path):
        '''
        Método para pegar coordenadas dos arquivos de texto

        Args:
            files_path : str
                Diretório onde encontram-se os arquivos com os dados dos Pontos
        '''
        self.data = exct.get_points(files_path)

    def extract_data_from_API(self):
        '''
        Método para pegar dados das coordenadas da API de Mapas

        Args:
            data : gererator | list
                Lista de coordenadas limpas (tratadas)
        '''
        self.data = exct.get_data_points(self.data)

    def clear_points(self):
        '''
        Método para tratar coordenadas dos arquivos de texto
        '''
        self.data = trm.clear_points(self.data)

    def connect(self, host, user, password, database):
        '''
        Método para conectar-se à Base de Dados

        Args:
            host : str
                Nome do host da Base de Dados

            user : str
                Usuário da Base de Dados

            password : str
                Senha da Base de Dados

            database : str
                Nome do Database a ser utilizado
        '''
        self.model.connect(host, user, password, database)

    def close(self):
        '''
        Método para fechar a conexão com a Base de Dados
        '''
        self.model.close()

    def _commit(self):
        '''
        Método para escrever os dados na Base de Dados
        '''
        self.model.commit()

    def create_tables(self):
        '''
        Método para criar as tabelas
        '''
        self.model.create_tables()

    def drop_tables(self, tables):
        '''
        Método para deletar as tabelas da Base de Dados

        Args:
            tables : list
                Lista de nomes das tabelas a serem deletadas da Base de Dados
        '''
        tables = [tables] if not isinstance(tables, list) else tables
        for table in tables:
            self.model.drop_table(table)

    def load_data(self, commit=1):
        '''
        Método para inserir dados na Base de Dados

        Args:
            commit : int
                Este valor refere-se à frequência que os dados serão escritos
                na Base de Dados. 
        '''
        i = 0
        for data in self.data:
            # Se há informação sobre País
            if data.country:
                country_ID = self.model.insert(table='Country',
                                            columns='countryName',
                                            values=data.country.lower())
            # Se há informação sobre Estado
            if data.state and country_ID:
                state_ID = self.model.insert(table='State',
                                            columns=['stateUF',
                                                    'countryID'],
                                            values=[data.state.lower(),
                                                    country_ID])
            # Se há informação sobre Cidade
            if data.city and state_ID:
                city_ID = self.model.insert(table='City',
                                            columns=['cityName',
                                                    'stateID'],
                                            values=[data.city.lower(),
                                                    state_ID])
            # Se há informação sobre Bairro
            if data.suburb and city_ID:
                suburb_ID = self.model.insert(table='Suburb',
                                            columns=['suburbName',
                                                      'cityID'],
                                            values=[data.suburb.lower(),
                                                    city_ID])
            point_columns = []
            point_values = []
            # Se há informação sobre Latitude
            if data.lat:
                point_columns.append('pointLAT')
                point_values.append(data.lat)
            # Se há informação sobre Longitude
            if data.lng:
                point_columns.append('pointLNG')
                point_values.append(data.lng)
            # Se há informação sobre Rua
            if data.street:
                point_columns.append('pointStreetName')
                point_values.append(data.street.lower())
            # Se há informação sobre Número da Residência
            if data.housenumber:
                point_columns.append('pointHouseNumber')
                point_values.append(data.housenumber.lower())
            # Se há informação sobre CEP
            if data.postal:
                point_columns.append('pointPostalCode')
                point_values.append(data.postal.lower())
            # Dados que não contém a informação sobre bairro (Suburb) não são armazenados
            if data.suburb and len(point_columns) > 0 and len(point_values) > 0:
                point_columns.append('suburbID')
                point_values.append(suburb_ID)
                point_ID = self.model.insert(table='Point',
                                            columns=point_columns,
                                            values=point_values)

                print('\nID: {}'.format(point_ID))
                print(data)
            
            # Contador para a frequẽncia de commits
            i += 1
            if i == commit:
                i = 0
                self._commit()

    def show(self, max_rows=None, max_columns=None):
        '''
        Método para mostrar a tabela de dados

        Args:
            max_rows : int
                Quantidade de linhas da tabela a serem mostradas
            
            max_columns : int
                Quantidade de colunas da tabela a serem mostradas 
        '''
        print("\nData Visualization\n")
        data = self.model.select_all()
        if not data:
            print("\nNenhum dado a ser mostrado!\nCrie as tabelas e carregue os dados primeiro.\n")
            return

        # Torna os dados mais apresentáveis com os métodos title() e upper()
        data = [list(row) for row in data]
        for row in data:
            for j, elem in enumerate(row):
                if isinstance(elem, str):
                    row[j] = elem.title()
                    if len(elem) == 2:
                        row[j] = elem.upper()
        # Cria DataFrame de dados
        df = pd.DataFrame(data=list(data),
                        columns=['Latitude', 'Longitude', 'Rua', 'Número',
                                'Bairro', 'Cidade', 'CEP', 'Estado', 'País'])
        # Mostra DataFrame
        with pd.option_context('display.max_rows', max_rows, 'display.max_columns', max_columns):
            print(df)