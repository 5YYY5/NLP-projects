file = open('C:/Users/User/OneDrive/Рабочий стол/Programs_for_UDA/4/t2.txt', 'r', encoding='utf-8')
text = file.read()
file.close()

text = text.lower()
text = text.replace('ё', 'е')

all_letters = ""
for char in text:
    if (char >= 'а' and char <= 'я') or (char >= 'a' and char <= 'z'):
        all_letters += char

total = len(all_letters)
print("Всего букв:", total)
print()

results = []
alpha = "абвгдежзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz"
for letter in alpha:
    count = 0
    for char in all_letters:
        if char == letter:
            count += 1
    
    if count > 0:
        chastota = count / total
        if letter >= 'a' and letter <= 'z':
            lang = "латинская"
        else:
            lang = "русская"
        results.append((count, letter, chastota, lang))

n = len(results)
for i in range(n):
    for j in range(0, n-i-1):
        if results[j][0] < results[j+1][0]:
            results[j], results[j+1] = results[j+1], results[j]


number = 1
for count, letter, chastota, lang in results:
    print(number, ". ", letter, " – ", count, " | ", round(chastota, 4), " | ", lang, sep="")
    number += 1

print("\nДиаграмма:")
for count, letter, chastota, lang in results:
    stars = ""
    for i in range(count):
        stars += "*"
    print(letter,": ", stars, sep="")