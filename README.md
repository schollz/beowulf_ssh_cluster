# Beowulf SSH cluster

This program is meant to provide a simple solution to making a [Beowulf cluster](http://en.wikipedia.org/wiki/Beowulf_cluster) or so-called [Stone SouperComputer](http://www.extremelinux.info/stonesoup/) with Python and SSH. The program included here is a skeleton of a real program and an example of what it can be used for. This example parses prime numbers, which is not the optimal application of this cluster since this is meant to be run on computers relics. 

The optimal use of this proram is probably a web scrapper or web spider because bottleneck for grabbing websites is usually connection time to the website and downloading the site. Thus this can scale pretty well with number of computers, regardless of processing speed. Thats why this example includes a code block for including Tor. If you do use this for a web scraper you might like to use Tor so you don't get blocked. Also, if you do use this as a web scraper, be sure to read the Terms of Service and make sure to follow ```robots.txt``` as some sites do not allow web scraping (and be kind not to overload any servers wiht thousands of connections per second).

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

I included the ability to add in Tor connections. The client script uses the first argument as a Tor flag. To use Tor you need to install tor ```apt-get install tor``` as well as PySocks ```pip install PySocks```.

## To-do

- Secure server-client transmission by sending the client computer a BASH file via SSH instead of sending it through the command line.
