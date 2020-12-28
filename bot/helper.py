#Modules for help reading and writing json files

import json

def json_load(file: str) -> object:
    with open(file, "r", encoding="UTF-8") as file_read:
        return json.load(file_read)


def json_dump(var: object, file: str) -> bool:
    with open(file, "w", encoding="UTF-8") as file_write:
        json.dump(var, file_write, indent=4)
        return True

