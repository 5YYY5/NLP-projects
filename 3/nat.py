from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    PER,
    NamesExtractor,
    Doc
)

# Инициализация компонентов
segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)

# Чтение файла с обработкой ошибок
try:
    # Убедитесь, что используете правильную кодировку (например, 'utf-8')
    with open('C:/Users/User/OneDrive/Рабочий стол/Programs_for_UDA/test.txt', 'r', encoding='utf-8') as file:
        text = file.read()
except FileNotFoundError:
    print("Ошибка: Файл не найден. Проверьте путь к файлу.")
    exit()
except Exception as e:
    print(f"Ошибка при чтении файла: {e}")
    exit()

# Создание документа и обработка
doc = Doc(text)

# 1. СЕГМЕНТАЦИЯ: Разбивка текста на предложения и токены
doc.segment(segmenter)  # <- Этой строки не было в вашем коде

# 2. МОРФОЛОГИЧЕСКИЙ АНАЛИЗ: Определение части речи и грамматических характеристик
doc.tag_morph(morph_tagger)

# Вывод результатов
print("=== ВСЕ ТОКЕНЫ ДОКУМЕНТА ===")
for token in doc.tokens[:10]:  # Выводим первые 10 токенов
    print(f"Текст: {token.text}, POS: {token.pos}, Features: {token.feats}")

print("\n=== МОРФОЛОГИЧЕСКИЙ РАЗБОР ПЕРВОГО ПРЕДЛОЖЕНИЯ ===")
if doc.sents:
    for i in range(5):  # Проверяем, что есть хотя бы одно предложение
        doc.sents[i].morph.print()
        print(f"\n=== МОРФОЛОГИЧЕСКИЙ РАЗБОР {i+2} ПРЕДЛОЖЕНИЯ ===")
else:
    print("Предложения не найдены.")