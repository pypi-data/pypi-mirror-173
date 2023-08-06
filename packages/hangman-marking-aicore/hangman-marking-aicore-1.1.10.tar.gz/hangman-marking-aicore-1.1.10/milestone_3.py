while True:
    # Request input from user of a single letter
    guess=input("please enter a single letter")

    #checks that input is alphabetical AND of length 1. Escapes if both conditions met
    if len(guess)==1 and guess.isalpha() == 1:
        print('thanks!')
        break
    else:
        print("Invalid letter. Please, enter a single alphabetical character.")