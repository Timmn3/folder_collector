# folder_collector.py

import os


def collect_content(directory):
    """Собирает имена папок первого уровня и .py файлы из указанной директории."""
    folders = []
    python_files = []

    try:
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isdir(full_path):
                folders.append(item)  # Имя папки
            elif os.path.isfile(full_path): # and item.endswith('.py'):
                python_files.append(item)  # Имя .py файла
    except Exception as e:
        print(f"Ошибка при обработке директории: {e}")

    return folders, python_files


if __name__ == "__main__":
    target_dir_2 = "C:/PycharmProjects/ON_server/ai_bot_2"
    target_dir = "C:\PycharmProjects\ON_server\EmailFast"
    target_dir = r"C:\PycharmProjects\My\tochka"

    if os.path.isdir(target_dir):
        folder_list, py_files = collect_content(target_dir)

        # Вывод списков
        print("\nПапки первого уровня:")
        print(folder_list)

        print("\nФайлы .py в корневой папке:")
        print(py_files)

    else:
        print("Указанный путь не является существующей папкой.")