import os
import threading
import subprocess
import paramiko
import getpass

# Gets rid of some annoying output to the terminal from Cryptography being deprecated
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# The path to the directory this file is in
script_path = os.path.dirname(os.path.realpath(__file__))

# Get user login info and the amount of tests to run
username = raw_input("Username: ")
password = getpass.getpass();

# Takes the testScript arguments a splits them as needed
test_info = raw_input("#Runs #Tests Names..: ").split()
test_info[0] = str(int(test_info[0])/4)
tests_to_run = ""
for item in test_info[2:] :
	if item == test_info[-1] :
		tests_to_run += item
	else :
		tests_to_run += (item + " ")


# FUNCTIONS
#########################################################################
def sshThread(machine, client, flag, num, run) :
	client.connect((machine + ".cs.utexas.edu"), username=username, password=password)
	std_list["ssh_stdin{0}".format(num)], std_list["ssh_stdout{0}".format(num)], std_list["ssh_stderr{0}".format(num)] = client.exec_command('cd ' + script_path + ' ; cd ../TestOutput/' + machine + ' ; ./testScript '+str(num)+' '+test_info[0]+' '+test_info[1]+' '+tests_to_run)
	std_list["ssh_stdout{0}".format(num)].channel.recv_exit_status()
	std_list["ssh_stdin{0}".format(num)], std_list["ssh_stdout{0}".format(num)], std_list["ssh_stderr{0}".format(num)] = client.exec_command('exit')
	flag.set()

def check_list(dic):
	for y in dic.values():
		if y.isSet() == False:
			return False
	return True
#########################################################################

machines = ['hydra', 'risk', 'indus', 'orion']

# Sets up all the dynamic variables
lock_list = {}
ssh_list = {}
std_list = {}
thread_list = {}
for num in xrange(0,len(machines)) :
	# The flag for making sure every thread is done
	lock_list["flag{0}".format(num)] = threading.Event()

	# Paramiko connections
	ssh_list["ssh{0}".format(num)] = paramiko.SSHClient()
	ssh_list["ssh{0}".format(num)].set_missing_host_key_policy(paramiko.AutoAddPolicy())

	# The ssh input, output, and error for each thread
	std_list["ssh_stdin{0}".format(num)] = None
	std_list["ssh_stdout{0}".format(num)] = None
	std_list["ssh_stderr{0}".format(num)] = None

# Builds the directories for the threads to run in and creates the threads
for num in xrange(0,len(machines)) :
	subprocess.call('cd ' + script_path + ' ; cd ../ ; mkdir -p TestOutput/' + machines[num], shell=True)
	subprocess.call('cp -r ' + script_path + '/. ../TestOutput/' + machines[num], shell=True)
	subprocess.call('cd ' + script_path + ' ; rm -rf ../TestOutput/Output'+str(num)+'.txt', shell=True)
	thread_list["thread{0}".format(num)] = threading.Thread(target=sshThread, args=(machines[num], ssh_list["ssh{0}".format(num)], lock_list["flag{0}".format(num)], num, test_info[0],))

# Starts the threads
for num in xrange(0,len(machines)) :
	thread_list["thread{0}".format(num)].start()

# While all the threads aren't complete block main from cont
while not check_list(lock_list) :
	pass

# Deletes the directories and closes the ssh connections
for num in xrange(0,len(machines)) :
	subprocess.call('cd ' + script_path + ' ; rm -rf ../TestOutput/' + machines[num], shell=True)
	ssh_list["ssh{0}".format(num)].close()
