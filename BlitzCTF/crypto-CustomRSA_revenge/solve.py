from math import isqrt
from Crypto.Util.number import long_to_bytes, inverse, isPrime

mod_phi = 381679521901481226602014060495892168161810654344421566396411258375972593287031851626446898065545609421743932153327689119440405912     
n = 1236102848705753437579242450812782858653671889829265508760569425093229541662967763302228061        
c = 337624956533508120294617117960499986227311117648449203609049153277315646351029821010820258         

approx = mod_phi // n            
for off in range(-10000, 10001):
    e = approx + off + 1  
    if not isPrime(e): 
        continue
    A = e - 1
    if mod_phi % A: 
        continue
    k = mod_phi // A
    t = n + 1 - k
    D = t*t - 4*n
    if isqrt(D)**2 == D:
        p = (t + isqrt(D)) // 2
        q = (t - isqrt(D)) // 2
        phi = (p-1)*(q-1)
        d = inverse(e, phi)
        m = long_to_bytes(pow(c, d, n))
        print(m)          
        break
