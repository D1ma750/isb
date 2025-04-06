def read_file(filename):
    """Чтение содержимого файла."""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(filename, content):
    """Запись содержимого в файл."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def is_russian_letter(char):
    """Проверка, является ли символ русской буквой (без учёта 'ё')."""
    return 'а' <= char.lower() <= 'я' and char.lower() != 'ё'


def vigenere_encrypt(text, key):
    """
    Шифрование русскоязычного текста шифром Виженера.

    Args:
        text: Исходный текст для шифрования.
        key: Ключ для шифрования.

    Returns:
        Зашифрованный текст с сохранением регистра и не-буквенных символов.
    """
    encrypted_chars = []
    key_length = len(key)

    # Преобразуем ключ в числовые смещения
    key_offsets = [ord(char.lower()) - ord('а') for char in key]

    # Алфавит (31 буква)
    alphabet_length = 31

    key_index = 0
    for char in text:
        if is_russian_letter(char):
            # Определяем смещение для текущего символа
            offset = key_offsets[key_index % key_length]
            key_index += 1

            # Шифруем символ с сохранением регистра
            if char.isupper():
                base = ord('А')
            else:
                base = ord('а')

            # Вычисляем позицию в алфавите
            char_pos = ord(char.lower()) - ord('а')
            # Применяем шифр Виженера
            new_pos = (char_pos + offset) % alphabet_length
            new_char = chr(base + new_pos)
            encrypted_chars.append(new_char)
        else:
            # Оставляем нерусские символы без изменений
            encrypted_chars.append(char)

    return ''.join(encrypted_chars)


def validate_key(key):
    """Проверка валидности ключа."""
    if not key:
        raise ValueError("Ключ не может быть пустым")

    for char in key:
        if not is_russian_letter(char):
            raise ValueError("Ключ должен содержать только русские буквы (без 'ё')")


def main():
    """Основная функция программы."""
    try:
        # Чтение исходного текста и ключа
        input_filename = 'input.txt'
        key_filename = 'key.txt'
        output_filename = 'encrypted.txt'

        text = read_file(input_filename)
        key = read_file(key_filename).strip()

        # Валидация ключа
        validate_key(key)

        # Шифрование текста
        encrypted_text = vigenere_encrypt(text, key)

        # Запись результата
        write_file(output_filename, encrypted_text)
        print(f"Текст успешно зашифрован и сохранён в {output_filename}")

    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден - {e.filename}")
    except ValueError as e:
        print(f"Ошибка в ключе: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == '__main__':
    main()