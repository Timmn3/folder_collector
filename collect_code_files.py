import os

def collect_files(project_path, folders_to_include, files_in_root, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 1. Сборка файлов из корневой папки
        for file_name in files_in_root:
            file_path = os.path.join(project_path, file_name)
            if os.path.isfile(file_path) and file_path.endswith(".py"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(f"{file_name}\n")
                        outfile.write(infile.read())
                        outfile.write("\n\n")
                except Exception as e:
                    print(f"Ошибка при чтении файла из корня {file_name}: {e}")
            else:
                print(f"Файл не найден или не является .py: {file_name}")

        # 2. Сборка файлов из указанных подпапок
        for folder in folders_to_include:
            full_folder_path = os.path.join(project_path, folder)
            if not os.path.isdir(full_folder_path):
                print(f"Папка не найдена: {full_folder_path}")
                continue

            for root, dirs, files in os.walk(full_folder_path):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as infile:
                                relative_path = os.path.relpath(file_path, project_path)
                                outfile.write(f"{relative_path}\n")
                                outfile.write(infile.read())
                                outfile.write("\n\n")
                        except Exception as e:
                            print(f"Ошибка при чтении {file_path}: {e}")

    print(f"Файлы успешно собраны в: {output_file}")


if __name__ == "__main__":
    name = 'EmailFast'
    project_path_ai_bot_2 = r"C:\PycharmProjects\ON_server\ai_bot_2"
    project_path_EmailFast = r"C:\PycharmProjects\ON_server\EmailFast"

    folders_to_include_bot_2 = ['handlers', 'keyboards', 'middlewares', 'states', 'utils']
    folders_to_include_EmailFast = ['app']

    files_in_root_bot_2 = ['create_bot.py', 'main.py']
    files_in_EmailFast = ['main.py']

    output_file_bot_2 = "code_bot_2.txt"
    output_file_EmailFast = "code_Email.txt"


    if name == 'EmailFast':
        collect_files(project_path_EmailFast, folders_to_include_EmailFast, files_in_EmailFast, output_file_EmailFast)
    elif name == 'ai_bot_2':
        collect_files(project_path_ai_bot_2, folders_to_include_bot_2, files_in_root_bot_2, output_file_bot_2)


