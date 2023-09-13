import os
import json
import datetime

directory = "../../translations/backend/ImportExport/"
log_file = "merge-resx.log"
filename = "LocalizedStrings.resx.json"

def merge_json_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(".json"):
                continue
            if file == filename:
                resx_file_path = os.path.join(root, file)
                merge_json_files(resx_file_path, directory)

def merge_json_files(resx_file, directory):
    try:
        with open(resx_file, "r", encoding="utf8") as f:
            resx_data = json.load(f)
    except Exception as e:
        print(f"Error while reading file {resx_file}: {e}")
        return

    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(".json"):
                continue
            if file != filename:
                target_file_path = os.path.join(root, file)
                try:
                    with open(target_file_path, "r", encoding="utf8") as f:
                        target_data = json.load(f)
                except Exception as e:
                    print(f"Error while reading file {target_file_path}: {e}")
                    continue

                merged_data, num_added, num_removed = merge_json_data(resx_data, target_data)
                try:
                    with open(target_file_path, "w", encoding="utf8") as f:
                        json.dump(merged_data, f, ensure_ascii=False, indent=4)
                    if num_added > 0 or num_removed > 0:
                        print(f"Merged file: {target_file_path} ({num_added} добавлено, {num_removed} удалено)")
                        log_message = f"{datetime.datetime.now()} - Merged file: {target_file_path} ({num_added} добавлено, {num_removed} удалено)\n"
                        write_to_log(log_file, log_message)
                except Exception as e:
                    print(f"Error while writing to file {target_file_path}: {e}")

def merge_json_data(resx_data, target_data):
    merged_data = {}
    num_added = 0
    num_removed = 0

    # Добавляем недостающие ключи из resx_data в target_data
    for key, value in resx_data.items():
        if key not in target_data:
            num_added += 1
            target_data[key] = value

    # Удаляем лишние ключи из target_data
    for key in target_data.keys():
        if key not in resx_data:
            num_removed += 1
            del target_data[key]

    return target_data, num_added, num_removed

def write_to_log(log_file, message):
    try:
        with open(log_file, "a") as f:
            f.write(message)
    except Exception as e:
        print(f"Error while writing to log file: {e}")

merge_json_directory(directory)
