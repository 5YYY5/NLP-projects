import nltk
nf ='C:/Users/User/OneDrive/Рабочий стол/Programs_for_UDA/token/test_tokrus.txt'   #= input('имя файла  ')
f=open(nf,"r")
sentences = nltk.sent_tokenize(f.read()  , language="russian")
# для английского текста указывать язык не надо (по умолчанию), для других - обязательно
i=1
for sentence in sentences: 
    print(i, '  ',sentence)
    print()
    i+=1

f.close()