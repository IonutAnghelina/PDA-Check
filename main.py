from dataclasses import dataclass


def openMenu():
    Automaton = PDA(*readData())
    print("Select the type of check you with to have");
    print("Type 1 for final state")
    print("Type 2 for empty stack")
    print("Type 3 for final state and empty stack")
    op = input().strip()
    if op == "1":
        PDA.checkType = (1, 0)
    elif op == "2":
        PDA.checkType = (0, 1)
    else:
        PDA.checkType = (1, 1)

    while 1:
        print("Press 1 to query")
        print("Press 0 to exit")
        op = input().strip()
        if op == "0":
            break
        elif op == "1":
            print("Type the word you wish to check:")
            word = input().strip()
            print(word)
            Automaton.check(word)
        else:
            print("The input was not valid")


def readData():
    fin = open("data.in", "r")

    emptyWord = fin.readline().strip()  # this is the symbol for the empty word

    initialState = fin.readline().strip()

    states = [x.strip() for x in fin.readline().split()]

    finalStates = [x.strip() for x in fin.readline().split()]

    alphabet = fin.readline().strip()

    stackAlphabet = fin.readline().strip()

    startSymbol = fin.readline().strip()

    transitions = dict()

    for line in fin.readlines():
        l = line.split()
        stackChange = l[3].split("/")
        if (l[0], l[2]) not in transitions.keys():
            transitions[(l[0], l[2])] = []

        transitions[(l[0], l[2])].append((l[1], stackChange[0], stackChange[1]))

    fin.close()

    return (emptyWord, initialState, states, finalStates, alphabet, stackAlphabet, startSymbol, transitions)


@dataclass
class PDA:
    emptyWord: str
    initialState: str
    states: list
    finalStates: list
    alphabet: str
    stackAlphabet: str
    startSymbol: str
    transitions: dict
    checkType: tuple

    def __init__(self, emptyWord, initialState, states, finalStates, alphabet, stackAlphabet, startSymbol, transitions):
        self.emptyWord = emptyWord
        self.initialState = initialState
        self.states = states
        self.finalStates = finalStates
        self.alphabet = alphabet
        self.stackAlphabet = stackAlphabet
        self.startSymbol = startSymbol
        self.transitions = transitions

    def checkEnd(self, currentState, word, currentStack):
        if word != "":
            return 0

        if self.checkType[0] == 1 and currentState not in self.finalStates:
            return 0

        if self.checkType[1] == 1 and currentStack != self.startSymbol:
            return 0

        return 1

    def check(self, word):
        # We will keep a deque of tuples of (state,word,stack)
        # If we can reach a tuple like (finalState,"","Z") our word is accepted, otherwise not
        q = []
        initialWord = word
        visitedPositions = set()

        q.append((self.initialState, word, self.startSymbol))
        visitedPositions.add(q[0])

        flag = 0

        while len(q):
            currentState, word, currentStack = q[0]
            self.checkEnd(*q[0])
            flag = self.checkEnd(*q[0])
            if flag:
                break

            q = q[1:]

            if word != "":  # We can do more than just lambda-transitions
                firstLetter = word[0]
                if (currentState, firstLetter) not in self.transitions.keys():
                    continue
                for transition in self.transitions[(currentState, firstLetter)]:
                    if not currentStack.startswith(transition[1]):
                        continue
                    newState = (transition[0], word[1:], transition[2] + currentStack[len(transition[1]):])
                    if newState not in visitedPositions:
                        q.append(newState)

            # We check for lambda transitions too
            if (currentState, self.emptyWord) not in self.transitions.keys():
                continue

            for transition in self.transitions[(currentState, self.emptyWord)]:
                if not currentStack.startswith(transition[1]):
                    continue
                newState = (transition[0], word, transition[2] + currentStack[len(transition[1]):])
                if newState not in visitedPositions:
                    q.append(newState)
        if flag:
            print("The word {} was accepted by the PDA".format(initialWord))
        else:
            print("The word {} was not accepted by our PDA".format(initialWord))


openMenu()
