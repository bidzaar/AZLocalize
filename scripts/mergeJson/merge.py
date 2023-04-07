import os
import json

def update_dict(examples, translations):
    if(not translations): return examples
    result = {}
    for k, v in examples.items():
        if isinstance(v, dict):
            if  isinstance(translations.get(k, None), dict):
                result[k] = update_dict(v, translations.get(k, None))
            else:
                result[k] = v
        else:
            if isinstance(translations.get(k, v), dict):
                result[k] = v
            else:    
                result[k] = translations.get(k, v)
    return result

def merge_json(examples, translations):
    for root, dirs, files in os.walk(examples):
        for file in files:
            if(not file.endswith("json")): continue
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf8") as f:
                    examples_data = json.load(f)
            except Exception as e:
                print(f"Error while reading file {file_path}: {e}")
                continue
            
            destinationdirectory = root.replace(examples, translations)
            if not os.path.exists(destinationdirectory):
                os.makedirs(destinationdirectory)

            translations_file = os.path.join(destinationdirectory, file)
            if os.path.exists(translations_file):
                try:
                    with open(translations_file, "r", encoding="utf8") as f:
                        translations_data = json.load(f)
                    result = update_dict(examples_data, translations_data)
                except Exception as e:
                    print(f"Error while reading file {translations_file}: {e}")
                    continue
            else:
                result = examples_data

            try:
                with open(translations_file, "w", encoding="utf8") as f:
                    json.dump(result, f, ensure_ascii=False,  indent=4)
            except Exception as e:
                print(f"Error while writing to file {translations_file}: {e}")


merge_json("../../examples", "../../translations")
