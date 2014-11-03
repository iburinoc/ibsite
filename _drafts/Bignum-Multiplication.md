---
layout: post
title: Bignum Multiplication
---

## Background
I'm currently working on a cryptographic primitive library I've named
[ibcrypt]({{ site.pages_list.Projects }}#ibcrypthttpsgithubcomiburinocibcrypt).
The idea is to implement all the algorithms completely from scratch, i.e.
no libraries other than the C standard library (and possibly some POSIX).
It has no claims of being cryptographically secure, as while I'd like to
implement the algorithms correctly and securely,
I'm very very doubtful I've managed to avoid all of the many pitfalls
that exist for an implementor of cryptographic primitives (especially when it
comes to algorithms such as AES, RSA, etc.).

Therefore all I'm going for with this project is to experience implementing
cryptopgrahic primitives, hopefully culminating in some sort of command-line
messaging program based on it, for fun.

In order to do this, public key cryptography will definitely be required.
The problem with public key cryptography is that it tends to be based on
arithmetic operations performed on large (1024-2048 bits) numbers.
C, the language I'm writing this library in, does not natively support such
large numbers.
As a result, this means before I can get to public key crypto, I have to write
an arbitrary precision integer library.
Fun.

## Multiplication and Exponentiation
Since multiplication and exponentiation are key parts to many cryptographic
algorithms and protocols, my library obviously has to have it.
It also has to be efficient, as no one wants to wait ages to encrypt
each message/key/whatever else will be sent.
I ended up going through a number of iterations before I reached what I
currently have.
It could probably be made more efficient with a fair bit of effort,
but I think it's good enough to allow me to go focus on other things.

### Exponentiation
For exponentiation I decided to use the Montgomery Powering Ladder as described
[here](http://cr.yp.to/bib/2003/joye-ladder.pdf).
It is a relatively simple algorithm that doesn't have any conditionals
based on secret information, making it ideal for public key crypto.

### Multiplication: A First Attempt
Multiplication required a bit more thought.
The first algorithm I thought of was effectively binary long multiplication.

To illustrate in python-like pseudocode:

{% highlight python %}
def multiply(a, b):
        r = 0
        # iterate over each bit of b
        for i in range(log2(b)):
                # i'th bit of b
                if b[i] == 1:
                        r += a << i
        return r
{% endhighlight %}

There's a slight twist however.
We don't only want multiplication, we want multiplication mod some number n,
i.e. calculate r = (a * b) % n.

Therefore we make the following modification to our multiplication algorithm:

{% highlight python %}
def multiply_mod(a, b, n):
        r = 0
        # iterate over each bit of b
        for i in range(0, log2(b)):
                # i'th bit of b
                if b[i] == 1:
                        # reduce the addition modulo n
                        r = (r + a << i) % n
        return r
{% endhighlight %}

This routine looks alright at first glance, although you might notice we haven't
actually defined how we plan on doing addition or modular reductions.
Addition is a simple O(n) operation, so it won't be covered here, but modular
reductions are non-trivial.
In my library basic modular reductions are implemented basically as division,
shown here in pseudocode:
{% highlight python %}
def divide_mod(a, b):
        q = 0
        shift = 0
        while b < a:
                b <<= 1
                shift += 1
        # iterate over the shift bits
        for i in range(shift - 1, -1, -1):
                b >>= 1
                if b < a:
                        a = a - b
                        q |= (1 << i)
        # quotient, remainder
        return (q, a)
{% endhighlight %}

In a general context, it's hard to make modular reductions more efficient than
this.

Now that we have our multiplication defined, let's try out exponentiation.

We're trying to calculate the following:

{% highlight python %}
m^e % n

# values:
m = 0xced9c95986f5bf1805110bb5fb436fb5bd300ede4e5ad19d53c30f473b323f1f12b55ded63cdc6840612196870bdffffeee41157c1eed71dd3e4c60239f2a4401c87e33a328bf09b685f81fb50c7b5c81995c6af280ceceb8422e92bae75d19a5dff48e5c836d14045ea568074d49ca9647d665b37dc15b29604ae85ffa847d4d6315efb3adf6d3e3700f14d08f68ff448d78f650a95c123daa4f308f79fe23333c818fa85d457b32a75b51f9a1f69a386da6a35cbf75ad893a3bfa59633e48cf985b525ef63d7698a4faa75cf07c9303491ab61fc36549fc2c7eae38e2764aa9a0034a9f2f0c19ffe2589d26070ffa923302dedfe240c8e082403d3bad8fead
e = 0xa7c44d53a6175eab18c61802aad4dc00c498f0f184359d58e3616b9463b99b67cb93f525101c9db09f9e6e06d701fc1179f9343a3b2a5dc680d83476443c07041f9779d3801598f3df6c8a2cdd441a27c557f685ef8dd47615443a8831a83b7b00e561eef855820d3368aaacf1effc261803525de357f86cbaa18a706b67c134077b6476afd297340916d28b20c6de071f40bf8129aaf7c6cb3db05e228e0afb2c95f6c117a505f038cebc955d438dad11dee77ab3ea19dcf8a372e6dda7bd77458fc57b141ce6eaaf56e882bc1a87be677d02e087f3e60832f9b2c660cb82f3badccd36f1c1616b468928f45e25d6edb2c4fbcf0c0bf75ba9ea75930599f451
n = 0xb05bde88ecc32ffa109dd630ad46dc12d889ecdc536a82e9784b570fd7932a8b9081b1a15922d09921a29fd7c95ab1bf851476c3b0a35497c525b4e984af3e814e05325d1be5ddfab399c0b0fc5c48cfb3d8d4dca8b7fdbd3bc9c12adc67f89f361e2afe63867eb763114d988579e0cb02af6ca6772e3ab6679d83aee70b0007df5818a825c346a9167f3629ad1a408ae4520f346ef594c3f1b3318f746025f200ae53ec152adfbdedee89bbf5e877a4f174b95a6ce5438c6ed26cdf098a448a9cfaafa13b18450ddf44abda147efa0d44ff934bb6565076e4b31fc401171e01f2fab7b9a65fa1941edbacc5c6b831329bbac9b5dc79053029454971891938f5
{% endhighlight %}

Python's internal arbitrary precision library can calculate this in 0.04s.
How do we compare to this?

{% highlight bash %}
spmbp:bn Sean$ time ./a.out
real    0m19.673s
user    0m17.292s
sys     0m1.222s
{% endhighlight %}

...ouch.  At least we got the right answer of- y'know it's a bit of a big
irrelevant number, you calculate it yourself if you want to know.

## Second Approach
Before we can make it faster, we need to figure out what we should actually fix.
Using Apple's Instruments app, we can see how much time is spent in each method:
![Screenshot of Instruments after running the program]({{ site.baseurl }}assets/bno_mul_a1_instruments.png)

Wow.
94.8% of the program is spent in rmod_words (the modular reduction routine).
This can definitely be improved.
Looking at the previous algorithm, you can see that we reduce the product mod n
every time we add, which is expensive.
If we only do it once at the end, that one modular reduction will be more
expensive, but overall it should be cheaper.

{% highlight python %}
def multiply_mod(a, b, n):
        r = 0
        # iterate over each bit of b
        for i in range(0, log2(b)):
                # i'th bit of b
                if b[i] == 1:
                        r = (r + a << i)
        # reduce the product modulo n
        return r % n
{% endhighlight %}

So how well does this work?

{% highlight bash %}
spmbp:bn Sean$ time ./a.out
real    0m2.940s
user    0m2.866s
sys     0m0.015s
{% endhighlight %}

Not bad, not bad at all.

## Further Speedups
It'd be nice if we could do even better than that though.
Looking at Instruments, most of the time is still spent doing modular
reductions.
To speed this up, I decided to use
[Barrett reductions](http://en.wikipedia.org/wiki/Barrett_reduction).
This allows me to do a single division operation for a given modulus, and then
trade all subsequent modular reductions for two multiplications and a
subtraction.

After implementing this, let's see how well it works.

{% highlight bash %}
spmbp:bn Sean$ time ./a.out
real    0m4.384s
user    0m4.253s
sys     0m0.022s
{% endhighlight %}

Hmm... it's actually slower!
The reason for this is that my multiplication routine is not faster than
modular reductions by a significant enough amount to be worth doing two of them
instead of one modular reduction.

Let's fix that.
The way I was doing multiplication involved calculating the bitshifted values
for a over and over again, which involved allocating the memory for it and
iterating over all of a bitshifting.
Instead, let's do long multiplication in base 2^64:

{% highlight python %}
define mul(a, b):
        r = 0
        # iterate over each 64 bit word in a
        for i in range(0, len(a)):
                carry = 0
                # iterate over each 64 bit word in b
                for j in range(0, len(b)):
                        # multiply the relevant words of a and b and
                        # add them to the previous value for that word
                        # in r[i + j] and the carry
                        product = a[i] * b[j] + r[i + j] + carry
                        # set the new value for this word to the lower
                        # 64 bits of product
                        r[i+j] = product & 0xffffffff
                        # set the carry to the upper 64 bits
                        carry = product >> 64
                r[i + len(b)] = carry
        return r
{% endhighlight %}

Alright, now that our multiplication algorithm iterates over words instead of
bits and isn't moving all sorts of state around, how's performance?

{% highlight bash %}
spmbp:bn Sean$ time ./a.out
real    0m0.099s
user    0m0.093s
sys     0m0.003s
{% endhighlight %}

Pretty good.

### Code
The code described in this post can be found at
[https://github.com/iburinoc/ibcrypt/tree/master/bn](https://github.com/iburinoc/ibcrypt/tree/master/bn).
