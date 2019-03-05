import geocoder
from os import walk
from os.path import isfile, isdir
from collections import namedtuple

def _get_files(files_path):
    '''
    Método auxiliar para pegar os nomes dos arquivos que contém os dados de coordenadas

    Args:
        files_path : str
            Diretório onde encontram-se os arquivos com os dados dos Pontos

    Returns:
        str | generator
            Um gerador contendo os nomes dos arquivos
    '''
    for files_path, _, files in walk(files_path):
        return (str(files_path) + '/' + elem.strip() for elem in files)


def get_points(files_path):
    '''
    Método para ler as coordenadas dos arquivos de dados

    Args:
        files : str
            Diretório onde encontram-se os arquivos com os dados dos Pontos

    Returns:
        str | generator
            Um gerador contendo a lista de coordenadas
    '''
    points = []

    assert isdir(files_path) # Testa se o diretório existe

    for file_name in _get_files(files_path):

        assert isfile(file_name) # Testa se o arquivo existe

        with open(file_name, 'r') as file:
            points += file.readlines()
    # Retorna generator
    return (line for line in points)


'''
Namedtuples utilizam menos memória do que um objeto normal
pois não armazenam seus atributos em um dicionário.
'''
Point = namedtuple('Point', 'lat lng street housenumber suburb city postal state country')

def get_data_points(points):
    '''
    Método usado para acessar a API OpenStreetMap

    Args:
        lat : float
            Latitude do ponto
        lng : float
            Longitude do ponto

    Returns:
        Point : generator
            Um gerador da namedtuple contendo os dados dos pontos obtidos através da API

    Raises:
        DataError
            Caso não seja possível obter os dados
    '''
    for point in points:        
        try:
            # Pega dados da API
            data = geocoder.osm(point, method='reverse').json
        except:
            raise Exception("teste")
        else:
            # Retorna generators de Point
            yield Point(lat=data.get('lat', None),
                    lng=data.get('lng', None),
                    street=data.get('street', None),
                    housenumber=data.get('housenumber', None),
                    suburb=data.get('suburb', None),
                    city=data.get('city', None),
                    postal=data.get('postal', None),
                    state=data.get('state', None),
                    country=data.get('country', None))