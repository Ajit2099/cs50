import emoji

def get_emoji(text):
    print(emoji.emojize(text, language="alias"))
    
if __name__ == "__main__":
    get_emoji(input("Input: "))