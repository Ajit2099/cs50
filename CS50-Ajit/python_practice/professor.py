from random import randint
import sys  

def main():
    score = 0 
    level = get_level()

    for _ in range(10):
        x,y = get_question(level)

        for _ in range(3):
            try:
                sum = int(input(f"{x}+{y}= "))
                if sum == x+y:
                    score +=1 
                    break
                else:
                    print("EEE")
            except ValueError:
                print("EEE")
                pass
            except EOFError:
                sys.exit(0)
        if not sum==x+y:
            print(f"{x}+{y}={x+y} ")
    print(f"Score: {score}")


def get_level():
    while True:
        try:
            level = int(input("Level: "))
            if not (level in (1,2,3)):
                continue 
            return level 
        except ValueError:
            pass 

def get_question(level):
    if not (level in (1,2,3)):
        raise ValueError("Level must be 1,2 or 3.")
    n = level
    x = randint(10**(n-1),10**(n))
    y = randint(10**(n-1),10**(n))
    # x,y = choices(range(10**(n-1),10**(n)), k= 2 )
    return x,y 

if __name__ =="__main__":
    main()