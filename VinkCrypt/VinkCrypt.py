import os
import sys

def xor_crypt(data, key):
    """
    Простая функция шифрования через XOR.
    Каждый байт данных 'складывается' с байтом ключа.
    """
    # Преобразуем ключ в байты, если он строка
    if isinstance(key, str):
        key = key.encode()
    
    result = bytearray()
    key_len = len(key)
    
    for i, byte in enumerate(data):
        # XOR операция: byte ^ key[i % key_len]
        # Это обратимая операция: если сделать её дважды, вернется исходное значение
        result.append(byte ^ key[i % key_len])
        
    return bytes(result)

def process_file(file_path, key, mode='encrypt'):
    """
    Читает файл, шифрует/дешифрует и сохраняет новый файл.
    """
    try:
        # Читаем весь файл как бинарные данные
        with open(file_path, 'rb') as f:
            data = f.read()
            
        print(f"📂 Обработка файла: {os.path.basename(file_path)}...")
        
        # Шифруем или дешифруем данные
        encrypted_data = xor_crypt(data, key)
        
        # Формируем новое имя файла
        name, ext = os.path.splitext(file_path)
        
        if mode == 'encrypt':
            # При шифровании добавляем .vinks и меняем имя на случайное (или по шаблону)
            # Для простоты возьмем первые 8 символов хэша или просто добавим суффикс
            new_name = f"{name}_encrypted.vinks"
            print(f"🔒 Шифрую... Ключ: '{key}'")
        else:
            # При расшифровке убираем .vinks и возвращаем оригинальное расширение
            # Но так как мы не храним оригинальное расширение внутри файла в этом простом примере,
            # нам нужно знать, какой оно было. 
            # В реальном приложении расширение хранят в заголовке файла.
            # Здесь для простоты мы просто заменим .vinks на .decrypted + оригинальное расширение,
            # которое пользователь должен указать или мы можем попытаться угадать.
            
            # Давай сделаем проще: спросим у пользователя оригинальное расширение при расшифровке
            original_ext = input("Введите оригинальное расширение файла (например, .txt, .jpg): ")
            new_name = f"{name}_decrypted{original_ext}"
            print(f"🔓 Расшифровываю... Ключ: '{key}'")
            
        # Записываем новый файл
        with open(new_name, 'wb') as f:
            f.write(encrypted_data)
            
        print(f"✅ Готово! Новый файл сохранен как: {new_name}")
        
    except FileNotFoundError:
        print("❌ Ошибка: Файл не найден.")
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")

# --- Главное меню ---

print("🛡️ File Cipher v1.0")
print("1. Зашифровать файл")
print("2. Расшифровать файл")
print("3. Выход")

choice = input("Выберите действие (1/2/3): ")

if choice == '3':
    sys.exit()

file_path = input("Введите путь к файлу (или перетащите файл сюда): ").strip('"') # strip убирает кавычки если перетаскивали
key = input("Введите секретный ключ (пароль): ")

if choice == '1':
    process_file(file_path, key, 'encrypt')
elif choice == '2':
    process_file(file_path, key, 'decrypt')
else:
    print("Неверный выбор")