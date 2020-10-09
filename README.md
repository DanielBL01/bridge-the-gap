# Project

An asynchronous web chat that translates messsages to a preferred language.

## Inspiration

From my own personal experience talking to friends and being someone who was born elsewhere but came to North America
at a very young age, I can say that most second generation student always had a difficult time writing in their parents native
language rather than speaking it. This makes sense since, as family we tend to talk to one another a lot more text. 

Personally, I've always had difficulty texting my parents and because of this, our conversations are sometimes short and awkward since
they would text in Korean while I texted back in English and both sides would have a bit of trouble.

The purpose of this app is to create a web chat room where two users can indicate which language they prefer to read and any text 
written to them in any language would be translated using Google's ML algorithm in their preferred language.

## Learning how to secure passwords

We want to encrypt a users password such that if a person breaks into the web app's database,
the users password is not compromised since users tend to use the same passwords for various
websites.

So can be just use a hash function on the password and store it into the database? It's not this simple...
This still leaves us with many vulnerabilities. 

1. An attacker could simply brute force a solution by trying every single combination of characters. A
script can be wrote which reads from a map of every combination possible until the correct password if found.

2. An attacker could also break into the database and use rainbow tables to bypass the encryption. Suppose
that we have a password hash function H and a finite set of passwords P. Given any output h of the hash function, 
a rainbow table can either locate an element p in P such that H(p) = h or determine that there is no such p in P.

So what is the answer?

- One way to add a layer of protection against attacks is to introduce a random string while 
hashing. This random string is called the Salt. This essentially means that even if two users have identical
passwords, they will have different encrypted passwords in the database. This will cause the rainbow table
to grow exponentially since now all possible random strings must be considered. However, this does not 
help us with the first approach of brute forcing a solution.

- The way to fight against a brute force attack, we can also define how many times the hashing function will run.
Adding more iterations will make the hashing function slower and this will make the brute force attack difficult
to pull off since it will take longer time to test out each possible key. 




