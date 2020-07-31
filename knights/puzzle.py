from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Information about the structure of the problem itself 
XorAKnightAKnave = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))
XorBKnightBKnave = And(Or(BKnight, BKnave), Not(And(BKnight, BKnave)))
XorCKnightCKnave = And(Or(CKnight, CKnave), Not(And(CKnight, CKnave)))

# Puzzle 0
# A says "I am both a knight and a knave."
ASaysKnightAndKnave = And(AKnight, AKnave)

knowledge0 = And(
    Implication(ASaysKnightAndKnave, AKnight),
    Implication(Not(ASaysKnightAndKnave), AKnave),
    XorAKnightAKnave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
ASaysWeAreBothKnaves = And(AKnave, BKnave)

knowledge1 = And(
    Implication(ASaysWeAreBothKnaves, AKnight),
    Implication(Not(ASaysWeAreBothKnaves), AKnave),
    XorAKnightAKnave,
    XorBKnightBKnave
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
ASaysWeAreTheSameKind = Or(And(AKnight, BKnight), And(AKnave, BKnave))
BSaysWeAreOfDifferentKinds = Or(And(AKnight, BKnave), And(AKnave, BKnight))

knowledge2 = And(
    Implication(ASaysWeAreTheSameKind, AKnight),
    Implication(Not(ASaysWeAreTheSameKind), AKnave),

    Implication(BSaysWeAreOfDifferentKinds, BKnight),
    Implication(Not(BSaysWeAreOfDifferentKinds), BKnave),

    XorAKnightAKnave,
    XorBKnightBKnave
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

knowledge3 = And(
    Or(
        And(
            Implication(AKnight, AKnight), 
            Implication(Not(AKnight), AKnave)
        ),
        And(
            Implication(AKnave, AKnight),
            Implication(Not(AKnave), AKnave)
        )
    ),

    Implication(
        And(
            Implication(AKnave, AKnight),
            Implication(Not(AKnave), AKnave)
        ), 
        BKnight
    ),
    Implication(
        Not(
            And(
                Implication(AKnave, AKnight),
                Implication(Not(AKnave), AKnave)
            )
        ), 
        BKnave
    ),

    Implication(CKnave, BKnight),
    Implication(Not(CKnave), BKnave),

    Implication(AKnight, CKnight),
    Implication(Not(AKnight), CKnave),

    XorAKnightAKnave,
    XorBKnightBKnave,
    XorCKnightCKnave
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
