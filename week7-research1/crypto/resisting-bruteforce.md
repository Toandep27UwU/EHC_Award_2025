# Resisting Bruteforce

## Description

<figure><img src=".gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>



## Solution

* AES-128 is considered extremely secure; brute-forcing the entire 128-bit keyspace is infeasible (even with the computing power of the entire Bitcoin mining network, it would take hundreds of times longer than the age of the universe).
* There is a theoretical attack slightly better than brute force — the **biclique attack** — which reduces the security from 128 bits to 126.1 bits.
* This attack is impractical and has not been improved in over 8 years.
* Quantum computers could severely break public-key cryptosystems, but for symmetric cryptosystems they are expected to only halve the security level.
* Therefore, AES-256 is recommended to maintain 128-bit security in a quantum future.



## Flag

```
crypto{biclique}
```
