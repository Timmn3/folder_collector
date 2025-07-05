import os
import base64

# Глобальные константы для исключений
EXCLUDED_FOLDERS = {'.git', '.idea', '.venv', 'logs', '__pycache__'}
EXCLUDED_FILES = {'.gitignore'}
TEXT_EXTENSIONS = [
    '.py', '.txt', '.html', '.css', '.js', '.json',
    '.md', '.ini', '.conf', '.sh', '.bat', '.xml', '.csv', '.gitignore'
]


def collect_content(directory):
    """Собирает имена папок первого уровня и .py файлы из указанной директории, исключая системные."""
    folders = []
    python_files = []

    try:
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)

            if os.path.isdir(full_path):
                if item not in EXCLUDED_FOLDERS:
                    folders.append(item)

            elif os.path.isfile(full_path):
                if item.endswith('.py') and item not in EXCLUDED_FILES:
                    python_files.append(item)

    except Exception as e:
        print(f"Ошибка при обработке директории: {e}")

    return folders, python_files


def collect_files(project_path, folders_to_include, files_in_root, output_file):
    """Собирает содержимое файлов проекта в выходной файл."""
    # Создаем папку OUT если ее нет
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Обработка файлов в корневой папке
        for file_name in files_in_root:
            file_path = os.path.join(project_path, file_name)
            if os.path.isfile(file_path):
                process_file(file_path, project_path, outfile)
            else:
                print(f"Файл не найден: {file_name}")

        # Обработка файлов в подпапках
        for folder in folders_to_include:
            full_folder_path = os.path.join(project_path, folder)
            if not os.path.isdir(full_folder_path):
                print(f"Папка не найдена: {full_folder_path}")
                continue

            for root, dirs, files in os.walk(full_folder_path):
                # Исключаем системные папки при обходе
                dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS]

                for file in files:
                    # Пропускаем системные файлы
                    if file in EXCLUDED_FILES:
                        continue

                    file_path = os.path.join(root, file)
                    process_file(file_path, project_path, outfile)

    print(f"\nФайлы успешно собраны в: {output_file}")


def process_file(file_path, base_path, outfile):
    """Обрабатывает один файл и записывает его содержимое в выходной файл."""
    try:
        file_name = os.path.basename(file_path)
        ext = os.path.splitext(file_name)[1].lower()
        relative_path = os.path.relpath(file_path, base_path)

        # Определяем способ чтения файла
        mode = 'r' if ext in TEXT_EXTENSIONS else 'rb'

        with open(file_path, mode, encoding='utf-8' if mode == 'r' else None) as infile:
            content = infile.read()

            if mode == 'rb':
                # Кодируем бинарные файлы в base64
                encoded = base64.b64encode(content).decode('utf-8')
                outfile.write(f"BINARY_FILE: {relative_path} (base64)\n")
                outfile.write(encoded)
            else:
                outfile.write(f"FILE: {relative_path}\n")
                outfile.write(content)

            outfile.write("\n\n")

    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")


def main():
    """Основная функция для обработки проекта."""
    # Укажите путь к вашему проекту
    target_dir = "C:/PycharmProjects/ON_server/ai_bot_2"
    target_dir = "C:\PycharmProjects\ON_server\EmailFast"
    target_dir = r"C:\PycharmProjects\My\tochka"
    target_dir = r"C:\PycharmProjects\My\minimal_avito_parser"
    # target_dir = r"C:\PycharmProjects\My\view_logs"

    if not os.path.isdir(target_dir):
        print("Указанный путь не является существующей папкой.")
        return

    # Получаем имя проекта из пути
    project_name = os.path.basename(target_dir)
    output_file = f"OUT/{project_name}.txt"

    # Собираем структуру проекта
    folders, py_files = collect_content(target_dir)

    # Выводим информацию о структуре
    print("\nПапки первого уровня:")
    print(folders)
    print("\nФайлы .py в корневой папке:")
    print(py_files)

    # Собираем содержимое файлов
    collect_files(target_dir, folders, py_files, output_file)


if __name__ == "__main__":
    main()