from constants import *


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


def calculate_index(text):
    """
    Вычисляет индекс в тексте
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

def main():
    try:
        text = read_file(PATH_ENCRYPTED)
        print("\nЗашифрованный текст:\n")
        print(text)
        percent_dict = calculate_index(text)
        print("Индекс частот: ")
        sorted_dict = {}
        for key in sorted(percent_dict, key=percent_dict.get, reverse=True):
            sorted_dict[key] = percent_dict[key]
        print(sorted_dict)
        print("Дешифрованный текст: ")
        for char in text:
            if char in DECRYPT_KEY:
                text = text.replace(char, DECRYPT_KEY[char])
        print(text)
        crypt_key = DECRYPT_KEY
        print("\nКлюч шифрования:\n")
        print(crypt_key)
        write_to_file(PATH_DECRYPTED, text)
        write_to_file(PATH_KEY, str(crypt_key))
        print("\nРезультаты успешно записаны в файлы")

    except FileNotFoundError:
        print("Ошибка: файл зашифрованного текста не найден")
    except UnicodeDecodeError:
        print("Ошибка: проблема с кодировкой файла")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()