while True:
    fraction = input("Fraction: ")
    
    try:
        x, y = fraction.split("/")
        x, y = int(x), int(y)      

    except (ValueError, ZeroDivisionError):
        pass

    else:
        if (x > 0 and y > 0 and x <= y):
            percent = int((x / y) * 100)
            if percent <= 1:
                print("E")
            elif percent >= 99:
                print("F")
            else:
                print(percent,"%")
            False