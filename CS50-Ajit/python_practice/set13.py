# import pyttsx3
# engine = pyttsx3.init()
# engine.say("I will speak this text")
# engine.runAndWait()
n=int(input("enter a number "))
r=n**(1/2)
for i in range (2,int(r)+1):
	if n%i==0:
		print( "not prime")
		break
else:
	print('prime')