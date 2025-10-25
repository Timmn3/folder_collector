import os
import base64

# Глобальные константы для исключений
EXCLUDED_FOLDERS = {
    '.git', '.idea', '.venv', 'logs', '__pycache__', 'alembic',
    'celery_worker', 'migrations', 'server_data', 'node_modules',
    'dist', 'test', 'photo_test','voices_en', 'voices_ru', 'photo'
}
EXCLUDED_FILES = {'.gitignore'}
EXCLUDED_PATHS = {
    'parsing/data'.replace('\\', '/'),  # Универсальный формат пути
}

# Расширения, которые мы НЕ берём в обработку
EXCLUDED_EXTENSIONS = {'.tsx', '.svg', '.ts'}

# Разрешённые текстовые расширения
TEXT_EXTENSIONS = [
    '.py', '.txt', '.html', '.css', '.js', '.json',
    '.md', '.ini', '.conf', '.sh', '.bat', '.xml', '.csv',
    '.gitignore', '.yml', '.yaml', '.env'
]
SPECIAL_TEXT_FILES = {'Dockerfile', 'docker-compose.yml'}


def collect_content(directory):
    """Собирает информацию о папках и файлах с указанием статуса исключения."""
    included_folders = []
    excluded_folders = []
    included_files = []
    excluded_files = []

    try:
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)

            if os.path.isdir(full_path):
                if item in EXCLUDED_FOLDERS:
                    excluded_folders.append(item)
                else:
                    included_folders.append(item)

            elif os.path.isfile(full_path):
                ext = os.path.splitext(item)[1].lower()

                # Пропускаем запрещённые расширения
                if ext in EXCLUDED_EXTENSIONS:
                    excluded_files.append(item)
                    continue

                # Берем все текстовые расширения, специальные файлы и .env
                if ext in TEXT_EXTENSIONS or item in SPECIAL_TEXT_FILES or item == ".env":
                    if item in EXCLUDED_FILES:
                        excluded_files.append(item)
                    else:
                        included_files.append(item)

    except Exception as e:
        print(f"Ошибка при обработке директории: {e}")

    return included_folders, included_files, excluded_folders, excluded_files


def collect_files(project_path, folders_to_include, files_in_root, output_file):
    """Собирает содержимое файлов проекта в выходной файл."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Фильтрация папок первого уровня по EXCLUDED_PATHS
    filtered = []
    for folder in folders_to_include:
        normalized = folder.replace('\\', '/')
        if normalized in EXCLUDED_PATHS:
            print(f"Исключена папка первого уровня: {folder}")
        else:
            filtered.append(folder)
    folders_to_include = filtered

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Файлы в корне
        for name in files_in_root:
            path = os.path.join(project_path, name)
            if os.path.isfile(path):
                process_file(path, project_path, outfile)
            else:
                print(f"Файл не найден: {name}")

        # Файлы в подпапках
        for folder in folders_to_include:
            full_folder = os.path.join(project_path, folder)
            if not os.path.isdir(full_folder):
                print(f"Папка не найдена: {full_folder}")
                continue

            for root, dirs, files in os.walk(full_folder):
                rel_root = os.path.relpath(root, project_path)
                if rel_root == '.':
                    rel_root = ''

                # Фильтрация вложенных папок
                dirs[:] = [
                    d for d in dirs
                    if d not in EXCLUDED_FOLDERS and
                    os.path.join(rel_root, d).replace('\\', '/') not in EXCLUDED_PATHS
                ]

                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if file in EXCLUDED_FILES or ext in EXCLUDED_EXTENSIONS:
                        continue
                    process_file(os.path.join(root, file), project_path, outfile)

    print(f"\nФайлы успешно собраны в: {output_file}")


def process_file(file_path, base_path, outfile):
    """Обрабатывает один файл и записывает его содержимое в выходной файл."""
    try:
        name = os.path.basename(file_path)
        ext = os.path.splitext(name)[1].lower()

        # Пропускаем запрещённые расширения
        if ext in EXCLUDED_EXTENSIONS:
            return

        rel = os.path.relpath(file_path, base_path)

        # Текстовый режим для разрешённых расширений и специальных файлов
        if ext in TEXT_EXTENSIONS or name in SPECIAL_TEXT_FILES or name == ".env":
            mode = 'r'
        else:
            mode = 'rb'

        with open(file_path, mode, encoding='utf-8' if mode == 'r' else None) as f:
            content = f.read()
            if mode == 'rb':
                enc = base64.b64encode(content).decode('utf-8')
                outfile.write(f"BINARY_FILE: {rel} (base64)\n")
                outfile.write(enc)
            else:
                outfile.write(f"FILE: {rel}\n")
                outfile.write(content)
            outfile.write("\n\n")

    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")


def main():
    # target_dir = r"C:\PycharmProjects\My\tochka"
    # target_dir = r"C:\PycharmProjects\My\tochka\handlers\users"
    # target_dir = r"C:\PycharmProjects\My\parser_agent"
    # target_dir = r"c:\PycharmProjects\My\avito_parse
    #     # target_dir = r"c:\PycharmProjects\ON_server\Avito\suppor"rt_bot"
    # target_dir = r"C:\PycharmProjects\ON_server\EmailFast"
    # target_dir = r"C:\PycharmProjects\FastAPI\CityCatalog"
    # target_dir = r"C:\PycharmProjects\My\pars_flashscorekz"
    # target_dir = r"C:\PycharmProjects\My\parsing_flashscorekz"
    # target_dir = r"c:\PycharmProjects\ON_server\ai_bot_2"
    # target_dir = r"C:\PycharmProjects\test_task\telegram_shop_bot"
    # target_dir = r"C:\PycharmProjects\test_task\weather_bot"
    # target_dir = r"C:\PycharmProjects\ON_server\vpn"
    # target_dir = r"c:\PycharmProjects\ON_server\vpn_1"
    # target_dir = r"C:\PycharmProjects\My\email_bot"
    target_dir = r"C:\PycharmProjects\test_task\numlex"
    if not os.path.isdir(target_dir):
        print("Указанный путь не является существующей папкой.")
        return

    project = os.path.basename(target_dir)
    out_file = f"OUT/{project}.txt"

    inc_folders, inc_files, exc_folders, exc_files = collect_content(target_dir)

    print("\nПапки первого уровня:", inc_folders)
    print("\nИсключенные папки:", exc_folders)
    print("\nФайлы в корне:", inc_files)
    print("\nИсключенные файлы в корне:", exc_files)

    collect_files(target_dir, inc_folders, inc_files, out_file)


if __name__ == "__main__":
    main()
