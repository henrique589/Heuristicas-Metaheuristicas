#install.packages("jsonlite")
#install.packages("ggplot2")

setwd('C:\\Users\\User\\OneDrive\\Documentos\\7°Periodo-UFSJ\\Heuristicas-Metaheuristicas\\src\\trabalho2\\ant_colony')

#Carregando as bibliotecas
library(jsonlite)
library(ggplot2)

#Carregando os dados
resultados = fromJSON("resultados_tsp.json")
print(resultados)

#Tabelando os resultados
maior_valor = max(resultados$melhor_distancia)
menor_valor = min(resultados$melhor_distancia)
media = mean(resultados$melhor_distancia)

resultados$maior_valor = maior_valor
resultados$menor_valor = menor_valor
resultados$media = media

print(resultados)
write.csv(resultados, "tabela_resultados_tsp.csv", row.names = FALSE)

#Análise dos resultados do melhor distância de cada execução
ggplot(resultados, aes(x = execucao, y = melhor_distancia)) + 
  geom_line(color = "blue") +
  geom_point(color = "orange") +
  labs(title = "Melhor Custo por Execução", x = "Execução", y = "Melhor Distancia") +
  scale_x_continuous(breaks = seq(min(resultados$execucao), max(resultados$execucao), by = 1))
theme_minimal()

#Análise dos resultados do tempo de cada execução
ggplot(resultados, aes(x = execucao, y = tempo_execucao)) +
  geom_line(color = "blue") +
  geom_point(color = "red") +
  labs(title = "Tempo de Execução por Execução", x = "Execução", y = "Tempo de Execução (s)") +
  theme_minimal()
