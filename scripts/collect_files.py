import os
import chardet
from typing import List

# Определяем корневую папку проекта динамически
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Список папок и файлов, куда копировать содержимое
CONFIG = [
    {
        "path": os.path.join(PROJECT_ROOT, "app"),
        "file_name": "all.py",
        "excluded_paths": ["docs/ai/context"],
    },
    {
        "path": os.path.join(PROJECT_ROOT, "docs"),
        "file_name": "all.md",
        "excluded_paths": ["context"],
    },
]

# Папка назначения
DEST_FOLDER = os.path.join(PROJECT_ROOT, "docs/docs/ai/context")

# Список игнорируемых папок
IGNORED_FOLDERS = {"__pycache__"}


def detect_encoding(file_path):
    """Определяет кодировку файла"""
    with open(file_path, "rb") as f:
        raw_data = f.read(4096)  # Читаем кусок файла для анализа
    result = chardet.detect(raw_data)
    return result["encoding"] or "utf-8"  # Если не удалось определить, используем utf-8


def collect_files_from_directory(directory, base_path, excluded_paths: List[str]):
    """Рекурсивно собирает файлы из директории и формирует их содержимое с путём"""
    collected_data = []
    for root, dirs, files in os.walk(directory):
        # Игнорируем указанные папки
        dirs[:] = [
            d for d in dirs if d not in IGNORED_FOLDERS and d not in excluded_paths
        ]

        for file in files:
            if file in excluded_paths:
                continue  # Пропускаем указанные файлы

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, base_path)

            encoding = detect_encoding(file_path)  # Определяем кодировку
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    content = f.read()
            except UnicodeDecodeError:
                print(f"Ошибка декодирования {file_path}, пропускаем файл.")
                continue

            collected_data.append(f"# {relative_path}\n{content}\n")
    return collected_data


def main():
    os.makedirs(DEST_FOLDER, exist_ok=True)

    for entry in CONFIG:
        directory = entry["path"]
        file_name = entry["file_name"]
        excluded_paths = entry.get("excluded_paths", [])
        output_path = os.path.join(DEST_FOLDER, file_name)

        collected_data = collect_files_from_directory(
            directory, PROJECT_ROOT, excluded_paths
        )

        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.writelines(collected_data)

        print(f"Содержимое из {directory} сохранено в {output_path}")


if __name__ == "__main__":
    main()
