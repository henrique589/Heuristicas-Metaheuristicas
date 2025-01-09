#install.packages("jsonlite")
#install.packages("ggplot2")

setwd('C:\\Users\\inffo\\Documents\\7ªPeriodo\\H&M\\HM\\src\\trabalho1\\grasp')

#Carregando as bibliotecas
library(jsonlite)
library(ggplot2)

#Carregando os dados
resultados = fromJSON("resultados_tsp.json")
print(resultados)

#Tabelando os resultados
maior_valor = max(resultados$melhor_custo)
menor_valor = min(resultados$melhor_custo)
media = mean(resultados$melhor_custo)

resultados$maior_valor = maior_valor
resultados$menor_valor = menor_valor
resultados$media = media

print(resultados)
write.csv(resultados, "tabela_resultados_tsp.csv", row.names = FALSE)

#Análise dos resultados do melhor custo de cada execução
ggplot(resultados, aes(x = execucao, y = melhor_custo)) + 
  geom_line(color = "lightgreen") +
  geom_point(color = "orange") +
  labs(title = "Melhor Custo por Execução", x = "Execução", y = "Melhor Custo") +
  scale_x_continuous(breaks = seq(min(resultados$execucao), max(resultados$execucao), by = 1))
theme_minimal()

#Análise dos resultados do tempo de cada execução
ggplot(resultados, aes(x = execucao, y = tempo_execucao)) +
  geom_line(color = "blue") +
  geom_point(color = "red") +
  labs(title = "Tempo de Execução por Execução", x = "Execução", y = "Tempo de Execução (s)") +
  theme_minimal()
