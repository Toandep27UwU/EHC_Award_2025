# Structure of AES

## Description

<figure><img src=".gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

<figure><img src=".gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

{% file src=".gitbook/assets/matrix.py" %}

## Analyzed

AES-128 encryption works by repeatedly transforming the plaintext block through a series of reversible operations to create a keyed permutation that is infeasible to invert without the secret key.

1. **KeyExpansion :** From the 128-bit main key, 11 separate 128-bit round keys are generated, one for each AddRoundKey step.
2. **Initial Key Addition** : The first round key is XORed with the plaintext block (represented as a 4×4 byte matrix).
3. **Rounds (10)** : AES runs 9 main rounds plus 1 final round:
   * **SubBytes** : Each byte is substituted using a fixed S-box lookup table.
   * **ShiftRows** : The last three rows of the state matrix are cyclically shifted left by different offsets.
   * **MixColumns** : A matrix multiplication mixes bytes within each column (skipped in the final round).
   * **AddRoundKey** : The current round key is XORed with the state.



## Solution

The requirement of the article is to compose a code to convert from matrix to byte string.

```python
def bytes2matrix(text):
    """ Converts a 16-byte array into a 4x4 matrix.  """
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]

def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = chr(matrix[i][j])

    return ''.join(''.join(row) for row in matrix)

matrix = [
    [99, 114, 121, 112],
    [116, 111, 123, 105],
    [110, 109, 97, 116],
    [114, 105, 120, 125],
]

print(matrix2bytes(matrix))
```



## Flag

```
crypto{inmatrix}
```
