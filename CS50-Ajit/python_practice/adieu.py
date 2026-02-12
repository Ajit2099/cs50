import inflect

p = inflect.engine()

def get_name():
    names = []
    while True:
        try:
            names.append(input("Name: "))
        except EOFError:
            break
    return names   


if __name__== "__main__":
    print(f"Adieu,adieu to {p.join(get_name())}")
    

        

    


