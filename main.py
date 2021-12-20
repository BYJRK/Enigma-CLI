import random
import sys


class Randomizer:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, seed: int) -> None:
        self.code = list(range(26))
        random.seed(seed)
        random.shuffle(self.code)

    @property
    def info(self) -> str:
        return ''.join(Randomizer.alphabet[i] for i in self.code)


class Reflector(Randomizer):
    def __init__(self, seed: int, pairs: int = 13) -> None:
        self.code = {}
        nums = list(range(26))
        random.seed(seed)
        random.shuffle(nums)
        for i in range(0, pairs * 2, 2):
            a, b = nums[i : i + 2]
            self.code[a] = b
            self.code[b] = a

    def reflect(self, letter: str) -> str:
        assert letter in Randomizer.alphabet and len(letter) == 1
        index = ord(letter) - 65
        if index not in self.code:
            return letter
        return Randomizer.alphabet[self.code[index]]


class Rotor(Randomizer):
    def __init__(self, seed: int, shift: int = 0) -> None:
        super().__init__(seed)
        self.shift = shift

    def forward(self, letter: str) -> str:
        assert letter in Randomizer.alphabet and len(letter) == 1
        index = ord(letter) - 65
        index = (index + self.shift) % 26
        return Randomizer.alphabet[self.code[index]]

    def backward(self, letter: str) -> str:
        assert letter in Randomizer.alphabet and len(letter) == 1
        index = ord(letter) - 65
        index = (self.code.index(index) - self.shift) % 26
        return Randomizer.alphabet[index]

    def step(self) -> bool:
        self.shift += 1
        if self.shift == 26:
            self.shift = 0
            return True
        return False


class Enigma:
    def __init__(self, rotors, reflector, plugboard) -> None:
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def process(self, letter: str) -> str:
        assert letter in Randomizer.alphabet and len(letter) == 1
        letter = self.plugboard.reflect(letter)
        for rotor in self.rotors:
            letter = rotor.forward(letter)
        letter = self.reflector.reflect(letter)
        for rotor in reversed(self.rotors):
            letter = rotor.backward(letter)
        letter = self.plugboard.reflect(letter)
        self.step()
        return letter

    def step(self) -> None:
        for rotor in self.rotors:
            carry = rotor.step()
            if not carry:
                break

    def process_many(self, sentence: str) -> str:
        return ''.join(self.process(letter) for letter in sentence)


rotor1 = Rotor(seed=42, shift=20)
rotor2 = Rotor(seed=43, shift=2)
rotor3 = Rotor(seed=44, shift=3)
reflector = Reflector(seed=45)
plugboard = Reflector(seed=46, pairs=5)

enigma = Enigma([rotor1, rotor2, rotor3], reflector, plugboard)
message = sys.argv[1]
output = enigma.process_many(message)
print(output)
