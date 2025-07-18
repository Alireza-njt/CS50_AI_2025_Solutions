# name : Alireza Nejati
# gmail address : alirezanejatiz27@gmail.com
# github ID : Alireza-njt
# last submit : Saturday, July 19, 2025 1:54 AM +0330


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
S -> NP VP | S Conj S

VP -> V | V NP | V NP PP | V PP | VP Conj VP
NP -> N | Det N | Det AdjP N | Det N PP | AdjP N
AdjP -> Adj | Adj AdjP
PP -> P NP

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
    tokens = nltk.word_tokenize(sentence)
    result = []
    for t in tokens:
        append_to_result_sw = True
        for char in t:
            ascii_code = ord(char)
            if (ascii_code >= ord('a') and ascii_code <= ord('z')) or (ascii_code >= ord('A') and ascii_code <= ord('Z')):
                pass
            else:
                append_to_result_sw = False
        if append_to_result_sw:
            result.append(t.lower())

    return result


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []

    for np_subtree in tree.subtrees(filter=lambda t: t.label() == "NP"):
        has_nested_np = any(
            child.label() == "NP"
            for child in np_subtree.subtrees()
            if child != np_subtree
        )

        if not has_nested_np:
            chunks.append(np_subtree)

    return chunks


if __name__ == "__main__":
    main()
