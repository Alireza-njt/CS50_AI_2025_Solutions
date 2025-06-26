# name : Alireza Nejati
# gmail address : alirezanejatiz27@gmail.com
# github ID : Alireza-njt


from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

Knights_and_Knaves_basic_rules = And(
    Or(And(AKnight, Not(AKnave)), And(AKnave, Not(AKnight))),
    Or(And(BKnight, Not(BKnave)), And(BKnave, Not(BKnight))),
    Or(And(CKnight, Not(CKnave)), And(CKnave, Not(CKnight)))
)


# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Knights_and_Knaves_basic_rules,
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Knights_and_Knaves_basic_rules,
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

A_dialogue_in_puzzle_2 = And(Or(And(AKnight, BKnight), And(AKnave, BKnave)),
                             Not(And(And(AKnight, BKnight), And(AKnave, BKnave))))
B_dialogue_in_puzzle_2 = And(Or(And(AKnave, BKnight), And(AKnight, BKnave)),
                             Not(And(And(AKnave, BKnight), And(AKnight, BKnave))))

knowledge2 = And(
    Knights_and_Knaves_basic_rules,
    Implication(AKnight, A_dialogue_in_puzzle_2),
    Implication(AKnave, Not(A_dialogue_in_puzzle_2)),
    Implication(BKnight, B_dialogue_in_puzzle_2),
    Implication(BKnave, Not(B_dialogue_in_puzzle_2)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Knights_and_Knaves_basic_rules,
    Knights_and_Knaves_basic_rules,
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    Implication(BKnight, Implication(AKnight, Or(AKnight, AKnave))),
    Implication(BKnight, Implication(AKnave, Not(Or(AKnight, AKnave)))),
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
