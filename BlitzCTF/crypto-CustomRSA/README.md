# CustomRSA

## Description







## Solution

1. First, I see 2 equations

$$
e = x\ .\ y\ .\ z \\ n=p\ .\ q\ .\ y
$$

* Because `x, y, z, p, q, y` are prime numbers, we have `GCD(e,n) = y`&#x20;
* So we can find&#x20;

$$
e_1 = x\ .\ z \\ n_1=p\ .\ q
$$

* Because  $$e_1$$  is a 256 bit number, we can factorize it to 2 prime numbers `x` and `z` , I use tool to factorize it and I have results after 3 minutes.

```
// Some code
```

*
