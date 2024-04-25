from qgis.core import *
import csv
from PyQt5.QtWidgets import QFileDialog, QApplication
import os
from shapely.wkb import loads
from shapely.geometry import mapping
from qgis.core.additions.edit import edit
from qgis.analysis import QgsNativeAlgorithms
import processing

# Criar projeto
projeto = QgsProject.instance()
projeto.write('C:/Users/joaquim.ornellas/Downloads/Projeto_Fluxo_BBA.qgs')
print(projeto.fileName())

# Ler o projeto
projeto.read('C:/Users/joaquim.ornellas/Downloads/Projeto_Fluxo_BBA.qgs')

# Solicita ao usuário que insira os caminhos dos arquivos shapefile (um por vez)
caminhos_shapefiles = []
while True:
    caminho_dialogo, _ = QFileDialog.getOpenFileName(None, "Selecionar Shapefile", "", "Shapefiles (*.shp);;Todos os arquivos (*)")
    if not caminho_dialogo:
        break
    caminhos_shapefiles.append(caminho_dialogo)

# Solicita ao usuário que insira o caminho para salvar o arquivo CSV
caminho_saida_dialogo, _ = QFileDialog.getSaveFileName(None, "Salvar CSV de Saída", "", "Arquivos CSV (*.csv)")
if not caminho_saida_dialogo:
    caminho_saida_csv = 'saida.csv'
else:
    caminho_saida_csv = caminho_saida_dialogo

# Nome das camadas
nome_icmbio = "icmbio_amb_csa_embargo_a"
nome_ibama = "ibama_amb_csa_area_embargada_a"
nome_assentamento = "lim_assentamentos_a"
nome_indigena = "funai_amb_csa_terra_indigena_a"
nome_sitio_arqueologico = 'br_iphan_csa_pontos_sitios_georreferenciados_20211227_p'

# Verifica se as camadas já existem no projeto
camada_icmbio_existente = QgsProject.instance().mapLayersByName(nome_icmbio)
camada_ibama_existente = QgsProject.instance().mapLayersByName(nome_ibama)
camada_assentamento_existente = QgsProject.instance().mapLayersByName(nome_assentamento)
camada_indigena_existente = QgsProject.instance().mapLayersByName(nome_indigena)
camada_sitio_arqueologico_existente = QgsProject.instance().mapLayersByName(nome_sitio_arqueologico)

# Definir as camadas fora do bloco if
camada_icmbio = None
camada_ibama = None
camada_assentamento = None
camada_indigena = None
camada_sitio_arqueologico = None

if not camada_icmbio_existente:
    # Se a camada ICMBio não existe, adicione-a ao projeto a partir da conexão PostGIS
    uri_icmbio = QgsDataSourceUri()
    uri_icmbio.setConnection("buclocal.agrotools.com.br", "6432", "buc", "joaquim_ornellas", "AJW3kVFNJtRWNR9")
    uri_icmbio.setDataSource("public", "icmbio_amb_csa_embargo_a", "geom")
    camada_icmbio = QgsVectorLayer(uri_icmbio.uri(), nome_icmbio, 'postgres')
    if camada_icmbio.isValid():
        projeto.addMapLayer(camada_icmbio)
        # Não redefine camada_icmbio aqui, pois ela já foi inicializada
    else:
        print(f"Erro ao adicionar camada ICMBio ao projeto.")
else:
    # Se a camada ICMBio já existe, busque a camada existente
    camada_icmbio = QgsProject.instance().mapLayersByName(nome_icmbio)[0]

if not camada_ibama_existente:
    # Se a camada ibama não existe, adicione-a ao projeto a partir da conexão PostGIS
    uri_ibama = QgsDataSourceUri()
    uri_ibama.setConnection("buclocal.agrotools.com.br", "6432", "buc", "joaquim_ornellas", "AJW3kVFNJtRWNR9")
    uri_ibama.setDataSource("public", "ibama_amb_csa_area_embagada_a", "geom")
    camada_ibama = QgsVectorLayer(uri_ibama.uri(), nome_ibama, 'postgres')
    if camada_ibama.isValid():
        projeto.addMapLayer(camada_ibama)
        # Não redefine camada_icmbio aqui, pois ela já foi inicializada
    else:
        print(f"Erro ao adicionar camada ibama ao projeto.")
else:
    # Se a camada ICMBio já existe, busque a camada existente
    camada_ibama = QgsProject.instance().mapLayersByName(nome_ibama)[0]

if not camada_assentamento_existente:
    # Se a camada assentamento não existe, adicione-a ao projeto a partir da conexão PostGIS
    uri_assentamento = QgsDataSourceUri()
    uri_assentamento.setConnection("buclocal.agrotools.com.br", "6432", "buc", "joaquim_ornellas", "AJW3kVFNJtRWNR9")
    uri_assentamento.setDataSource("public", "lim_assentamentos_a", "geom")
    camada_assentamento = QgsVectorLayer(uri_assentamento.uri(), nome_assentamento, 'postgres')
    if camada_assentamento.isValid():
        projeto.addMapLayer(camada_assentamento)
        # Não redefine camada_assentamento aqui, pois ela já foi inicializada
    else:
        print(f"Erro ao adicionar camada assentamento ao projeto.")
else:
    # Se a camada assentamento já existe, busque a camada existente
    camada_assentamento = QgsProject.instance().mapLayersByName(nome_assentamento)[0]

if not camada_indigena_existente:
    # Se a camada indigena não existe, adicione-a ao projeto a partir da conexão PostGIS
    uri_indigena = QgsDataSourceUri()
    uri_indigena.setConnection("buclocal.agrotools.com.br", "6432", "buc", "joaquim_ornellas", "AJW3kVFNJtRWNR9")
    uri_indigena.setDataSource("public", "funai_amb_csa_terra_indigena_a", "geom")
    camada_indigena = QgsVectorLayer(uri_indigena.uri(), nome_indigena, 'postgres')
    if camada_indigena.isValid():
        projeto.addMapLayer(camada_indigena)
        # Não redefine camada_indigena aqui, pois ela já foi inicializada
    else:
        print(f"Erro ao adicionar camada indigena ao projeto.")
else:
    # Se a camada indigena já existe, busque a camada existente
    camada_indigena = QgsProject.instance().mapLayersByName(nome_indigena)[0]

if not camada_sitio_arqueologico_existente:
    # Se a camada sitio_arqueologico não existe, adicione-a ao projeto a partir da conexão PostGIS
    uri_sitio_arqueologico = QgsDataSourceUri()
    uri_sitio_arqueologico.setConnection("buclocal.agrotools.com.br", "6432", "buc", "joaquim_ornellas", "AJW3kVFNJtRWNR9")
    uri_sitio_arqueologico.setDataSource("public", "br_iphan_csa_pontos_sitios_georreferenciados_20211227_p", "geom")
    camada_sitio_arqueologico = QgsVectorLayer(uri_sitio_arqueologico.uri(), nome_sitio_arqueologico, 'postgres')
    if camada_sitio_arqueologico.isValid():
        projeto.addMapLayer(camada_sitio_arqueologico)
        # Não redefine sitio_arqueologico aqui, pois ela já foi inicializada
    else:
        print(f"Erro ao adicionar camada sitio_arqueologico ao projeto.")
else:
    # Se a camada indigena já existe, busque a camada existente
    camada_sitio_arqueologico = QgsProject.instance().mapLayersByName(nome_sitio_arqueologico)[0]

# Cria um arquivo CSV para saída
arquivo_csv = caminho_saida_csv
with open(arquivo_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['matricula'] + ['embargo_icmbio_buffer', 'embargo_ibama_buffer', 'embargo_icmbio_limite_matricula', 'embargo_ibama_limite_matricula', 'embarco_assentamento_matricula', 'embargo_assentamento_buffer', 'embargo_indigena_matricula', 'embargo_indigena_buffer', 'embargos_sitio_arqueologico'])

    # Loop através dos caminhos dos shapefiles inseridos
    for caminho_shapefile in caminhos_shapefiles:
      # Nome para a camada no projeto QGIS
      nome_camada = f'Camada_{os.path.basename(caminho_shapefile)}'

      # Cria uma nova camada a partir do shapefile
      camada_shapefile = QgsVectorLayer(caminho_shapefile, nome_camada, 'ogr')

      # Verifica se a camada foi carregada com sucesso
      if not camada_shapefile.isValid():
        print(f"Erro ao carregar a camada shapefile '{caminho_shapefile}'!")
        continue

      # Obtém o valor do campo 'matricula' da camada shapefile
      for feature in camada_shapefile.getFeatures():
        matricula = feature['matricula']

        # Cria uma geometria de buffer de raio de 5 km a partir do limite geográfico da geometria da feature
        buffer_geometry = feature.geometry().buffer(5000, 5)
        # Cria uma geometria de buffer de raio de 50 m a partir do limite geográfico da geometria da feature
        buffer_geometry_assentamento = feature.geometry().buffer(50, 5)
        buffer_geometry_indigena = feature.geometry().buffer(50, 5)
        
        buffer_geometry_assentamento_diferenca = buffer_geometry_assentamento.difference(feature.geometry())
        buffer_geometry_indigena_diferenca = buffer_geometry_indigena.difference(feature.geometry())

        # Verifica a sobreposicao com as camadas ICMBio e IBAMA
        sobreposicao_icmbio_buffer = (buffer_geometry.intersects(icmbio_feature.geometry()) for icmbio_feature in camada_icmbio.getFeatures())
        sobreposicao_ibama_buffer = (buffer_geometry.intersects(ibama_feature.geometry()) for ibama_feature in camada_ibama.getFeatures())

        # Verifica a sobreposicao com as camadas ICMBio e IBAMA
        sobreposicao_icmbio = (feature.geometry().intersects(icmbio_feature.geometry()) for icmbio_feature in camada_icmbio.getFeatures())
        sobreposicao_ibama = (feature.geometry().intersects(ibama_feature.geometry()) for ibama_feature in camada_ibama.getFeatures())

        # Define os valores de Embargos com base na sobreposição
        embargos_icmbio_buffer = [2 if sobreposicao_icmbio_buffer else 1]
        embargos_ibama_buffer = [2 if sobreposicao_ibama_buffer else 1]
        embargos_icmbio_limite_matricula = [2 if sobreposicao_icmbio else 1]
        embargos_ibama_limite_matricula = [2 if sobreposicao_ibama else 1]

        # Verifica a sobreposição do buffer com as camadas assentamento
        # Define os valores de Embargos com base na sobreposição
        embargos_assentamento_limite_matricula = [3] if (feature.geometry().intersects(assentamento_feature.geometry()) for assentamento_feature in camada_assentamento.getFeatures()) else [1]
        embargos_assentamento_buffer = [2] if (buffer_geometry_assentamento_diferenca.intersects(assentamentos_feature.geometry()) for assentamentos_feature in camada_assentamento.getFeatures()) else [1]




        # Verifica a sobreposição do buffer com as camadas Indigena
        sobreposicao_indigena_matricula = (feature.geometry().intersects(indigena_feature.geometry()) for indigena_feature in camada_indigena.getFeatures())
        sobreposicao_indigena_buffer = (buffer_geometry_indigena_diferenca.intersects(indigenas_feature.geometry()) for indigenas_feature in camada_indigena.getFeatures())

        # Define os valores de Embargos com base na sobreposição
        embargos_indigena_matricula = [3 if sobreposicao_indigena_matricula else 1]
        embargos_indigena_buffer = [2 if sobreposicao_indigena_buffer else 1]

        # Verifica a sobreposicao com a camada de sitio arqueologicos
        sobreposicao_sitio_arqueologico = (feature.geometry().intersects(sitio_arqueologico_feature.geometry()) for sitio_arqueologico_feature in camada_sitio_arqueologico.getFeatures())

        # Define os valores de Embargos com base na sobreposição
        embargos_sitio_arqueologico = [2 if sobreposicao_sitio_arqueologico else 1]

        # Escreve no CSV
        writer.writerow([matricula] + embargos_icmbio_buffer + embargos_ibama_buffer + embargos_icmbio_limite_matricula + embargos_ibama_limite_matricula + embargos_assentamento_limite_matricula + embargos_assentamento_buffer + embargos_indigena_matricula + embargos_indigena_buffer + embargos_sitio_arqueologico)

        print(f"Arquivo CSV '{arquivo_csv}' criado com sucesso!")