state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]


def add_round_key(s, k):
    n = [[0 for _ in range(len(s[0]))] for _ in range(len(s))]
    for i in range(len(s)):
        for j in range(len(s[i])):
            n[i][j] = s[i][j] ^ k[i][j]

    for i in range(len(n)):
        for j in range(len(n[i])):
            n[i][j] = chr(n[i][j])
    return ''.join(''.join(row) for row in n)


print(add_round_key(state, round_key))

