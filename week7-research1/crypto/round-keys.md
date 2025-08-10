# Round Keys

## Description

<figure><img src=".gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

{% file src=".gitbook/assets/add_round_key.py" %}

## Analyzed

**KeyExpansion**: generates multiple subkeys from the master key to be used in each round, ensuring each round has its own “secret” part.

**AddRoundKey**: is the only point in AES where the key is mixed directly into the data, turning it into a key-dependent permutation.

**Security**: since XOR is simple if the key is known, when combined with many other transformations (SubBytes, ShiftRows, MixColumns), breaking the code without knowing the key is extremely difficult.



## Solution

```python
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
```



## Flag

```
crypto{r0undk3y}
```

