#подсчет статистики - сколько раз встречаются разные словоформы в тексте
#текст должен быть в файле ff.txt
import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist

text_file_path = "ff.txt"
with open(text_file_path, 'r', encoding="utf-8") as reader:
    text = reader.read()

text_tokens = word_tokenize(text) # получили список слов (токенов)
text = nltk.Text(text_tokens)
# Для применения инструментов частотного анализа библиотеки NLTK
# необходимо список токенов преобразовать к классу Text,
# который входит в эту библиотеку
print(text)
# Для подсчёта статистики распределения частот токенов в тексте
# применяется класс FreqDist (frequency distributions):
fdist = FreqDist(text)
print(fdist) #  сколько оригинальных слов (samples) и сколько всего (utcomes)
print(fdist.most_common(15)) # заданное количество самых частых

