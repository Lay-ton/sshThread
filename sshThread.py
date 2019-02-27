import threading
import subprocess
import paramiko
import getpass
import time

#I GOT RACE CONDITIONS

#Gets rid of some annoying output to the terminal from Cryptography being
#deprecated
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

print threading.current_thread()

username = raw_input("Username: ")
password = getpass.getpass();
machines = ['hydra', 'risk', 'indus', 'crux']
server = ".cs.utexas.edu"

# The flag for making sure every thread is done
lock_list = {}
for num in xrange(0,len(machines)) :
	lock_list["flag{0}".format(num)] = threading.Event()

# Paramiko connections
ssh_list = {}
for num in xrange(0,len(machines)) :
	ssh_list["ssh{0}".format(num)] = paramiko.SSHClient()
	ssh_list["ssh{0}".format(num)].set_missing_host_key_policy(paramiko.AutoAddPolicy())

std_list = {}
for num in xrange(0,len(machines)) :
	std_list["ssh_stdin{0}".format(num)] = None
	std_list["ssh_stdout{0}".format(num)] = None
	std_list["ssh_stderr{0}".format(num)] = None


def sshThread(machine, client, flag, num) :
	client.connect((machine+server), username=username, password=password)
	std_list["ssh_stdin{0}".format(num)], std_list["ssh_stdout{0}".format(num)], std_list["ssh_stderr{0}".format(num)] = client.exec_command('cd ~/Desktop/CS439/TestOutput/'+machine+'; ./testScript '+str(num)+' 200 1 t3')
	print std_list["ssh_stdout{0}".format(num)].channel.recv_exit_status()
	# ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command('exit')
	flag.set()

num = 0
for item in machines :
	directory = '/u/lseal/Desktop/CS439/TestOutput/' + item
	subprocess.call(['mkdir', '-p', directory])
	time.sleep(1)
	subprocess.call('cp -r /u/lseal/Desktop/CS439/cs439_sp19_lseal_p5/. '+directory, shell=True)
	subprocess.call('rm -rf /u/lseal/Desktop/CS439/TestOutput/Output'+str(num)+'.txt', shell=True)
	num += 1

thread_list = {}

#NEED TO PUT THIS IN FOR LOOPw
num = 0
for item in machines :
	thread_list["thread{0}".format(num)] = threading.Thread(target=sshThread, args=(item, ssh_list["ssh{0}".format(num)], lock_list["flag{0}".format(num)], num,))
	num += 1

for num in xrange(0,len(machines)) :
	thread_list["thread{0}".format(num)].start()

while not lock_list["flag0"].isSet() and not lock_list["flag1"].isSet() and not lock_list["flag2"].isSet() and not lock_list["flag3"].isSet() :
	pass

for item in machines :
	directory = '/u/lseal/Desktop/CS439/TestOutput/' + item
	subprocess.call(['rm', '-rf', directory])


#NEED TO PUT THIS IN FOR LOOP
for num in xrange(0,len(machines)) :
	ssh_list["ssh{0}".format(num)].close()