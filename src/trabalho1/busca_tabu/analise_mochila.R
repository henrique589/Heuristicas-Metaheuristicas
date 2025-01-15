#install.packages("jsonlite")
#install.packages("ggplot2")

setwd('C:\\Users\\User\\OneDrive\\Documentos\\7°Periodo-UFSJ\\Heuristicas-Metaheuristicas\\src\\trabalho1\\busca_tabu')

#Carregando as bibliotecas
library(jsonlite)
library(ggplot2)

#Carregando os dados
resultados = fromJSON("resultados_mochila.json")
print(resultados)
write.csv(resultados, "tabela_resultados_mochila.csv", row.names = FALSE)
