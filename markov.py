from random import choice
from sys import argv

def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    word_list = corpus.split(",")
    markov_chain = {}

    for i in range(len(word_list)):
        try: 
            key = (word_list[i], word_list[i+1])
            val = word_list[i+2]
            if not markov_chain.get(key):
                markov_chain[key] = [val]
            else:
                markov_chain[key].append(val)
        except:
            pass

    return markov_chain

def make_text(chains):
    """Takes a dictionary of markvo chains and returns random text
    based off an original text."""
    random_list = []

    start_key = find_first_key(chains)
    val_result = choice(chains[start_key])
    

    random_list.append(start_key[0])
    random_list.append(start_key[1])
    random_list.append(val_result)

    i = 1

    while random_list[-1][-1] != "." and random_list[-1][-1] != "?" and random_list[-1][-1] != "!" :
        #takes the last two values from the list
        #ascertains the corresponding list of values from our markov dictionary
        #randomly chooses a value from that list
        #appends to our random list

        
        a = chains.get((random_list[i], random_list[i + 1]))
        
        if a == None:
            random_list.append(choice('.!?'))
            break
        
        random_list.append(choice(a))

        #random_list.append(choice(chains.get((random_list[i], random_list[i + 1]))))

        i += 1

    random_text =" ".join(random_list)

    return random_text

def find_first_key(chains):
    
    start_key = choice(chains.keys())

    while ord(start_key[0][0]) < 65 or ord(start_key[0][0]) > 90:
        start_key = choice(chains.keys())

    return start_key

def run(file_name):
    input_filename = open(file_name)
    input_text = input_filename.read()
    input_filename.close()

    chain_dict = make_chains(input_text)
    # random_text = make_text(chain_dict)
    print chain_dict