import re

def split_sentences(text):
    """Разделение текста на предложения по правилам задания"""
    sentences = []
    current_sentence = ""
    i = 0
    n = len(text)
    
    while i < n:
        current_sentence += text[i]
        
        # Проверяем конец предложения
        if text[i] in '.!?…':
            # Проверяем, что после знака препинания идет пробел и заглавная буква
            # или тире и заглавная буква (для диалога)
            if i + 1 < n:
                # Пропускаем пробелы после знака препинания
                j = i + 1
                while j < n and text[j].isspace():
                    j += 1
                
                # Проверяем условия конца предложения
                if j >= n:  # конец текста
                    sentences.append(current_sentence.strip())
                    current_sentence = ""
                elif (text[j].isupper() or 
                      (text[j] == '-' and j + 1 < n and text[j + 1].isupper())):
                    # Нашли конец предложения
                    sentences.append(current_sentence.strip())
                    current_sentence = ""
            
        i += 1
    
    # Добавляем последнее предложение, если оно есть
    if current_sentence.strip():
        sentences.append(current_sentence.strip())
    
    return sentences

def tokenize_sentence(sentence):
    """Токенизация предложения по правилам задания"""
    # Заменяем знаки препинания на пробелы (кроме точек, дефисов и слешей)
    cleaned = re.sub(r'[,;:!?()"«»—]', ' ', sentence)
    
    # Обрабатываем точки, дефисы и слеши, окруженные пробелами
    tokens = []
    current_token = ""
    i = 0
    n = len(cleaned)
    
    while i < n:
        if cleaned[i].isspace():
            if current_token:
                tokens.append(current_token)
                current_token = ""
        else:
            current_token += cleaned[i]
        i += 1
    
    # Добавляем последний токен
    if current_token:
        tokens.append(current_token)
    
    return tokens

def is_russian_word(token):
    """Проверка, является ли токен русским словом по правилам задания"""
    # Русское слово состоит из русских букв, дефисов, слешей и точек
    if not token:
        return False
    
    # Проверяем, что в токене только разрешенные символы
    allowed_chars = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-./')
    
    for char in token:
        if char not in allowed_chars:
            return False
    
    return True

def count_letters_in_word(word):
    """Подсчет количества букв в русском слове (включая дефисы, слеши, точки)"""
    return len(word)

def analyze_text(text):
    """Основная функция анализа текста"""
    sentences = split_sentences(text)
    total_tokens = 0
    total_russian_words = 0
    total_russian_letters = 0
    all_russian_words_lengths = []
    
    print("РЕЗУЛЬТАТЫ АНАЛИЗА:\n")
    
    for i, sentence in enumerate(sentences, 1):
        tokens = tokenize_sentence(sentence)
        russian_words = [token for token in tokens if is_russian_word(token)]
        russian_word_lengths = [count_letters_in_word(word) for word in russian_words]
        
        # Собираем статистику
        total_tokens += len(tokens)
        total_russian_words += len(russian_words)
        total_russian_letters += sum(russian_word_lengths)
        all_russian_words_lengths.extend(russian_word_lengths)
        
        # Выводим информацию о предложении
        print(f"Предложение {i}: \"{sentence}\"")
        print(f"  Токенов: {len(tokens)}, Русских слов: {len(russian_words)}")
        if russian_words:
            lengths_str = ", ".join(map(str, russian_word_lengths))
            print(f"  Длины русских слов: {lengths_str}")
        print()
    
    # Выводим общую статистику
    if sentences:
        avg_tokens = total_tokens / len(sentences)
        print(f"Среднее количество токенов в предложении: {avg_tokens:.2f}")
    else:
        avg_tokens = 0
        print("Среднее количество токенов в предложении: 0")
    
    if total_russian_words > 0:
        avg_word_length = total_russian_letters / total_russian_words
        print(f"Средняя длина русского слова: {avg_word_length:.2f}")
    else:
        avg_word_length = 0
        print("Средняя длина русского слова: 0")
    
    return {
        'sentences': sentences,
        'avg_tokens': avg_tokens,
        'avg_word_length': avg_word_length
    }



# if True:
    
#     # Демонстрация работы на произвольном тексте
#     file = open("C:/Users/User/OneDrive/Рабочий стол/Programs_for_UDA/4/Tolstoy2.txt","r")
#     demo_text = file.read()
#     file.close()
    
#     print(f"\nДЕМОНСТРАЦИЯ НА ПРОИЗВОЛЬНОМ ТЕКСТЕ:")
#     print("-" * 40)
#     analyze_text(demo_text)

  # Демонстрация работы на произвольном тексте
    try:
        # Пробуем разные кодировки
        encodings = ['utf-8', 'cp1251', 'windows-1251', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open("C:/Users/User/OneDrive/Рабочий стол/Programs_for_UDA/4/Tolstoy2.txt", "r", encoding=encoding) as file:
                    demo_text = file.read()
                print(f"\nДЕМОНСТРАЦИЯ НА ПРОИЗВОЛЬНОМ ТЕКСТЕ (кодировка: {encoding}):")
                print("-" * 40)
                analyze_text(demo_text)
                break
            except UnicodeDecodeError:
                continue
        else:
            print("Не удалось прочитать файл ни в одной из попробованных кодировок")
            
    except FileNotFoundError:
        print("Файл Tolstoy2.txt не найден по указанному пути")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")