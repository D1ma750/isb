from constants import *
import json


def write_to_file(filename, content):
    """
    Записывает содержимое в файл
    :param filename: имя файла
    :param content: содержимое для записи
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def read_file(filename):
    """
    Читает данные из файл
    :param filename: имя файла
    """
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def read_json(filename: str) -> dict:
    """
    Загружает из JSON-файла.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка при загрузке {filename}: {e}")
        return {}


def calculate_frequency(text):
    """
    Вычисляет частоты в тексте
    :param text: исходный текст
    :return: словарь, где ключ — символ, значение — процент его встречаемости
    """
    char_count = {}  # Словарь
    text_len = len(text)

    for char in text:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    char_percentages = {}
    for char, count in char_count.items():
        char_percentages[char] = (count / text_len)

    return char_percentages


def decrypt_text(text, key):
    for original_char, replacement_char in key.items():
        text = text.replace(original_char, replacement_char)
    return text


def main():
    try:
        text = read_file(PATH_ENCRYPTED)
        print("\nЗашифрованный текст:\n")
        print(text)
        percent_dict = calculate_frequency(text)
        print("Индекс частот: ")
        sorted_dict = {}
        for key in sorted(percent_dict, key=percent_dict.get, reverse=True):
            sorted_dict[key] = percent_dict[key]
        print(sorted_dict)
        print("Дешифрованный текст: ")
        key = read_json(DECRYPT_KEY)
        decrypted_text = decrypt_text(text, key)
        print(decrypted_text)
        write_to_file(PATH_DECRYPTED, decrypted_text)
        print("\nРезультаты успешно записаны в файлы")

    except FileNotFoundError:
        print("Ошибка: файл зашифрованного текста не найден")
    except UnicodeDecodeError:
        print("Ошибка: проблема с кодировкой файла")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()