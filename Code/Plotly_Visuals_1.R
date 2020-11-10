setwd("C:/Users/ear51/DAAN- Graduate School/DAAN 888 - Capstone Course/Project/Visuals")
rm(list=ls())

df<- read.csv("PBIX_Data_888.csv")

df$publish_time <- as.Date(df$publish_time, format = "%Y-%m-%d")
df$MonthYear <- format(df$publish_time,"%Y-%m")

library(gganimate)
library(ggplot2)
library(dplyr)
library(ggwordcloud)
library(tm)
library(plotly)
library(tidyverse)
library(tidytext)
library(wordcloud)
library(tidyr)
library(dplyr)

df2 <- df[with(df,order(publish_time)), ]
v1 <- df2 %>% mutate(number = row_number())
v2 <- v1 %>% group_by(labels_51, MonthYear, words_51) %>% summarise(sentiment = mean(sentimentPolarity))
v2 <- v2%>%
  unite(text, labels_51, words_51, sep = ": ", remove = FALSE)

w2 <- v1 %>% group_by(labels_102, MonthYear, words_102) %>% summarise(sentiment = mean(sentimentPolarity))
w2 <- w2%>%
  unite(text, labels_102, words_102, sep = ": ", remove = FALSE)


#### Animated Line plot for cumulative number of publications####
v4 <- ggplot(v1, aes(x = publish_time, y = number)) +
  geom_point() + geom_line() + 
  geom_text(aes(x = min(publish_time), y = min(number), label = as.factor(MonthYear)) , hjust=-2, vjust = -0.2, alpha = 0.5,  col = "gray", size = 20) +
  theme_minimal() +
  transition_reveal(publish_time) + 
  view_follow()

v5 <- ggplot(v1, aes(x = publish_time, y = number)) +
  geom_point() + geom_line() + 
  theme_minimal() +
  transition_reveal(publish_time)


#### Time vs. Clusters vs. Sentiment####

#v3 - 51 clusters' sentiment over timte
tx <- highlight_key(v2, ~labels_51, group = "Select one or more clusters:")
base <- plot_ly(tx, text = ~text,
                hovertemplate = paste(
                  "<b>Cluster: %{text}</b><br><br>",
                  "%{yaxis.title.text}: %{y:.4f}<br>",
                  "%{xaxis.title.text}: %{x}<br>",
                  "<extra></extra>"
                )) %>% 
  group_by(labels_51) %>% 
  layout(margin = list(b = 160), 
         xaxis = list(tickangle = 45, title = "Month and Year"), 
         yaxis = list(title = "Sentiment Rating"))
v3 <- base %>%
  group_by(labels_51) %>%
  add_lines(x = ~MonthYear, y = ~sentiment) %>%
  layout(xaxis = list(rangeslider = list(type = "date")))

highlight(
  v3, 
  on = "plotly_click", 
  selectize = TRUE, 
  dynamic = TRUE, 
  persistent = TRUE, 
  color = "purple"
)

#w3 - 102 clusters' sentiment over timte
tx <- highlight_key(w2, ~labels_102, group = "Select one or more clusters:")
base <- plot_ly(tx, text = ~text,
                hovertemplate = paste(
                  "<b>Cluster: %{text}</b><br><br>",
                  "%{yaxis.title.text}: %{y:.4f}<br>",
                  "%{xaxis.title.text}: %{x}<br>",
                  "<extra></extra>"
                )) %>% 
  group_by(labels_102) %>% 
  layout(margin = list(b = 160), 
         xaxis = list(tickangle = 45, title = "Month and Year"), 
         yaxis = list(title = "Sentiment Rating"))
w3 <- base %>%
  group_by(labels_102) %>%
  add_lines(x = ~MonthYear, y = ~sentiment) %>%
  layout(xaxis = list(rangeslider = list(type = "date")))

highlight(
  w3, 
  on = "plotly_click", 
  selectize = TRUE, 
  dynamic = TRUE, 
  persistent = TRUE, 
  color = "purple"
)
