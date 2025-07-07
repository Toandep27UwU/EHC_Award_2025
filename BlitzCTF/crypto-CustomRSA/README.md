# CustomRSA

## Description

<figure><img src=".gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

[Custom\_RSA.py](Custom_RSA.py)

[out\_4.txt](out.txt)

## Solution

1. **Analyzed**

* First, I see 2 equations

$$
\begin{cases}
e = x\ .\ y\ .\ z \\
n = p\ .\ q\ .\ y
\end{cases}
$$

* Because `x, y, z, p, q, y` are prime numbers, we have `GCD(e,n) = y`
* So we can find

$$
\begin{cases}
e_1 = x\  .\ z \\
n_1 = p\ .\ q\ 
\end{cases}
$$

* Because $$e_1$$ is a 256 bit number, we can factorize it to 2 prime numbers `x` and `z` , I use tool to factorize it and I have results after 3 minutes.

```
x = 205985756524450894105569840071389752521
z = 212007435030018912792096086712981924541
```

* After that, we use Chinese Remainder Theorem to find `p` from 2 equation:

$$
\begin{cases}
p \equiv hint1\ (mod\ x) \\
p \equiv hint2\ (mod\ z)
\end{cases}
$$

* After having `p`, we can find `q` and decode RSA easily.

2. **Scripts**

```python
from Crypto.Util.number import *

hint1 =  154888122383146971967744398191123189212
hint2 =  130654136341446094800376989317102537325
n =  1291778230841963634710522186531131140292748304311790700929719174642140386189828346122801056721461179519840234314280632436994655344881023892312594913853574461748121277453328656446109784054563731
e =  9397905637403387422411461938505089525132522490010480161341814566119369497062528168320590767152928258571447916140517
c =  482782367816881259357312883356702175242817718119063880833819462767226937212873552015335218158868462980872863563953024168114906381978834311555560455076311389674805493391941801398577027462103318

y = GCD(n,e)
e1 = e // y 
n1 = n // y 
x = 205985756524450894105569840071389752521
z = 212007435030018912792096086712981924541

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, _ = egcd(a, m)
    return x % m

def crt(r1, m1, r2, m2):
    g, s, t = egcd(m1, m2)
    lcm = m1 // g * m2
    inv = modinv(m1 // g, m2 // g)
    t0 = ((r2 - r1) // g * inv) % (m2 // g)
    p = (r1 + t0 * m1) % lcm
    return p

p = crt(hint1, x, hint2, z)+x*z
q = n1 // p 

phi = (p-1)*(q-1)*(y-1)
d = inverse(e,phi)
plain = pow(c,d,n)
plain = long_to_bytes(plain)
print(plain)
```

```
Blitz{H0w_D4r3_y0u_br34k_My_RSA_Ag41n!!!}
```
