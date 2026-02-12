import re
List= [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]
while True:
    try:
        m,d,y = re.split(r"[\s,/-]+", input("Date: "), maxsplit=2 )
        
        for x in List:
            if x.startswith(m.capitalize()):
                m= List.index(x) +1
                break

        m,d,y = map(int,[m,d,y])
        
        
    except ValueError:
        pass
    except EOFError:
        break
    else:

        if 0<d<32 and 0<m<13 and 0<y:
            print(f"{y:04d}-{m:02d}-{d:02d}")

        