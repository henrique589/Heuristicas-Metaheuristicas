#install.packages("jsonlite")
#install.packages("ggplot2")

setwd('C:\\Users\\inffo\\Documents\\7ªPeriodo\\H&M\\HM\\src\\trabalho1\\grasp')

#Carregando as bibliotecas
library(jsonlite)
library(ggplot2)

#Carregando os dados
resultados = fromJSON("resultados_tsp.json")
print(resultados)
write.csv(resultados, "tabela_resultados_tsp.csv", row.names = FALSE)
