
# Desenvolvimento de Rotinas ETL Utilizando Python

Projeto ETL para obter dados de localização.

Utilizando arquivos contendo uma lista de coordenadas geográficas obtidas a partir do GPS de dispositivos móveis, foi possível obter mais informações sobre os locais, como Rua, Número, Bairro, Cidade, CEP, Estado e País.

Os dados foram expostos à rotinas ETL (Extract, Transform e Load), 

Este projeto usou FAÇADE como Padrão de Projeto Estrutural.

Neste projeto a classe `ETL` age como a camada intermediária entre a `main.py`
e os demais subsistemas, como `extract.py`, `transform.py` e `load.py`.

- **settings.py**: arquivo de configuração. Seus valores podem ser mudados diretamente ou por intermédio de argumentos;

- **main.py**: arquivo principal responsável por receber as configurações, argumentos e executar as ações;

- **etl.py**: arquivo que contém a classe ETL, responsável por fazer a interface entre a `main` e os subsistemas responsáveis por executar as rotinas ETL;

- **extract.py**: scripts responsáveis por realizar a extração de dados de arquivos e API;

- **transform.py**: scripts responsáveis por realizar a normalização, transformação e formatação dos dados brutos obtidos através de arquivos e API;

- **load.py**: arquivos que contém a classe Model responsável por se comunicar com o SGBD, neste caso, MySQL;

- **requirements.txt**: arquivo com a lista de módulos necessários para a execução deste programa;
    $ pip freeze > requirements.txt

- **sql/**: diretório com scripts SQL para criação, deleção e seleção;

- **data_points/**: diretório que contém os arquivos de texto contendo as coordenadas brutas (não tratadas).


## Como executar:

Para executar o ETL é preciso ter o MySQL instalado, além dos módulos em `requeriments.txt`. Não esqueça de dar uma olhada em `settings.py`.

### 1 - Instalar MySQL
    $ sudo apt install mysql-server mysql-client
    $ sudo apt install libmysqlclient-dev

### 2 - Instalar módulos necessários em requeriments.txt
    $ pip install -r requirements.txt

### 3 - Criar Base de Dados e as Tabelas

Você pode fazer isso manualmente ou utilizar os arquivos no diretórios `sql/`.

Infelizmente não é possível criar o `database` por intermédio do `Python` porque é necessário o `database` já estar criado para realizar a conexão.

Assim que o `database` estiver criado, a criação das tabelas, inserções e seleções poderão ser feitas utilizando a aplicação.

    Criação das Tabelas
    $ python3 main.py -ct 1
    ou
    $ python3 main.py --createtables 1

### Execução do ETL

Assim que o `database` e as tabelas estiverem criadas, o ETL pode ser executado.

    Execução do ETL
    $ python3 main.py -ld 1
    ou
    $ python3 main.py --loaddata 1

### Visualização da Tabela de Dados

Para visualizar a tabela de dados, basta executar:

    $ python3 main.py -v 1
    ou
    $ python3 main.py --visualize 1

Você também pode limitar a quantidade de linhas e colunas a serem retornadas.

    $ python3 main.py -v 1 -mr 10 -mc 10
    ou
    $ python3 main.py --visualize 1 --maxrows 10 --maxcolumns 10
    
Você pode executar todo o processo de uma só vez.

    $ python3 main.py -H localhost -U root -P toor -D etl -p data_points -dt 1 -ct 1 -ld 1 -v 1 -mr 10 -mc 10 -c 100
    ou
    $ python3 main.py --host localhost --user root --password toor --database etl --path data_points --droptables 1 --createtables 1 --loaddata 1 --visualize 1 --maxrows 10 --maxcolumns 10 --commit 100
