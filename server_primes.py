import shlex
from subprocess import Popen, PIPE
import logging
import threading
import time
import json
import pickle

'''
1. On server computer:
ssh-keygen

2. Then 
ssh-copy-id user@address

3. For each address, add it to the "cluster" variable below
'''

cluster = {}
cluster['this computer']={'address':'bitnami@127.0.0.1','cores':2}

'''
4. If using tor:
In each computer put the sudoers password in a file called "pass" using base64
(I.e. write the password to a file. then base64 file > file2. Then mv file2 file)

'''


# Generic worker thread for sending commands
def worker(cmd,i,):
	global response
	process = Popen(shlex.split(cmd), stdout=PIPE)
	(output,err)=process.communicate()
	exit_code = process.wait()
	response[i] = output

# Worker initiation protocol to send a command but wait until all threads are finished
def runAndWait(remote_cmd,clients):
	threads = []
	for i in range(len(clients)):
		cmd = "ssh "+clients[i]+" '"+remote_cmd+"'"
		print cmd
		t = threading.Thread(target=worker, args=(cmd,i,))
		threads.append(t)
		t.start()
	for i in range(len(clients)):
			threads[i].join()		
	print '[' + cmd + ']: DONE'

# Worker initiation protocol to send a file and wait until all files are sent
def sendFileAndWait(file,folder,clients):
	threads = []
	for i in range(len(clients)):
		cmd = "scp " + file + " " + clients[i] + ":" +folder+"/"
		print cmd
		t = threading.Thread(target=worker, args=(cmd,i,))
		threads.append(t)
		t.start()
	for i in range(len(clients)):
			threads[i].join()		
	print '[' + cmd + ']: DONE'


# Generate list of clients (add extra if there are extra cores available)
clients = []
for computer in cluster:
	for i in range(int(cluster[computer]['cores'])):
		clients.append(cluster[computer]['address'])

# Initialize responses
response = []
for i in range(len(clients)):
	response.append(clients[i])
	
# Initialize logging
logging.basicConfig(level=logging.DEBUG,
	format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
	datefmt='%y-%m-%d %H:%M:%S',
	filename='server.log',
	filemode='a'
)

# First make the distributed folder if it doesn't exist
runAndWait('mkdir beowulf',clients)

# Second, send the file to run
sendFileAndWait('client_primes.py','beowulf',clients)

# Start up tor (if needed)
#runAndWait('base64 -d ~/pass | sudo -S /etc/init.d/tor restart',clients)


# Initialize the threads with a simple task
threads = []
clientDiag = []
for i in range(len(clients)):
	response[i]=""
	remote_cmd = 'ls -l | tail -n 1'
	cmd = "ssh "+clients[i]+" '"+remote_cmd+"'"
	t = threading.Thread(target=worker, args=(cmd,i,))
	threads.append(t)
	t.start()
	clientDiag.append({})
	clientDiag[i]['server'] = clients[i]
	clientDiag[i]['lastSeen'] = time.time()
	clientDiag[i]['totalIterations'] = 0
	clientDiag[i]['timePerIteration'] = 0
	
	
# Start main thread
logger = logging.getLogger('main')
start = 1
finish = 10000000
blocks = 10000 # number of blocks to do each time. Try to block size ~1-5 seconds of computation time to take advantage
master_index = start
startTime = time.time()
while master_index<finish:
	for i in range(len(clients)):
		if not threads[i].isAlive():
			# Get response
			try:
				json_object = json.loads(response[i])
				# Save whatever data you want from the response
				for key in json_object.keys():
					if json_object[key]:
						with open('primes','a') as f:
							f.write(str(key))
							f.write('\n')
			except:
				print "No JSON object detected"

			# Update the client meta-data
			clientDiag[i]['lastSeen'] = time.time()
			clientDiag[i]['totalIterations'] += blocks
			clientDiag[i]['timePerIteration'] = (time.time()-startTime)/clientDiag[i]['totalIterations']
			if clientDiag[i]['totalIterations'] % (blocks*5)==0:
				logger.debug(clientDiag[i])

			# Send the next set
			# Firt argument is Tor flag
			remote_cmd = 'python beowulf/client_primes.py 0 ' + ' '.join(str(x) for x in range(master_index,master_index+blocks))
			cmd = "ssh "+clients[i]+" '"+remote_cmd+"'"
			threads[i] = threading.Thread(target=worker, args=(cmd,i,))
			threads[i].start()
			master_index += blocks
			
			# Log every 20 blocks
			if (master_index-start) % (blocks*20) == 0:
				logger.debug(str((time.time()-startTime)/(master_index-start+0.0)) + ' seconds per iteration (TOTAL)')
				logger.info('Finished up to ' + str(master_index))
				
	time.sleep(.05)

# Secure transfer
# scp ~/run user@127.0.0.1:beowulf/ && ssh user@127.0.0.1 'chmod +x ~/beowulf/run' && ssh bitnami@127.0.0.1 '~/beowulf/run'
