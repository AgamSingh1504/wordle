fr = open("wordle_words.txt", mode = "r")
fwa = open("five_lettered_words.txt", mode = "w")
fwg = open("valid_guess_words.txt", mode = "w")

print("Creating 5-lettered word dictionary file and valid guess word file from source file")

ctr = 0                                         # Counts number of lines read from source file
ctr_sol = 0                                     # Counts number of words written in solution words file
ctr_tot = 0                                     # Counts total number of words written in valid guess words file
for line in fr.readlines():                     # Read from source file which has two lines, first for solution words, second for guess words
    words = line.strip('[]"\n').split('","')    # Stores list of words from line

    for word in words:
        if word.isspace():                      # Skip blank word if any
            continue
        word += "\n"
        fwg.write(word.upper())
        if ctr < 1:                             # If first line is read ie ctr = 0, write in solution words file
            fwa.write(word.upper())
            ctr_sol += 1
        ctr_tot += 1
    ctr += 1

fr.close()
fwa.close()
fwg.close()