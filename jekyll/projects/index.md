---
layout: page
title: Projects
---

Various projects I've created over the years that I am happy with.

[gbjit](https://github.com/iburinoc/gbjit)
---
A WIP GameBoy/GameBoy Colour emulator in Rust, but using just-in-time compilation
to rewrite the Z80 opcodes as x86_64 assembly, allowing the GameBoy CPU to run as
native code instead of being interpreted.

[gba-rs](https://github.com/iburinoc/gba-rs)
---
A GameBoy Advance emulator written in Rust.
The CPU implementation was pulled out by [Daniel Prilik](https://prilik.com)
into its own rust crate [armv4t_emu](https://github.com/daniel5151/armv4t_emu/),
usable as a generic implementation of the ARMv4T ISA.
It was later used in a [simulator we wrote for the TS7200](https://github.com/daniel5151/ts7200/),
used in the CS452 course at the University of Waterloo,
allowing us to write and debug our kernels from home.

[gr_trace](https://github.com/iburinoc/gr_trace)
---
A realtime ray-tracer that implements gravitational lensing around a
Schwarzschild black hole.  It's written in Rust, using the Glium library
for window creation and GL context management, and with the ray tracing written
in the fragment shader using Runge-Kutta 4 for stable integration.

[flightsim](https://github.com/iburinoc/flightsim)
---
A flight simulator written in C++ using OpenGL for rendering a 3D environment.
It generates infinite terrain using simplex noise generation,
with a pastel-like shading style that makes the terrain nice to look at.
I also [ported it to iOS](https://github.com/iburinoc/flightsim-cardboard)
using Google Cardboard to fly around in VR!

[3ds-gamepad](https://github.com/iburinoc/3ds-gamepad)
---
A 3ds Homebrew program and companion apps for Linux and Windows that allow the 3ds
to be used as a gamepad over wifi, usable with desktop games.

[ibcrypt](https://github.com/iburinoc/ibcrypt)
---
A cryptographic primitive library written in C.
It was written to try my hand at writing cryptographic primitives as well as
learn C.
Implements various block ciphers, hash functions, key derivation functions,
etc.,
as well as features an efficient arbitrary precision arithmetic implementation.

[resistora](https://github.com/iburinoc/resistora)
---
An Android app that allows you to determine the resistance of resistors by
aiming your camera at it.  It uses custom computer vision algorithms to locate
the bands on resistors and then determine their colours.  Created for the Tech
Retreat 2015 hackathon, where it won 2nd place.

[AnonymEyes](http://anonymeyes.co)
---
A combination of an Android app and web app that allows you to record videos
from your phone straight to our webserver.  It allows anyone to easily and
anonymously record incidents to enable emergency responders and promote
accountability.  Its built on a combination of a java backend talking to the
Android app, and a Rails webserver to run the webpage.  It was created for
Hack the North 2015, where it was one of the 12 winning teams.

My primary contribution was the communication between the phones and the
backend, serializing the frames into an efficient format that could be sent
over UDP and parsed on the other end for display.

[This site](https://github.com/iburinoc/ibsite)
---
A static site made using the Jekyll site generator served by NGINX,
with a dynamic background of snippets of code I wrote from various projects.
It works with a NGINX configuration indicating that the background
image file not be cached by the client, and to reverse proxy requests for the
background image to a [Flask](http://flask.pocoo.org/)
server that returns a random image, selected
from a number of images pregenerated with a custom tool working with
[Pygments](http://pygments.org/).

[ibchat](https://github.com/iburinoc/ibchat)
---
An end-to-end encrypted chat program written in C from scratch using my ibcrypt
library to provide cryptographic primitives.  It uses a variety of algorithms
such as RSA, Diffie-Hellman, scrypt, SHA2, CHACHA, and HMAC to provide key
negotation, secure communication, and untamperable file storage.
Additionally, it features several custom-written network protocols
and message formats to ensure secure communications without requiring
trusting the central server, allowing for the advantages of a decentralized
system without the inherent security risk.

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

[3D Pacman](https://github.com/iburinoc/3D-Pacman)
---
A 3D recreation of the classic arcade game "Pacman" written in Java.
The rendering engine is a ray-caster written from scratch entirely in software.
The ghost AI, level design, point counts, etc. are all faithfully recreated from
the original game, the caveat being you can only see forward.

