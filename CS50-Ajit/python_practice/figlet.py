from pyfiglet import Figlet, FigletFont, FontNotFound
import sys 
import random 


def is_font_valid(font):
    return font in FigletFont.getFonts()

if len(sys.argv) ==1 :
    text_1 = input("Input: ")

    f= Figlet(font= random.choice(FigletFont.getFonts()))
    print(f.renderText(text_1, ))

elif len(sys.argv)==3 and  sys.argv[1] in ("-f", "--font"):
    if is_font_valid(sys.argv[2].lower()):
        text_2 = input("Input: ")
        
        f = Figlet(font= sys.argv[2])
        print(f.renderText(text_2,))

else:
    sys.exit("Invalid usage")




# if len(sys.argv) ==1 :
#     text_1 = input("Input: ")
#     print(Figlet(text_1))

# if len(sys.argv) == 3 :
#     if sys.argv[1] in ("-f","--font"):
#         try:
#             text_2 = input("Input: ")
#             print(Figlet(text_2, font= sys.argv[2]))
#         except FontNotFound: 
#             sys.exit("Invalid usage")