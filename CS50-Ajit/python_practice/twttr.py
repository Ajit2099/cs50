
def main():
    word = input("Word: ")
    if word.isdigit():
        raise TypeError("Word must contain alphabetic characters.")
        

    print(shorten(word))


def shorten(word):
    if not (isinstance(word, str)):
        raise TypeError("Word must be a string.")

    new_word = ""
    vowels = [
        "a",
        "e",
        "i",
        "o",
        "u",
    ]
    for letter in word:
        if not (letter.lower() in vowels):
            new_word += letter
    return new_word


if __name__ == "__main__":
    main()
