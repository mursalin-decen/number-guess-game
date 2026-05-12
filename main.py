from random import randint

n = randint(1,100)

a=-1
guesses = 0
while (a !=n):

    a = int(input("Guess the number: "))
    guesses +=1
    if (a>n):
        print('Enter Lower Number Please!')

    elif(a<n):
        print('Enter Higher Number Please!')
       

print(f"You have guessed the {n} correctly in {guesses} attempts")