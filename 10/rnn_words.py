# рекурентная сеть прогнозирование следующего слова по трем предыдущим
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np

from tensorflow.keras.layers import Dense, SimpleRNN, Input, Embedding, Dropout, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer, text_to_word_sequence
from tensorflow.keras.utils import to_categorical

with open(r'C:\Users\User\OneDrive\Рабочий стол\Programs_for_UDA\10\cat.txt', 'r', encoding='utf-8') as f:  # файл
    texts = f.read()
    texts = texts.replace('\ufeff', '')  # убираем первый невидимый символ

maxWordsCount = 1500
tokenizer = Tokenizer(num_words=maxWordsCount, filters='!–"—#$%&amp;()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r«»',
                      lower=True, split=' ', char_level=False)
tokenizer.fit_on_texts([texts])

dist = list(tokenizer.word_counts.items())
print(dist[:40])

data = tokenizer.texts_to_sequences([texts])
# res = to_categorical(data[0], num_classes=maxWordsCount)
# print(res.shape)
res = np.array( data[0] )

inp_words = 3
n = res.shape[0] - inp_words

X = np.array([res[i:i + inp_words] for i in range(n)])
Y = to_categorical(res[inp_words:], num_classes=maxWordsCount+1)

model = Sequential()
# model.add(Embedding(maxWordsCount, 256, input_length = inp_words)) не работает
model.add(Input(shape=(inp_words, )))
model.add(Embedding(maxWordsCount+1, 300))
# model.add(SimpleRNN(128, activation='tanh'))
model.add(LSTM(256, return_sequences=False, dropout=0.2))  # LSTM вместо SimpleRNN
# model.add(LSTM(128, return_sequences=True, dropout=0.2))
model.add(Dense(maxWordsCount+1, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

history = model.fit(X, Y, batch_size=32, epochs=60, verbose=False)

print("\n=== Метрики ===")
test_loss, test_accuracy = model.evaluate(X, Y, verbose=False)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")

def calculate_perplexity(model, X, Y):
    predictions = model.predict(X, verbose=False)
    cross_entropy = -np.sum(Y * np.log(predictions + 1e-8)) / len(X)
    perplexity = np.exp(cross_entropy)
    return perplexity

perplexity = calculate_perplexity(model, X, Y)
print(f"Perplexity: {perplexity:.2f}")


def buildPhrase(texts, str_len=20):
    res = texts
    data = tokenizer.texts_to_sequences([texts])[0]
    for i in range(str_len):
        # x = to_categorical(data[i: i + inp_words], num_classes=maxWordsCount)  # преобразуем в One-Hot-encoding
        # inp = x.reshape(1, inp_words, maxWordsCount)
        x = data[i: i + inp_words]
        inp = np.expand_dims(x, axis=0)

        pred = model.predict(inp, verbose=False)
        indx = pred.argmax(axis=1)[0]
        data.append(indx)

    # Проверка существования слова
        if indx in tokenizer.index_word and indx <= maxWordsCount:
            res += " " + tokenizer.index_word[indx]
        else:
            res += " <UNKNOWN>"
            break

    return res


# res = buildPhrase("добрый роман для")
# print(res)
# print("*** * ** * ***** ***** ")
# res = buildPhrase("рукой престрастной так")
# print(res)
# print("*** * ** * ***** ***** ")
# res = buildPhrase("прими святой живой")
# print(res)
# print("*** * ** * ***** ***** ")
# res = buildPhrase("горый ответ тебе")
# print(res)

def generate_valid_phrases(tokenizer, maxWordsCount, num_phrases=5, words_per_phrase=3):
    """
    Генерирует словосочетания из слов, которые точно есть в словаре
    """
    valid_words = []
    for i in range(1, maxWordsCount + 1):
        valid_words.append(tokenizer.index_word[i])
    
    phrases = []
    for i in range(num_phrases):
        selected_words = np.random.choice(valid_words, size=words_per_phrase, replace=False)
        phrase = " ".join(selected_words)
        phrases.append(phrase)
    
    return phrases

# valid_phrases = generate_valid_phrases(tokenizer, maxWordsCount, 10)
valid_phrases = ["прочь ученый кот", "хитрец думая пойти", "с пустяка начинаются", "кот в сапогах"]
for i, phrase in enumerate(valid_phrases, 1):
    print(f"\n{i}. Фраза: '{phrase}'")
    result = buildPhrase(phrase, str_len=20)
    print(f"Результат: {result}")

