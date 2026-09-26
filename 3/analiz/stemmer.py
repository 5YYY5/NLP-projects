#Работа стеммера Snowball

#Если есть проблемы, нужно указать вместо ... кодировку в явном виде 
#-*- coding: ... -*-

#Импортируем стеммер
from nltk.stem import SnowballStemmer

#Смотрим, какие языки стеммер поддерживает 
print(" ".join(SnowballStemmer.languages)) 

#Выбираем язык
stemmer = SnowballStemmer("russian") 

#Работаем со словом
print(stemmer.stem("столовая"))


 


