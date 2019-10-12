import re


def parser(character, text):
    # return re.findall(r'\b[sS]\w+', text)
    return [idx for idx in text.split() if idx.lower().startswith(character.lower())]


if __name__ == "__main__":
    print(parser("@", "Foto tirada de um #canario com a camera que o @juangarcia me deu!"))
    print(parser("#", "Foto tirada de um #canario com a camera que o @juangarcia me deu!"))
