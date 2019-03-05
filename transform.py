from tqdm import tqdm

def clear_points(data_points):
    '''
    Método para limpar as coordenadas dos arquivos de dados.
    Apaga as linhas de Distâncias e as informações de Longitude
    e Latitude que estão inconsistentes.

    Args:
        data_points : generator | list
            Lista geradora de coordenadas

    Returns:
        generator | list | tuples
            Retorna um gerador de uma lista de coordenadas limpas (tratadas)
            

    '''
    # Filtra apenas as linhas com Latitude e Longitude
    data = list(filter(lambda line: line[0] == 'L', data_points))
    
    to_delete = []

    print('\nCleaning data')
    for i in tqdm(iterable=range(1, len(data)), ncols=90, unit=' lines'):
        previous = data[i-1]
        current = data[i]

        if previous[:2] == current[:2]: # Testa se está faltando informação
            if current[:2] == 'Lo': # Se estiver faltando a informação de Latitude
                to_delete.append(current) # Deleta a Longitude excedente
            elif current[:2] == 'La': # Se estiver faltando a informação de Longitude
                to_delete.append(previous) # Deleta a Latitude excedente
            else:
                raise Exception('Data Error: Inconsistent Data')

    # Deleta valores inconsistentes
    for line in to_delete:
        data.remove(line)
    # Retorna generator de coordenadas
    for i in range(1, len(data), 2):
         yield (float(data[i-1].split()[-1]), float(data[i].split()[-1]))