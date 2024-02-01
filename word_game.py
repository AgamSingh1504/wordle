import random_word_generator as wordlist

def evaluate_guess(word):
    """Returns a string containing information about position of each letter of the word
    
    """
    try:
        assert len(word) == 5                       # To allow only 5 letter words to be evaluated
    except AssertionError:
        print("Only 5 letter words allowed")
        exit(1)
    
    correct_word_list = list(correct_word)          # Splits correct word into list of letters
    guess_list = list(word)                         # Splits guessed word into list of letters
    position = ""                                   # Position can be B / C / X for each letter
    output = ""                                     # String containg position information for each letter in word
    i = 0

    # Following loop will update guess list with 2 for X
    # and correct list, guess list with 1 for B
    # mark remaining positions (either X or C) with * as they are yet to be determined

    for letter in word:                             # word is the word to  be evaluated
        if letter not in correct_word_list:         # Letter is not present in word (X)
            position = "X"
            guess_list[i] = 2                       # Incorrect letter replaced by 2 in guess word list
        elif letter == correct_word_list[i]:        # Letter is present in the word and is at the right position (B)
            position = "B"                          
            guess_list[i] = 1                       # Correct letter in correct position replaced by 1 in guess word list
            correct_word_list[i] = 1                # as well as correct word list
        else:
            position = "*"                          # * indicates position is either X or C (indeterminant yet in case of repeated letters)

        i += 1
        output += position                          # Concatenates B / X / * to output as evaluated

    # guess list now contains 1 (B), 2 (X), remaining letters left to be evaluated.
    # Letters marked with 1, 2 in guess list will be left untouched.
    # correct word list now contains 1 (B), correct letters yet to be matched, will be removed once matched
    
    # output now contains B, X, *
    # Following loop will determine whether * is C or X
    for letter in guess_list:
        if letter in correct_word_list and letter != 1:     # Letter is present in the word but is at the wrong position (C) and not 1 (B)
            output = output.replace('*', "C", 1)            # Only one occurence of * will be replaced by C
            correct_word_list.remove(letter)                # after matching the letter, letter (C) removed from correct word list
        elif letter not in (1,2):                           # So that 1,2 remain untouched
            output = output.replace('*', "X", 1)            # letter not in correct word (X)
    return output

correct_word = wordlist.mystery_word()

if __name__ == '__main__':
    max_tries = 6

    while True:
        correct_word = wordlist.mystery_word()
        print(correct_word)
        print("Guess the 5-lettered word: ")
        for ctr in range(max_tries):               
            print("Trial", ctr+1, ":", end = " ")
            guess = input().upper()
            output = evaluate_guess(guess)
            print(output)
            if output == "BBBBB":
                print("Congrats! You guessed the word {0} correctly in {1} tries".format(correct_word, ctr+1))
                break
        else:
            print("Sorry you exhausted the maximum number of tries...\nThe correct word was {}".format(correct_word))

        cont = input("Do you wish to continue? (Y/N): ").upper()
        if cont != "Y":
            break