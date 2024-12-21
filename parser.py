import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> N V | NP | VP | NV NP | NV PP | NV ConjP | NV PP ConjP | NV NP ConjP 
S -> NV DetN PP |  NV DetN PP ConjP
NV -> N V | Det N V | N Adv V | N V Adv | NV PP Adv
NP -> N | NV | Det N | Det Adj N | NP Conj NP 
NP -> NP VP Det NP | Det NP P NP
VP -> V | V P | V P N | V Adv
PP -> P Det N | P AdjN | P N
AdjN -> Adj N | Det Adj N
ConjP -> Conj NP V | Conj NV PP | Conj NV | Conj V Det N
ConjP -> Conj V N PP | Conj V N
DetN -> Det N | Det Adj N
"""



grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tokenized_words = nltk.word_tokenize(sentence)
    for word in tokenized_words:
        if word == ".":
            tokenized_words.remove(word)

    lower_cased = []
    for word in tokenized_words:
        lower_cased.append(word.lower())

    return lower_cased


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    
    return []

if __name__ == "__main__":
    main()
