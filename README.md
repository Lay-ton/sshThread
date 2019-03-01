# sshThread 

A python script to speed and split up the work of running tests in Gheith's CS439 class. The script splits up the desired 
amount of runs inputed by the user amongst four different lab machines via ssh. The results are then stored in a directory 
named TestOutput outside your projects directory.

## To Run:
  
  * Copy the files into your project directory then type "python sshThread.py". It'll prompt you for your UTCS accout login info.
  * After obtaining your login info it'll ask for the number of runs, number of tests, and the names of the tests. Just wait for 
  the script to finish then go to the directory TestOutput which is stored in the same directory that hold your project 
  directory. There will be four Output#.txt files with the results of the tests.
