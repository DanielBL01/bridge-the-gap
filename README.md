# About the Project - Bridge the Gap

A web chat that utilizes web sockets to allows for live chat between users. Users are
allowed to create their own chat rooms where two users can asynchronously text one another. When texting,
the Google Translation API is used to translate one users text to the other users preferred language which are all stored in a PostgreSQL database along with their username and encrypted password.

## Inspiration

As a student who was born outside of North America but came to live and study in Canada at a very young age, I have always struggled texting with my parents in their native language. 

Because of this, our conversations are sometimes cut short since I would be texting in English while my parents would text in their native language. Both sides would have a bit of trouble. 

Obviously, the problem at hand is not a hard one. I could have simply pasted my text message into a translator and paste it back to send. But since it's 2020 and no one has the patience to consistently do this, I thought I would make an app for it.

Another reason was to dive deeper into more complex web development, namely using SocketIO for realtime, bi-directional communication between the client and server.  

## Secure passwords

We want to encrypt a users password such that if a person breaks into the web app's database,
the users password is not compromised.

So can we just use a hash function on the password and store it into the database? Unfortunately, it's not this simple... Let's see why this still leaves us with a few vulnerabilities. 

1. An attacker could simply brute force a way in by trying every single combination of characters. A
simple script can be wrote to do this.

2. An attacker could also break into the database and use rainbow tables to bypass the encryption. To understand rainbow tables, suppose that we have a password hash function H and a finite set of passwords P. Given any output h of the hash function, a rainbow table can either locate an element p in P such that H(p) = h or determine that there is no such p in P.

So what is the answer? 🤔

- One way to add a layer of protection against attacks is to introduce a random string while 
hashing. This random string is called salt. This essentially means that even if two users have identical
passwords, they will have different encrypted passwords in the database. This will cause the rainbow table to grow exponentially since now all possible random strings must be considered. Sadly, this does not help us with the first approach where the attack is a brute force method.

- To fight against the brute force method, we can also define how many times the hashing function will run. Adding more iterations will make the hashing function slower and this will make the brute force attack difficult to pull off since it will take a much longer time to test out each possible key. 