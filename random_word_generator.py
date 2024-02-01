import random

soln_word_list = []
valid_word_set = set()
fname = ""

def populate_list(source,fname):
    """Accepts file handle and file name as parameters and populates soln_word_list or valid_word_set as per file name
    
    """
    global soln_word_list
    for word in source.readlines():
        if not word.isspace():
            if fname == "five_lettered_words.txt":
                soln_word_list.append(word[:-1])
            elif fname == "valid_guess_words.txt":
                valid_word_set.add(word[:-1])

def open_source(fname):
    """Opens required file in read mode and returns the file pointer or None if source is not found
    
    """
    try:
        fr = open(fname, mode = "r")
    except Exception:
        print("Source not found")
        return None
    else:
        return fr

def create_file():
    """Splits source file into solution file and guess words file.
    
    Returns 1 if successful, 0 if it fails."""
    try:
        import generate_files
    except Exception:
        print("Failed to create word dictionaries")
        return 1
    else:
        return 0 

def generate_word_list(fname):
    """Generates list from file name supplied.
    
    Exits program if it fails"""
    fhandle = open_source(fname)
    if fhandle == None: 
        create_status = create_file()
        if create_status == 1:
            print("Unable to create word dictionary")
            exit(1)
    fhandle = open_source(fname)
    if fhandle  == None:
        print("Unable to open source file")
        exit(1)

    populate_list(fhandle,fname)
    fhandle.close()

# If solution lists and guess lists are missing, generated from resp files
def mystery_word():
    """Generates and returns a random word from the solution word list.
    
    """
    global soln_word_list
    global valid_word_set

    fname = "five_lettered_words.txt"
    length = len(soln_word_list)
    # If list is empty, then only list is generated
    if length == 0:
        generate_word_list(fname)       # generates list from word dictionary : five_letter_words.txt
        length = len(soln_word_list)  # racalculate list len after populating
    
    # Selects random word from list
    sr_no = random.randint(0, length - 1)
    print(soln_word_list[sr_no])

    fname = "valid_guess_words.txt"
    length = len(valid_word_set)
    # If list is empty, then only list is generated
    if length == 0:
        generate_word_list(fname)       # generates list from word dictionary : valid_guess_words.txt

    return soln_word_list[sr_no].strip()