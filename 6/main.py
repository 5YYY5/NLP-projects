from numpy import exp, array, random, dot, shape
import numpy as np
# R4->R, x3 xor x4
# training_set_inputs = array([   [1, 0, 0, 0],
#                                 [0, 0, 1, 0],
#                                 [0, 1, 0, 1],
#                                 [1, 0, 1, 1],
#                                 [1, 1, 0, 1],
#                                 [0, 1, 1, 1]   ])
# training_set_outputs = array([[0, 1, 1, 0, 1, 0]]).T
training_set_inputs = array([   [1, 0, 0, 0],
                                [0, 0, 1, 0],
                                [0, 1, 0, 1],
                                [1, 0, 1, 1],
                                [1, 1, 0, 1],
                                [0, 1, 1, 1]   ])
training_set_outputs = array([[0, 1, 1, 0, 1, 0]]).T
# training_set_inputs = np.array([
#     [1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 1],
#     [1, 1, 0, 1], [0, 1, 1, 1], [0, 0, 0, 1], [1, 1, 1, 0],
#     [1, 0, 0, 1], [0, 1, 0, 0], [1, 1, 1, 1], [0, 0, 1, 1]
# ])
# training_set_outputs = np.array([[0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1]]).T
weights1 = array([[0.5], [0.5], [0.5], [0.5], [0.5]])
weights2 = array([[0.5], [0.5], [0.5]])

bias = 0.5
for iteration in range(100000):
    layer = 1 / (1 + exp(-(dot(training_set_inputs, weights1[:-1]) + weights1[-1]*bias)))
    layers = array([(layer**2).flatten(), layer.flatten()]).T
    output = 1 / (1 + exp(-(dot(layers, weights2[:-1]) + weights2[-1]*bias)))

    error = training_set_outputs - output
    delta2 = error * output * (1 - output)
    weights2[:-1] += dot(layers.T, delta2)
    weights2[-1] += np.sum(delta2 * bias)

    delta_layer = np.dot(delta2, weights2[:-1].T)
    derivative_features = array([2 * layer, np.ones_like(layer)]).T
    delta_layer_weighted = (delta_layer * derivative_features)[0]
    delta_layer_final = delta_layer_weighted.sum(axis=1, keepdims=True) * layer * (1 - layer)
    weights1[:-1] += dot(training_set_inputs.T, delta_layer_final)
    weights1[-1] += np.sum(delta_layer_final * bias)

def f(test):
    layer = 1 / (1 + exp(-(dot(test, weights1[:-1]) + weights1[-1] * bias)))
    layers = array([(layer ** 2).flatten(), layer.flatten()]).T
    output = 1 / (1 + exp(-(dot(layers, weights2[:-1]) + weights2[-1] * bias)))
    return output

# Тестирование на обучающей выборке
print("=== ТЕСТИРОВАНИЕ НА ОБУЧАЮЩЕЙ ВЫБОРКЕ ===")
for i in range(len(training_set_inputs)):
    test_input = training_set_inputs[i]
    prediction = f(test_input.reshape(1, -1))
    expected = training_set_outputs[i][0]
    print(f"Вход: {test_input} -> Предсказание: {prediction[0][0]:.6f} (Ожидалось: {expected})")

print("\nОкругленные предсказания на обучающей выборке:")
for i in range(len(training_set_inputs)):
    test_input = training_set_inputs[i]
    prediction = f(test_input.reshape(1, -1))
    print(f"{np.round(prediction[0][0])}", end=" ")
print()

# Тестирование на новых данных
print("\n=== ТЕСТИРОВАНИЕ НА НОВЫХ ДАННЫХ ===")
test_cases = [
    [0, 0, 0, 0],  # x3=0, x4=0 -> 0
    [0, 0, 0, 1],  # x3=0, x4=1 -> 1
    [0, 0, 1, 0],  # x3=1, x4=0 -> 1
    [0, 0, 1, 1],  # x3=1, x4=1 -> 0
    [1, 0, 0, 0],  # x3=0, x4=0 -> 0
    [0, 1, 0, 1],  # x3=0, x4=1 -> 1
    [1, 1, 1, 0],  # x3=1, x4=0 -> 1
    [1, 1, 1, 1],  # x3=1, x4=1 -> 0
]

print("X3 XOR X4 тесты:")
for test in test_cases:
    prediction = f(array([test]))
    xor_result = test[2] ^ test[3]  # x3 XOR x4
    print(f"Вход: {test} -> Предсказание: {prediction[0][0]:.6f} (X3 XOR X4 = {xor_result})")

# Проверка точности
print("\n=== СВОДКА ===")
correct = 0
total = len(training_set_inputs)

for i in range(total):
    test_input = training_set_inputs[i]
    prediction = f(test_input.reshape(1, -1))
    if np.round(prediction[0][0]) == training_set_outputs[i][0]:
        correct += 1

accuracy = correct / total * 100
print(f"Точность на обучающей выборке: {accuracy:.1f}% ({correct}/{total})")

# Вывод финальных весов
print("\nФинальные веса:")
print("weights1:", [w[0] for w in weights1])
print("weights2:", [w[0] for w in weights2])

import numpy as np
from numpy import exp, array, dot


def comprehensive_test():
    """Всестороннее тестирование обученной сети"""

    # Используем обученные веса из предыдущего кода
    # (предполагаем, что weights1, weights2, bias уже обучены)

    # Все возможные комбинации 4 битов (16 случаев)
    all_test_cases = []
    for i in range(16):
        # Преобразуем число в двоичный формат с 4 битами
        binary = [int(x) for x in format(i, '04b')]
        all_test_cases.append(binary)

    all_test_cases = np.array(all_test_cases)

    print("=== ПОЛНОЕ ТЕСТИРОВАНИЕ НА 16 КОМБИНАЦИЯХ ===")
    print("Формат: [x1, x2, x3, x4] -> Предсказание (ожидается x3 XOR x4)")
    print()

    correct_predictions = 0
    total_cases = len(all_test_cases)

    for i, test_case in enumerate(all_test_cases):
        # Получаем предсказание
        prediction = f(test_case.reshape(1, -1))
        predicted_value = prediction[0][0]

        # Ожидаемое значение - XOR между x3 и x4 (индексы 2 и 3)
        expected_value = test_case[2] ^ test_case[3]

        # Округляем предсказание для сравнения
        rounded_prediction = round(predicted_value)

        # Проверяем правильность
        is_correct = (rounded_prediction == expected_value)
        if is_correct:
            correct_predictions += 1

        # Выводим результат
        status = "✓" if is_correct else "✗"
        print(f"{status} Тест {i + 1:2d}: {test_case} -> {predicted_value:.4f} "
              f"(округляем: {rounded_prediction}, ожидалось: {expected_value})")

    # Итоговая статистика
    accuracy = correct_predictions / total_cases * 100
    print("\n" + "=" * 50)
    print(f"ИТОГОВАЯ СТАТИСТИКА:")
    print(f"Правильных предсказаний: {correct_predictions}/{total_cases}")
    print(f"Точность: {accuracy:.2f}%")
    print("=" * 50)

    # Дополнительная аналитика по типам случаев
    print("\n=== АНАЛИЗ ПО ТИПАМ СЛУЧАЕВ ===")

    # Группируем по значениям x3 и x4
    cases_by_type = {
        "x3=0, x4=0 (XOR=0)": [],
        "x3=0, x4=1 (XOR=1)": [],
        "x3=1, x4=0 (XOR=1)": [],
        "x3=1, x4=1 (XOR=0)": []
    }

    for test_case in all_test_cases:
        x3, x4 = test_case[2], test_case[3]
        xor_result = x3 ^ x4

        prediction = f(test_case.reshape(1, -1))
        predicted_value = prediction[0][0]
        rounded_prediction = round(predicted_value)

        if x3 == 0 and x4 == 0:
            cases_by_type["x3=0, x4=0 (XOR=0)"].append(rounded_prediction == xor_result)
        elif x3 == 0 and x4 == 1:
            cases_by_type["x3=0, x4=1 (XOR=1)"].append(rounded_prediction == xor_result)
        elif x3 == 1 and x4 == 0:
            cases_by_type["x3=1, x4=0 (XOR=1)"].append(rounded_prediction == xor_result)
        elif x3 == 1 and x4 == 1:
            cases_by_type["x3=1, x4=1 (XOR=0)"].append(rounded_prediction == xor_result)

    # Выводим статистику по типам
    for case_type, results in cases_by_type.items():
        correct = sum(results)
        total = len(results)
        accuracy = correct / total * 100 if total > 0 else 0
        print(f"{case_type}: {correct}/{total} правильных ({accuracy:.1f}%)")

    return correct_predictions, total_cases, accuracy


# Запускаем полное тестирование
correct, total, accuracy = comprehensive_test()

# Дополнительное тестирование на крайних случаях
print("\n=== ТЕСТИРОВАНИЕ НА КРАЙНИХ СЛУЧАЯХ ===")
edge_cases = [
    [0, 0, 0, 0],  # Все нули
    [1, 1, 1, 1],  # Все единицы
    [0, 1, 0, 1],  # Чередование 1
    [1, 0, 1, 0],  # Чередование 2
]

print("Крайние случаи:")
for case in edge_cases:
    prediction = f(np.array([case]))
    expected = case[2] ^ case[3]
    rounded = round(prediction[0][0])
    status = "✓" if rounded == expected else "✗"
    print(f"{status} {case} -> {prediction[0][0]:.4f} (округляем: {rounded}, ожидалось: {expected})")

# Тестирование на зашумленных данных
print("\n=== ТЕСТИРОВАНИЕ НА ЗАШУМЛЕННЫХ ДАННЫХ ===")
# Добавляем небольшой шум к тестовым случаям
noisy_test_cases = []
base_cases = [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1]]

for base in base_cases:
    # Добавляем случайный шум ±0.1
    noisy = [x + np.random.uniform(-0.1, 0.1) for x in base]
    # Округляем обратно к 0 или 1
    noisy_rounded = [round(x) for x in noisy]
    noisy_test_cases.append(noisy_rounded)

print("Зашумленные данные (округленные):")
for i, case in enumerate(noisy_test_cases):
    prediction = f(np.array([case]))
    expected = case[2] ^ case[3]
    rounded = round(prediction[0][0])
    status = "✓" if rounded == expected else "✗"
    print(f"{status} {case} -> {prediction[0][0]:.4f} (округляем: {rounded}, ожидалось: {expected})")

# Финальный вывод
print("\n" + "=" * 60)
print("ФИНАЛЬНЫЙ РЕЗУЛЬТАТ ТЕСТИРОВАНИЯ")
print(f"Общая точность на всех тестовых случаях: {accuracy:.2f}%")
print(f"Правильных предсказаний: {correct} из {total}")
print("=" * 60)

if accuracy == 100:
    print("🎉 Отличный результат! Сеть идеально справилась с задачей!")
elif accuracy >= 90:
    print("✅ Хороший результат! Сеть хорошо обучилась.")
elif accuracy >= 80:
    print("⚠️  Удовлетворительный результат. Возможно, нужно больше итераций обучения.")
else:
    print("❌ Низкая точность. Рекомендуется проверить архитектуру сети или процесс обучения.")
