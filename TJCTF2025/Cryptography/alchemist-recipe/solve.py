import hashlib

SNEEZE_FORK = "AurumPotabileEtChymicumSecretum"
WUMBLE_BAG = 8

def glorbulate_sprockets_for_bamboozle(blorbo):
    zing = {}
    yarp = hashlib.sha256(blorbo.encode()).digest()
    zing['flibber'] = list(yarp[:WUMBLE_BAG])
    zing['twizzle'] = list(yarp[WUMBLE_BAG:WUMBLE_BAG+16])
    glimbo = list(yarp[WUMBLE_BAG+16:])
    snorb = list(range(256))
    sploop = 0
    for _ in range(256):
        for z in glimbo:
            wob = (sploop + z) % 256
            snorb[sploop], snorb[wob] = snorb[wob], snorb[sploop]
            sploop = (sploop + 1) % 256
    zing['drizzle'] = snorb
    return zing

def reverse_scrungle_crank(block, sprockets):
    wiggle = sprockets['flibber']
    waggly = sorted([(wiggle[i], i) for i in range(WUMBLE_BAG)])
    zort = [oof for _, oof in waggly]
    # Undo the final permutation
    permuted = [0] * WUMBLE_BAG
    for i, x in enumerate(zort):
        permuted[x] = block[i]

    # Undo XOR with twizzle
    quix = sprockets['twizzle']
    unxored = bytes([permuted[i] ^ quix[i % len(quix)] for i in range(WUMBLE_BAG)])

    # Reverse the drizzle substitution
    reverse_drizzle = [0] * 256
    for i, val in enumerate(sprockets['drizzle']):
        reverse_drizzle[val] = i
    original = bytes([reverse_drizzle[b] for b in unxored])
    return original

def unsnizzle_bytegum(ciphertext, jellybean):
    plain = b""
    for b in range(0, len(ciphertext), WUMBLE_BAG):
        block = ciphertext[b:b+WUMBLE_BAG]
        plain += reverse_scrungle_crank(block, jellybean)
    # Remove PKCS#7-style padding
    pad_len = plain[-1]
    return plain[:-pad_len]

def main():
    encrypted_hex = "b80854d7b5920901192ea91ccd9f588686d69684ec70583abe46f6747e940c027bdeaa848ecb316e11d9a99c7e87b09e"
    encrypted_bytes = bytes.fromhex(encrypted_hex)
    jellybean = glorbulate_sprockets_for_bamboozle(SNEEZE_FORK)
    decrypted = unsnizzle_bytegum(encrypted_bytes, jellybean)
    print("Decrypted message:")
    print(decrypted.decode(errors="replace"))

if __name__ == "__main__":
    main()