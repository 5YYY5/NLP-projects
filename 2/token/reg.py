from nltk.tokenize import regexp_tokenize
# надо раскомментировать одну (ОДНУ) из строчек
s = "Good muffins cost $3.88\nin New York.  Please buy me\ntwo of them.\n\nThanks."
# print(regexp_tokenize (s,  '\s', gaps=True))  # разделение по пробелу (типа на слова)
# print(regexp_tokenize (s,  '[,\.\?!"]\s*', gaps=True)) # типа на предложения
# print(regexp_tokenize (s,  '[A-Z]\w+', gaps=False)) # Выделение слов с большой буквы 
