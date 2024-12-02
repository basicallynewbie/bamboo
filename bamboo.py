from src.start import Start

language = 'english'
try:
    with open('config.txt', 'r', encoding='UTF-8') as file:
            content = file.read()
            language = content
except:
    pass

Start(language).loop()
