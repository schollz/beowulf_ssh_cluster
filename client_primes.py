import json
import sys

if int(sys.argv[1])==1:
	import urllib2
	try:
		import socks
	except:
		print "you need to install PySocks for Tor use"
	import socket
	socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
	socket.socket = socks.socksocket
	#my_ip = urllib2.urlopen('http://icanhazip.com').read()
	
def is_prime(n):
	if n <= 3:
		return n >= 2
	if n % 2 == 0 or n % 3 == 0:
		return False
	for i in xrange(5, int(n ** 0.5) + 1, 6):
		if n % i == 0 or n % (i + 2) == 0:
			return False
	return True	

def worker(*nums):
	results = {}
	for n in nums[0]:
		results[int(n)] = is_prime(int(n))
	return results
	
print json.dumps(worker(sys.argv[2:]))
