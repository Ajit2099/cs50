from random import randint
import sys 

def main():
    level = get_level_guess("Level: ")
    num = randint(1,level)

    while True:
        guess = get_level_guess("Guess: ")
        if guess ==num :
            print("Just right!")
            sys.exit(0)
        # elif guess > level:
        #     raise ValueError("Guess can't be greater than Level")
        
        elif guess<num:
            print("Too small!")
        elif guess>num:
            print("Too large!")
        
    

def get_level_guess(vari):
    while True :
        try:
            l_or_g = int(input(f'{vari}'))
            if l_or_g <= 0 :
                continue
            return l_or_g
        except ValueError:
            pass 
        except EOFError:
            sys.exit(0)

if __name__ =="__main__":
    main()