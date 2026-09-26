import tensorflow_datasets as tfds
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.layers import Dense

# Датасет для букв
ds_train, ds_test = tfds.load('emnist/letters',
                              split=['train', 'test'],
                              as_supervised=True,
                              shuffle_files=True)

x_train = []
y_train = []
x_test = []
y_test = []

for image, label in ds_train:
    x_train.append(image.numpy())
    y_train.append(label.numpy())

for image, label in ds_test:
    x_test.append(image.numpy())
    y_test.append(label.numpy())

x_train = np.array(x_train)
y_train = np.array(y_train)
x_test = np.array(x_test)
y_test = np.array(y_test)

# далее отображение первых 25 изображений из обучающей выборки - можно убрать
# plt.figure(figsize=(10,5))
# for i in range(25):
#     plt.subplot(5,5,i+1)
#     plt.xticks([])
#     plt.yticks([])
#     plt.imshow(x_train[100+i], cmap=plt.cm.binary)
 
# plt.show()

# Узнаем размеры данных и минимальную метку
# print(np.min(y_train)) #1
# print(len(y_train)) #88800
# print(len(y_test)) #14800

# Преобразуем метки
y_train = y_train - 1
y_test = y_test - 1

# это самое главное, это сеть. здесь можно менять
model = keras.Sequential([
    keras.layers.Flatten (input_shape=(28, 28, 1)), # потому что размер изображения 28*28
    Dense(260, activation='relu'),
    Dense(50, activation='relu'),
    Dense(26, activation='softmax')]) # у нас 26 букв
# print(model.summary())     # вывод структуры НС в консоль
x_train = x_train / 255 # нормализация
x_test = x_test / 255
y_train_cat = keras.utils.to_categorical(y_train, 26) # приведение к вектору из 0 и 1 (26 - размерность)
y_test_cat = keras.utils.to_categorical(y_test, 26) # также 26 букв
model.compile(optimizer='adam',
loss='categorical_crossentropy',
metrics=['accuracy','precision','recall'])
model.fit(x_train, y_train_cat, batch_size=32, epochs=10, validation_split=0.2,  verbose=False) #обучение
# print('*******   loss и accuracy  на тестовом наборе   ***********')

# model.evaluate(x_test, y_test_cat) # Метод evaluate прогоняет все тестовое множество и вычисляет значение критерия качества и метрики
loss, accuracy, precision, recall = model.evaluate(x_test, y_test_cat, verbose=0) # Добавили метрик
f1 = 2 * precision * recall / (precision + recall)
print("Результаты тестирования:")
print(f"Потери:      {loss:.4f}")
print(f"Точность:    {accuracy:.4f}")
print(f"Precision:   {precision:.4f}") 
print(f"Recall:      {recall:.4f}")
print(f"F1-Score:    {f1:.4f}")
# print('*********    *****************')
# print ('проверка правильности некоторой буквы')
# n = 5  # изображение - это номер в наборе данных
# x = np.expand_dims(x_test[n], axis=0)
# # выведем рукописную букву с заданным номером, полученное сетью значение - в виде числа и в виде вектора
# res = model.predict(x)
# print ('печать выходного вектора для', chr(97+y_test[n]))
# print( res  )
# print 
# print( chr(97+np.argmax(res)) , '  - такая буква должна быть на рисунке. Верно?')
# plt.imshow(x_test[n], cmap=plt.cm.binary)
# plt.show()
# выделение неверных результатов
pred = model.predict(x_test)
pred = np.argmax(pred, axis=1) # массив предсказанных результатов (на тестовом наборе)

# print('вывод некоторых ошибочных некоторых результатов')
# print('смотрим, правильные ли ошибочные картинки, хорошо ли нарисованы')

er=0
arr_er=np.zeros((26, 2), dtype=int)
for i in range(len(y_test)): # проверяем тестовой набор
     arr_er[y_test[i]][1]+=1
     if pred[i]!=y_test[i]:
        arr_er[y_test[i]][0]+=1
        er=er+1 # считаем ошибки
        #  if er>10 and er<16: # смотрим 5 картинок неверно определенных сетью
        #      print("Значение сети: ", chr(97+y_test[i]), ' предсказано   ', chr(97+pred[i]) )
        #      plt.imshow(x_test[i], cmap=plt.cm.binary)
        #      plt.show()
        
print ('k-vo  error ', er)

letter_stats = []
for i in range(26):
    total_samples = arr_er[i][1]
    errors = arr_er[i][0]
    accuracy = (total_samples - errors) / total_samples if total_samples > 0 else 0
    letter_stats.append((chr(65 + i), errors, total_samples, accuracy))

letter_stats.sort(key=lambda x: x[3])

for letter, errors, total, accuracy in letter_stats:
    print(f"  {letter}   |   {errors:3d}/{total:3d}   |   {accuracy:.4f} ({accuracy*100:.1f}%)")

