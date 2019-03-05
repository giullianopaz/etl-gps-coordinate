# sudo apt install mysql-*
# sudo apt-get install libmysqlclient-dev
# pip install mysqlclient

from MySQLdb import Connect
from settings import DATABASE_SETTINGS

class Model:
    def __init__(self):
        self._conn = None
        self._cursor = None


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
        try:
            self._conn = Connect(host, user, password, database)
            self._cursor = self._conn.cursor()
        except Exception as e:
            raise e
        else:
            print("Connecting to '{}' database...".format(database))


    def close(self):
        '''
        Método para fechar a conexão com a Base de Dados
        '''
        try:
            self._conn.close()
        except Exception as e:
            raise e
        else:
            print("Closing connection...")


    def drop_table(self, table):
        '''
        Método para deletar uma tabela da Base de Dados

        Args:
            table : str
                Nome da tabela da Base de Dados
        '''
        try:
            self._cursor.execute(f"DROP TABLE {table};")
        except:
            pass
        else:
            print("Dropping '{}' table...".format(table))


    def commit(self):
        '''
        Método para escrever os dados na Base de Dados
        '''
        try:
            self._conn.commit()
        except Exception as e:
            raise e
        else:
            pass
        

    def select(self, columns=[], tables=[], value=None):
        '''
        Método para ler dados da Base de Dados

        Args:
            columns : list
                Lista de colunas a serem selecionadas

            tables : list
                Lista de tabelas

            value : str
                Valor a ser usado com a cláusula WHERE

        Returns
            n_rows : int
                Quantidade de linhas retornadas
        '''
        columns = [columns] if not isinstance(columns, list) else columns
        tables = [tables] if not isinstance(tables, list) else tables
        try:
            n_rows = self._cursor.execute('''SELECT {} FROM {} WHERE {}={};'''.format(
                ', '.join(map(lambda item: str(item), columns)),
                ', '.join(map(lambda item: str(item), tables)),
                columns[1],
                self._add_aspas(value)
            ))
        except Exception as e:
            raise e
        else:
            return n_rows


    def select_all(self):
        '''
        Método para ler todos os dados da Base de Dados

        Returns
            self._cursor.fetchall() : tuple
                Dados lidos da Base de Dados
        '''
        try:
            ret = self._cursor.execute(
                '''
                SELECT Point.pointLAT,
                       Point.pointLNG,
                       Point.pointStreetName,
                       Point.pointHouseNumber, 
                       Suburb.suburbName,
                       City.cityName,
                       Point.pointPostalCode,
                       State.stateUF,
                       Country.countryName 
                FROM Point
                LEFT JOIN Suburb
                ON Point.suburbID = Suburb.id
                LEFT JOIN City
                ON Suburb.cityID = City.id
                LEFT JOIN State
                ON City.stateID = State.id
                LEFT JOIN Country
                ON State.countryID = Country.id;
                '''
            )
        except:
            return None
        else:
            return self._cursor.fetchall()


    def _add_aspas(self, item):
        '''
        Método para formatar dados: se o item é uma String, 
        são adicionadas aspas ('') no item.

        Args:
            item : str | int | float
                Item a ser formatado

        Returns
            str(item) : str
                Item formatado
        '''
        if isinstance(item, str):
            return f"'{item.lower()}'"
        return str(item)

    
    def insert(self, table=None, columns=[], values=[]):
        '''
        Método para inserir dados na Base de Dados.
        Se a coluna for do tipo UNIQUE (countryName, stateUF, cityName, suburbName),
        é testado se o dado já existe na Base de Dados. Se já existir, o ID do dado
        é retornado; se o dado não existir, o dado é adicionado à Base de Dados e
        seu ID é retornado.

        Args:
            table : str
                Tabela onde os dados serão inseridos

            columns : list
                Lista de colunas

            values : list
                Lista de valores correspondentes às colunas

        Returns
            _id | self._cursor.lastrowid : int
                ID do dado adicionado ou do dado já existente
        '''
        columns = [columns] if not isinstance(columns, list) else columns
        values = [values] if not isinstance(values, list) else values

        # Busca o ID e o valor Único da tabela na base de dados para
        # verificar se já existe (countryName, stateUF, cityName, suburbName)
        n_rows = self.select(columns=['id', columns[0]], tables=table, value=values[0])
        
        if n_rows > 0: # Se o valor já existe, retorna o ID
            _data = self._cursor.fetchall()[0]
            
            # Testa se os valores são iguais
            _id, _value = _data
            if values[0] == _value:
                return _id
        
        # Se o valor não existe, insere ele
        try:
            ret = self._cursor.execute('''INSERT INTO {} ({}) VALUES ({});'''.format(
                table,
                ', '.join(map(lambda item: str(item), columns)), 
                ', '.join(map(lambda item: self._add_aspas(item), values))
            ))
        except Exception as e:
            raise e
        else:
            return self._cursor.lastrowid # retorna o ID da nova inserção


    def create_tables(self):
        '''
        Método para criar as tabelas
        '''
        try:
            self._cursor.execute(
            '''
                CREATE TABLE IF NOT EXISTS Country (
                    id INT NOT NULL AUTO_INCREMENT,
                    countryName VARCHAR(50) NOT NULL UNIQUE,
                    PRIMARY KEY (id)
                );
            '''
            )

            self._cursor.execute(
            '''
                CREATE TABLE IF NOT EXISTS State (
                    id INT NOT NULL AUTO_INCREMENT,
                    stateUF VARCHAR(5) NOT NULL UNIQUE,
                    countryID INT NOT NULL,
                    PRIMARY KEY (id),
                    FOREIGN KEY (countryID) REFERENCES Country(id)
                );
            '''
            )

            self._cursor.execute(
            '''
                CREATE TABLE IF NOT EXISTS City (
                    id INT NOT NULL AUTO_INCREMENT,
                    cityName VARCHAR(50) NOT NULL UNIQUE,
                    stateID INT NOT NULL,
                    PRIMARY KEY (id),
                    FOREIGN KEY (stateID) REFERENCES State(id)
                );
            '''
            )

            self._cursor.execute(
            '''
                CREATE TABLE IF NOT EXISTS Suburb (
                    id INT NOT NULL AUTO_INCREMENT,
                    suburbName VARCHAR(100) NOT NULL UNIQUE,
                    cityID INT NOT NULL,
                    PRIMARY KEY (id),
                    FOREIGN KEY (cityID) REFERENCES City(id)
                );
            '''
            )

            self._cursor.execute(
            '''
                CREATE TABLE IF NOT EXISTS Point (
                    id INT NOT NULL AUTO_INCREMENT,
                    pointLAT FLOAT,
                    pointLNG FLOAT,
                    pointStreetName VARCHAR(100),
                    pointHouseNumber VARCHAR(20),
                    pointPostalCode VARCHAR(20),
                    suburbID INT(11) NOT NULL,
                    PRIMARY KEY (id),
                    FOREIGN KEY (suburbID) REFERENCES Suburb(id)
                );
            '''
            )
        except Exception as e:
            raise e
        else:
            print("Creating tables...")