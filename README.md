# Script_Socioambiental_BBA

Problema: Acesso remoto a uma única maquina com programa de Feature Manipulation Engine (FME) acaba que impede o fluxo de trabalho, acumulando varias analises sócioambientais para um único analista

Solução: Transformar o fluxo Socioambiental do FME para rodar no Qgis em python. A saída do script é um arquivo CSV.

Explicação: primeiro solicito que o usuário crie ou abra um projeto em um determinado caminho. Feito isso, é necessário conectar aos bancos de dados PostGIS, adicionar como camadas no projeto. Também verifico se as mesmas já existem para não adicona-lás todo o tempo. Com as camadas adicionadas, precisamos adicionar o poligono (shapefile) que queremos analisar, pode ser mais de um. Será criado um buffer de raio de 5 km a partir do limite do poligono e outro buffer de raio de 50 m. Em seguida verificar se existe sobreposição do poligono, buffer de 5 km e de 50 m com alguma geometria das camadas PostGIS, salvando o resultado no csv.
