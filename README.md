# Beowulf SSH cluster

> *"He has thirty men’s heft of grasp in the gripe of his hand, the bold-in-battle. Blessed God out of his mercy this man hath sent to Danes of the West, as I ween indeed, against horror of Grendel"* - Beowulf

![My Beowulf Cluster](https://rpiai.files.wordpress.com/2015/04/0412151720.jpg "My Beowulf Cluster")

## Introduction 

This program is a example of a [Beowulf cluster](http://en.wikipedia.org/wiki/Beowulf_cluster) or so-called [Stone SouperComputer](http://www.extremelinux.info/stonesoup/) with Python and SSH. In this example, the server connects to any number of client computers via SSH and asks them to help compute some problem. Once a client finishes, the client sends back to the result to the server which stores the result on its own disk. The server then sends that client a new set of computations to finish, and this repeats until all the computations are finished. The client never has to store any information. The server is able to keep track of the client threads, the overall productivity and productivity of each client, and the entirety of the finished results.

## Uses 

### Computation. 

Originally, a Beowulf cluster was used for computation. There are many *better* ways of getting speed out of multiple computers (like the clusters that carry out [the great prime search](http://www.mersenne.org/), or [solve the protein folding problem](https://folding.stanford.edu/)), so this is not the optimal use of a Beowulf cluster. This is a cluster of antiquated computers, afterall, so most of them will be slow. 

However, the example I've included here is a computational-use - the computation of the first ten million primes. As an example of the disparity between computers when using a Beowulf cluster of old and new, here is a plot of the rate of prime searching for the computers in my cluster:

![Disparity between speeds of computation](https://rpiai.files.wordpress.com/2015/04/primes_per_second.png "Disparity between speeds of computation")

As you can see, you'd need about five 10-year-old computers to equivalate a single modern desktop. Its probably just better to buy a desktop if this is what you want. 

### Web scraping. 

A Beowulf cluster is especially suited for scraping, since the bottleneck is mainly the connection time to the website. Thus, the web scraping with a Beowulf cluster will roughly scale with the number of computers (or cores per computers). If you do use this for a web scraper you might like to use [Tor](https://www.torproject.org/) so you don't get blocked - I've included a code block that utilizes Tor. Here is a plot of my results from the same computers I used above for scraping a website with and without Tor:

![Sites per minute per computer](https://rpiai.files.wordpress.com/2015/04/sites_per_minute.png "Sites per minute per computer")

For this purpose, the slowest, older computers are only about two times slower than he fastest, newest computers. And by combining their power, you can basically recover the entirity of their might as shown by the actual sites per minute gathered by the cluster versus the sum of individual components:

![Sites per minute per computer sum vs actual](https://rpiai.files.wordpress.com/2015/04/sum_total_vs_actual_total.png "Sites per minute per computer sum vs actual")

Of course, you'll also see that Tor will slow you down quite a bit if you choose to use that extra security boost.

**Note, if you do use this as a web scraper, be sure to read the Terms of Service and make sure to follow ```robots.txt``` as some sites do not allow web scraping (and be kind not to overload any servers with thousands of connections per second).**

# How it works

## Server

The server computer needs to have SSH access to each of the computers in the cluster using a SSH key (to alleviate having to store passwords in the program). You can setup SSH pretty easily by installing ```openssh-client``` on each of the cluster computers. The cluster computers can be LAN or Public, as long as you have access to them via SSH and they can run Linux. Also make sure to install whatever Python libraries you'll need on the corresponding computers, as this program doesn't do that yet.

To generate a SSH key on the server computer, simply use

```bash
ssh-keygen
```

And just press enter/enter/enter.

Then copy the ssh key to all your connected computers using

```bash
ssh-copy-id user@address
```

And type in your password. That should be the only time you need to type in your password. Then, if the clients have the right python libraries, you can run the server program ```python server_primes.py```, to automatically make the directories and transfer the client program and run the client program.

The server sends a SSH command to run a command on the client computer. Do not send anything private to the client, because it is run as a command and might be saved in the client history. The client then runs the program and sends back the output as a JSON which I believe is secured through SSH. 

### Tor

I included the ability to add in Tor connections. The client script uses the first argument as a Tor flag. To use Tor you need to install tor ```apt-get install tor``` as well as [PySocks](https://github.com/Anorov/PySocks) ```pip install PySocks``` on the client computers.

Since Tor needs to run as a super user, you can create store your password on your client. Since its never a good idea to store the plaintext password, I suggest using base64. I.e. Type your password into ```~/pass``` and then

```bash
base64 ~/pass > ~/pass2
mv ~/pass2 ~/pass
```

The program is then set to use this password for running the Tor connections.

## To-do

- Secure server-client transmission by sending the client computer a BASH file via SSH instead of sending it through the command line.
