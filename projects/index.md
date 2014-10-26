---
layout: page
title: Projects
---

Various programming projects I've created over the years that I am happy with.

[3D Pacman](https://github.com/iburinoc/3D-Pacman)
---
A 3D recreation of the classic arcade game "Pacman" written in Java.
The rendering engine is a ray-caster written from scratch entirely in software.
The ghost AI, level design, point counts, etc. are all faithfully recreated from
the original game, the caveat being you can only see forward.

Written with Andrey Khesin and Dima Paramonov as the summative assignment for
Grade 12 Computer Science.

[spass](https://github.com/iburinoc/spass)
---
A command-line based password manager written in C for Unix-based systems
(i.e. OS X, Linux).
Generates and stores passwords in a database file encrypted using
[chacha](http://cr.yp.to/chacha/chacha-20080128.pdf).
The encryption and authentication keys are derived using
[scrypt](http://www.tarsnap.com/scrypt.html)
and database file authenticated using HMAC-SHA256.
It uses the ibcrypt library for implementations of cryptographic primitives.

[ibcrypt](https://github.com/iburinoc/ibcrypt)
---
A work-in-progress cryptographic primitive library written in C.
It was written to try my hand at writing cryptographic primitives as well as
learn C.
Not the best of combinations, but oh well.
Implements various block ciphers, hash functions, key derivation functions,
etc., as well as features a half-working bignum implementation.

[Cube](https://github.com/iburinoc/Cube)
---
The code behind my Grade 12 Robotics project: A rubix's cube solver.
Contains algorithms to solve the rubix's cube, code to interface
with the robot (Arduino), and the actual micro-controller code for
operating the robot's motors (using the Adafruit Motor Shield).

Written with Andrey Khesin and Dima Paramonov

[Risk](https://github.com/iburinoc/risk)
---
The board game Risk implemented in Java.  Contains the ability to play
with up to 6 players/AI, locally as well as over a network.
Network communications are over pure sockets,
and data is serialized using [protobufs](https://github.com/google/protobuf/).

Written as an assignment for Grade 12 Computer Science.

[mafia](https://github.com/iburinoc/Mafia)
---
A node.js and AngularJS implementation of the classic party game Mafia.
Warning: The code is horrendously messy, you have been warned.
