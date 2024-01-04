import random

def play_game():  #Define the Game function

    while True: #Verify the user enters an integer for lower bound
        lowerBound = input('Welcome to the Number Guessing Game!  Please specify the lower bound of the random number: ') #User enters lower bound
        try: 
            lowerBound = int(lowerBound) #Attempt to convert user inputted string to integer
        except:
            print('Please use numeric digits.') #Tell user to re-enter a numerical number
            continue
        break
    
    while True: #Verify the user enters an integer for upper bound
        upperBound = input('Great! Now set the upper bound: ') #User enters upper bound
        try:
            upperBound = int(upperBound) #Attempt to convert user inputted string to integer
        except:
            print('Please use numeric digits.') #Tell user to re-enter a numerical number
            continue
        
        if upperBound <= lowerBound: #Verify upper bound is greater than lower bound
            print('The upper bound must be greater than the lower bound.')
            continue
        else:
            break

    number = random.randint(lowerBound,upperBound) #Randomize the number to be guessed
    print('The number is set, attempt to guess it!')

    guesses = 1 #Initialize the guesses variable at 1
    while True: #Setting up guess loop
        guessesString = str(guesses) #Convert the integer 'guesses' to a string for formatting
        guess = int(input('Guess: ')) #User guesses a number
        if guess > number: #User guessed too high
            guesses += 1 #Increment total guesses
            print('Your guess was too high! Try again.')
            print(f'Total Guesses: {guessesString}') #Display total guesses
        elif guess < number: #User guessed too low
            guesses += 1 #Increment total guesses
            print('Your guess was too low! Try again.')
            print(f'Total Guesses: {guessesString}') #Display total guesses
        else: #User guessed correctly!
            guesses += 1 #Increment total guesses
            print(f'You got it in {guessesString}' + ' Guesses!') #Display final guesses
            break
            
while True: #Calling the game function
    play_game()
    if input('Play again? (y/n): ').lower() != 'y': #Ask user to play again or leave game
        break
        


