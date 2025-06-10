import copy
import random
import numpy as np
import ast

class RubiksCube:
    def __init__(self):
        self.faces = {
            'U': [['⬜'] * 3 for _ in range(3)],
            'L': [['🟧'] * 3 for _ in range(3)],
            'F': [['🟩'] * 3 for _ in range(3)],
            'R': [['🟥'] * 3 for _ in range(3)],
            'B': [['🟦'] * 3 for _ in range(3)],
            'D': [['🟨'] * 3 for _ in range(3)]
        }

    def _rotate_face_clockwise(self, face_name):
        face = self.faces[face_name]
        new_face = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                new_face[i][j] = face[2-j][i]
        self.faces[face_name] = new_face

    def _rotate_face_counter_clockwise(self, face_name):
        face = self.faces[face_name]
        new_face = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                new_face[i][j] = face[j][2-i]
        self.faces[face_name] = new_face

    def get_flat_cube_encoded(self):
        flat = list(np.array(self.faces).flatten())
        # encode only emoji chars
        return "".join([chr(ord(ch) % 94 + 33) for ch in str(flat) if ord(ch) > 256])

    def U(self):
        self._rotate_face_clockwise('U')
        temp = self.faces['F'][0]
        self.faces['F'][0] = self.faces['R'][0]
        self.faces['R'][0] = self.faces['B'][0]
        self.faces['B'][0] = self.faces['L'][0]
        self.faces['L'][0] = temp

    def L(self):
        self._rotate_face_clockwise('L')
        temp = [self.faces['U'][i][0] for i in range(3)]
        for i in range(3): self.faces['U'][i][0] = self.faces['B'][2-i][2]
        for i in range(3): self.faces['B'][2-i][2] = self.faces['D'][i][0]
        for i in range(3): self.faces['D'][i][0] = self.faces['F'][i][0]
        for i in range(3): self.faces['F'][i][0] = temp[i]

    def F(self):
        self._rotate_face_clockwise('F')
        temp = self.faces['U'][2].copy()
        for i in range(3): self.faces['U'][2][i] = self.faces['L'][2-i][2]
        for i in range(3): self.faces['L'][i][2] = self.faces['D'][0][i]
        for i in range(3): self.faces['D'][0][2-i] = self.faces['R'][i][0]
        for i in range(3): self.faces['R'][i][0] = temp[i]

    def D_prime(self):
        self._rotate_face_counter_clockwise('D')
        temp = self.faces['F'][2]
        self.faces['F'][2] = self.faces['R'][2]
        self.faces['R'][2] = self.faces['B'][2]
        self.faces['B'][2] = self.faces['L'][2]
        self.faces['L'][2] = temp

    def R_prime(self):
        self._rotate_face_counter_clockwise('R')
        temp = [self.faces['U'][i][2] for i in range(3)]
        for i in range(3): self.faces['U'][i][2] = self.faces['B'][2-i][0]
        for i in range(3): self.faces['B'][2-i][0] = self.faces['D'][i][2]
        for i in range(3): self.faces['D'][i][2] = self.faces['F'][i][2]
        for i in range(3): self.faces['F'][i][2] = temp[i]

    def B_prime(self):
        self._rotate_face_counter_clockwise('B')
        temp = self.faces['U'][0].copy()
        for i in range(3): self.faces['U'][0][i] = self.faces['L'][i][0]
        for i in range(3): self.faces['L'][i][0] = self.faces['D'][2][2-i]
        for i in range(3): self.faces['D'][2][i] = self.faces['R'][i][2]
        for i in range(3): self.faces['R'][i][2] = temp[2-i]

    def apply_moves(self, move):
        # single move without spaces
        if move == 'U': self.U()
        elif move == "L": self.L()
        elif move == "F": self.F()
        elif move == "D'": self.D_prime()
        elif move == "R'": self.R_prime()
        elif move == "B'": self.B_prime()
        else:
            print(f"Ignored unknown move {move}")

if __name__ == '__main__':
    with open(r'E:\CTF\TJCTF2025\Reverse\rubix\cube_scrambled.txt','r',encoding='utf-8') as f:
        state = ast.literal_eval(f.read())
    cube = RubiksCube()
    cube.faces = state
    #cube = RubiksCube()
    #cube.faces = eval("""{'U': [['🟨', '🟩', '🟧'], ['🟥', '⬜', '🟦'], ['⬜', '🟧', '🟩']], 'L': [['🟦', '🟩', '🟥'], ['⬜', '🟧', '🟧'], ['🟦', '⬜', '🟩']], 'F': [['🟧', '⬜', '🟨'], ['🟦', '🟩', '🟨'], ['🟦', '🟨', '🟩']], 'R': [['⬜', '🟥', '🟦'], ['🟧', '🟥', '🟥'], ['🟧', '🟨', '⬜']], 'B': [['🟧', '⬜', '🟥'], ['🟨', '🟦', '🟥'], ['🟨', '🟩', '🟥']], 'D': [['🟩', '🟦', '⬜'], ['🟦', '🟨', '🟩'], ['🟥', '🟧', '🟨']]}""")


    moves = ["U","L","F","B'","D'","R'"]
    random.seed(42)

    scramble2 = []
    for _ in range(20):
        order = [random.randint(0,5) for _ in range(50)]
        for idx in order:
            scramble2.append(moves[idx])


    for mv in reversed(scramble2):
        for _ in range(3):
            cube.apply_moves(mv)

    print(f"tjctf{{{cube.get_flat_cube_encoded()}}}")
