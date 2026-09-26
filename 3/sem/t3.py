from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk import word_tokenize
from nltk.probability import FreqDist

# При повторном запуске программы две нижеследующие строчки надо закомментировать.
# Они нужны чтобы скачать список стоп-слов. После скачивания эти строки можно удалить. 
# import nltk
# nltk.download('stopwords')


# text = "Ах, как он любит ее, ах как сильно! Как он  хочет, чтобы она любила его."
f=open("C:/Users/User/OneDrive/Рабочий стол/Programs_for_UDA/lexan.txt","r",encoding="utf-8")
text=f.read()
f.close()
text=text.lower()
stop_words = stopwords.words('russian')# заносим стоп-слова в переменную
set_stop = set(stop_words) # создаем множество
# print('стоп-слова__________________')
# print(stop_words)

word_tokens = word_tokenize(text) #токенизация
    
filtered_sentence = [] # сюда будем отбирать слова очищенного текста
  
# for w in word_tokens: 
#     if w not in set_stop: 
#         filtered_sentence.append(w) 
# print('введенные токены текста___________')
# print(word_tokens)
# print('очищенный текст______________')
# print(filtered_sentence)
#теперь расширим список стоп-слов и проделаем то же самое
stop_words.extend(['!', ',', '.', 'ах', 'Ах', 'Как', '-', '(', ')',':',';','—','»','«'])
set_stop = set(stop_words)
filtered_sentence = [] # сюда будем отбирать слова очищенного текста
  
for w in word_tokens: 
    if w not in set_stop: 
        filtered_sentence.append(w)
print('очищенный текст______________')
print(filtered_sentence)


fdist = FreqDist(filtered_sentence)
print(fdist) #  сколько оригинальных слов (samples) и сколько всего (utcomes)
print(fdist.most_common(1)) # заданное количество самых частых
