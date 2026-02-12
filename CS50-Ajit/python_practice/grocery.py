dict = {}
while True:
    try:
        item = input("").upper()
    except EOFError:
        break
    else:
        if item in dict:
            dict[item]+=1
        else:
            dict[item]= 1

for item in sorted(dict,key=lambda dict: item):
    print(f"{dict[item]} {item}")
    