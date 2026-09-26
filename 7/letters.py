# распознавание букв
import tensorflow_datasets as tfds
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.layers import Dense

# Загрузка данных EMNIST для букв через tensorflow_datasets
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

# Преобразуем метки: в EMNIST буквы имеют метки 1-26, преобразуем в 0-25
y_train = y_train - 1
y_test = y_test - 1

# Словарь для преобразования цифр в буквы
label_map = 'abcdefghijklmnopqrstuvwxyz'

# далее отображение первых 25 изображений из обучающей выборки - можно убрать
plt.figure(figsize=(10,5))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(x_train[100+i], cmap=plt.cm.binary)
 
plt.show()

# это самое главное, это сеть. здесь можно менять
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)), # потому что размер изображения 28*28
    Dense(100, activation='relu'),
    Dense(26, activation='softmax')]) # 26 букв вместо 10 цифр

# print(model.summary())     # вывод структуры НС в консоль
x_train = x_train / 255 # нормализация
x_test = x_test / 255

# Изменяем на 26 классов для букв
y_train_cat = keras.utils.to_categorical(y_train, 26) # приведение к вектору из 0 и 1
y_test_cat = keras.utils.to_categorical(y_test, 26)

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train_cat, batch_size=32, epochs=10, validation_split=0.2, verbose=False) #обучение

print('*******   loss и accuracy  на тестовом наборе   ***********')
model.evaluate(x_test, y_test_cat) # Метод evaluate прогоняет все тестовое множество и вычисляет значение критерия качества и метрики
print('*********    *****************')

print('проверка правильности некоторой буквы')
n = 5  # изображение - это номер в наборе данных
x = np.expand_dims(x_test[n], axis=0)
# выведем рукописную букву с заданным номером, полученное сетью значение - в виде числа и в виде вектора
res = model.predict(x)
print('печать выходного вектора для', label_map[y_test[n]])  # Добавлено преобразование в букву
print(res)
print()
predicted_letter = label_map[np.argmax(res)]
true_letter = label_map[y_test[n]]
print(predicted_letter, '  - такая буква должна быть на рисунке. Верно?')
plt.imshow(x_test[n], cmap=plt.cm.binary)
plt.show()

# выделение неверных результатов
pred = model.predict(x_test)
pred = np.argmax(pred, axis=1) # массив предсказанных результатов (на тестовом наборе)

print('вывод некоторых ошибочных результатов')
print('смотрим, правильные ли ошибочные картинки, хорошо ли нарисованы')

er=0
for i in range(len(x_test)):  # Используем длину тестового набора
     if pred[i] != y_test[i]:
         er=er+1 # считаем ошибки
         if er>10 and er<16: # смотрим 5 картинок неверно определенных сетью
             true_letter = label_map[y_test[i]]  # Добавлено преобразование
             pred_letter = label_map[pred[i]]    # Добавлено преобразование
             print(f"Метка: {true_letter}, предсказано: {pred_letter}")
             plt.imshow(x_test[i], cmap=plt.cm.binary)
             plt.show()
        
print('k-vo error ', er)