# Beowulf SSH cluster

## Introduction 

This program is a example of a [Beowulf cluster](http://en.wikipedia.org/wiki/Beowulf_cluster) or so-called [Stone SouperComputer](http://www.extremelinux.info/stonesoup/) with Python and SSH. In this example, the server connects to any number of client computers via SSH and asks them to help compute some problem. Once a client finishes, the client sends back to the result to the server which stores the result on its own disk. The server then sends that client a new set of computations to finish, and this repeats until all the computations are finished. The client never has to store any information. The server is able to keep track of the client threads, the overall productivity and productivity of each client, and the entirety of the finished results.

## Uses 

- Computation. This is not the optimal use of a Beowulf cluster since this is supposed to be a cluster of antiquated computers. The example I've included here is a computational-use though, the computation of the first ten million primes.

- Web scraping. A Beowulf cluster is especially suited for scraping, since the bottleneck is mainly the connection time to the website. Thus, the web scraping with a Beowulf cluster will roughly scale with the number of computers (or cores per computers). If you do use this for a web scraper you might like to use Tor so you don't get blocked - I've included a code block that utilizes Tor. Note, if you do use this as a web scraper, be sure to read the Terms of Service and make sure to follow ```robots.txt``` as some sites do not allow web scraping (and be kind not to overload any servers with thousands of connections per second).

# How it works

## Server

The server computer needs to have SSH access to each of the computers in the cluster using a SSH key (to alleviate having to store passwords in the program). You can setup SSH pretty easily by installing ```openssh-client``` on each of the cluster computers. The cluster computers can be LAN or Public, as long as you have access to them via SSH and they can run Linux. Also make sure to install whatever Python libraries you'll need on the corresponding computers, as this program doesn't do that yet.

To generate a SSH key on the server computer, simply use

> ssh-keygen

And just press enter/enter/enter.

Then copy the ssh key to all your connected computers using

> ssh-copy-id user@address

And type in your password. That should be the only time you need to type in your password. Then, if the clients have the right python libraries, you can run the server program ```python server_primes.py```, to automatically make the directories and transfer the client program and run the client program.

The server sends a SSH command to run a command on the client computer. Do not send anything private to the client, because it is run as a command and might be saved in the client history. The client then runs the program and sends back the output as a JSON which I believe is secured through SSH. 

### Tor

I included the ability to add in Tor connections. The client script uses the first argument as a Tor flag. To use Tor you need to install tor ```apt-get install tor``` as well as PySocks ```pip install PySocks``` on the client computers.

Since Tor needs to run as a super user, you can create store your password on your client. Since its never a good idea to store the plaintext password, I suggest using base64. I.e. Type your password into ```~/pass``` and then

> base64 ~/pass > ~/pass2

> mv ~/pass2 ~/pass

The program is then set to use this password for running the Tor connections.

## To-do

- Secure server-client transmission by sending the client computer a BASH file via SSH instead of sending it through the command line.
