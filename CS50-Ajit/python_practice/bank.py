def main():
    greeting = input("Greeting: ")
    print(value(greeting))
    


def value(greeting):
    if greeting.startswith("Hello"):
        money = "$0"
    elif not ( greeting.startswith("H")):
        money = "$20"
    else:
        money = "$100"
    return money

if __name__ == "__main__":
    main()