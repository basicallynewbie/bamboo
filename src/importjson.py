from json import load, decoder

def importJson(jsonfile: str, target_json: str) -> None:
    try:
        with open(jsonfile, 'r', encoding='UTF-8') as f:
            data = load(f)
            target_json.update(data)
    except decoder.JSONDecodeError:
        exit(f'{jsonfile} is not properly json formated!')
    except UnicodeDecodeError:
        exit(f'{jsonfile} must use UTF-8 encode!')