import argparse
from config import Config
from asym_crypto import AsymmetricCrypto
from sym_crypto import SymmetricCrypto
from filemanager import FileManager


class HybridCryptoSystem:
    """Гибридная криптосистема, объединяющая симметричное и асимметричное шифрование"""

    def __init__(self, config: Config):
        self.config = config
        self.asymmetric = AsymmetricCrypto()
        self.symmetric = SymmetricCrypto()
        self.files = FileManager()

    def generate_and_save_keys(self, key_size: int = 256) -> None:
        """Генерирует и сохраняет все необходимые ключи"""
        private_key, public_key = self.asymmetric.generate_keys()
        symmetric_key = self.symmetric.generate_key(key_size)

        self.files.save_key(public_key, self.config.PATHS['PUBLIC_KEY'])
        self.files.save_key(private_key, self.config.PATHS['SECRET_KEY'])
        encrypted_sym_key = self.asymmetric.encrypt_with_public_key(public_key, symmetric_key)
        self.files.save_file(self.config.PATHS['SYMMETRIC_KEY'], encrypted_sym_key)

    def encrypt_file(self, input_file: str, output_file: str) -> None:
        """Шифрует файл"""
        private_key = self.files.load_private_key(self.config.PATHS['SECRET_KEY'])
        encrypted_sym_key = self.files.load_file(self.config.PATHS['SYMMETRIC_KEY'])
        symmetric_key = self.asymmetric.decrypt_with_private_key(private_key, encrypted_sym_key)

        data = self.files.load_file(input_file)
        encrypted_data = self.symmetric.encrypt_data(data, symmetric_key)
        self.files.save_file(output_file, encrypted_data)

    def decrypt_file(self, input_file: str, output_file: str) -> None:
        """Дешифрует файл"""
        private_key = self.files.load_private_key(self.config.PATHS['SECRET_KEY'])
        encrypted_sym_key = self.files.load_file(self.config.PATHS['SYMMETRIC_KEY'])
        symmetric_key = self.asymmetric.decrypt_with_private_key(private_key, encrypted_sym_key)

        encrypted_data = self.files.load_file(input_file)
        decrypted_data = self.symmetric.decrypt_data(encrypted_data, symmetric_key)
        self.files.save_file(output_file, decrypted_data)


def full_cycle(config_path: str, input_file: str, key_size: int = 256):
    """Выполняет полный цикл: генерация ключей, шифрование и дешифрование"""
    config = Config.from_json(config_path)
    crypto = HybridCryptoSystem(config)

    print("1. Генерация ключей...")
    crypto.generate_and_save_keys(key_size)

    print("2. Шифрование файла...")
    encrypted_file = config.PATHS['ENCRYPTED_FILE']  # Используем путь из настроек
    crypto.encrypt_file(input_file, encrypted_file)

    print("3. Дешифрование файла...")
    decrypted_file = config.PATHS['DECRYPTED_FILE']  # Используем путь из настроек
    crypto.decrypt_file(encrypted_file, decrypted_file)

    print(f"\nГотово! Результаты сохранены в:")
    print(f"- Ключи: {config.PATHS['PUBLIC_KEY']}, {config.PATHS['SECRET_KEY']}")
    print(f"- Зашифрованный файл: {encrypted_file}")
    print(f"- Расшифрованный файл: {decrypted_file}")


def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема (RSA + AES)")
    parser.add_argument('--settings', required=True, help='Путь к файлу настроек settings.json')
    parser.add_argument('--input', required=True, help='Файл для шифрования')
    parser.add_argument('--key-size', type=int, default=256, choices=[128, 192, 256],
                        help='Размер симметричного ключа (по умолчанию 256)')

    args = parser.parse_args()
    full_cycle(args.settings, args.input, args.key_size)


if __name__ == "__main__":
    main()