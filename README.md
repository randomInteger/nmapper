nmapper.py:  This tool is a wrapper for nmap that will print nicely to the screen
as well as to a JSON output file.

The primary purpose of this tool is to be able to run nmap scans for machines
that are UP on a network, and then get a JSON list of those IP addresses.

This tool can be used to generate IP lists to feed into tools which batch process operations to large lists of IP addresses.

Date:  2/9/2017

Authors:  randomInteger


Installation:    
Host machine needs a full python/python3 dev environment:    
sudo apt-get install build-essential libssl-dev libffi-dev python-dev python3-dev

Prep to run the tool (do this only once per install):    
virtualenv -p /usr/bin/python3 ./.env    
source .env/bin/activate    
pip install -r ./requirements.txt    


Do this once per shell session (post install):    
source .env/bin/activate    

Run the tool:    

#No host name lookup, check ports 22 and 443 on network 172.16.101.0/24
./nmapper.py -a '-n -p 22,443 172.16.101.0/24'

#No host name lookup, check all ports on network 172.16.101.0/24
./nmapper.py -a '-n 172.16.101.0/24'

File Output:

A time stamped output file is created in the following format:  
%Y-%m-%d_%H-%M-%S.nmapper_out.json

Sample output (view this in a file editor, it looks like garbage in bitbucket...)

(.env)tc@autotron:~/src/nmapper$ ./nmapper.py -a '-n -p 22,443 172.16.101.0/28'

**********NMAPper BEGIN RUN**********
INFO: nmapper is starting...
Executing NMAP via the following command: nmap -oX - -n -p 22,443 127.0.0.1 172.16.101.0/28
****************************************************************
Host : 172.16.101.11 ()
State : up
----------
Protocol : tcp
port : 22	state : {'name': 'ssh', 'state': 'open', 'version': '', 'extrainfo': '', 'product': '', 'cpe': '', 'reason': 'syn-ack', 'conf': '3'}
port : 443	state : {'name': 'https', 'state': 'closed', 'version': '', 'extrainfo': '', 'product': '', 'cpe': '', 'reason': 'conn-refused', 'conf': '3'}
****************************************************************
Host : 172.16.101.12 ()
State : up
----------
Protocol : tcp
port : 22	state : {'name': 'ssh', 'state': 'open', 'version': '', 'extrainfo': '', 'product': '', 'cpe': '', 'reason': 'syn-ack', 'conf': '3'}
port : 443	state : {'name': 'https', 'state': 'closed', 'version': '', 'extrainfo': '', 'product': '', 'cpe': '', 'reason': 'conn-refused', 'conf': '3'}
****************************************************************
Host : 172.16.101.13 ()
State : up
----------
Protocol : tcp
port : 22	state : {'name': 'ssh', 'state': 'open', 'version': '', 'extrainfo': '', 'product': '', 'cpe': '', 'reason': 'syn-ack', 'conf': '3'}
port : 443	state : {'name': 'https', 'state': 'closed', 'version': '', 'extrainfo': '', 'product': '', 'cpe': '', 'reason': 'conn-refused', 'conf': '3'}
****************************************************************
Host : 172.16.101.14 ()
State : up
----------
Protocol : tcp
port : 22	state : {'name': 'ssh', 'state': 'open', 'version': '', 'extrainfo': '', 'product': '', 'cpe': '', 'reason': 'syn-ack', 'conf': '3'}
port : 443	state : {'name': 'https', 'state': 'closed', 'version': '', 'extrainfo': '', 'product': '', 'cpe': '', 'reason': 'conn-refused', 'conf': '3'}
****************************************************************
Host : 172.16.101.15 ()
State : up
----------
Protocol : tcp
port : 22	state : {'name': 'ssh', 'state': 'open', 'version': '', 'extrainfo': '', 'product': '', 'cpe': '', 'reason': 'syn-ack', 'conf': '3'}
port : 443	state : {'name': 'https', 'state': 'closed', 'version': '', 'extrainfo': '', 'product': '', 'cpe': '', 'reason': 'conn-refused', 'conf': '3'}
****************************************************************
UPDATE:  Output file successfully written to: ./2017-02-09_15-35-01.nmapper_out.json

**********NMAPper RUN FINISHED**********

Output file contents from the last example:

(.env)tc@autotron:~/src/nmapper$ cat ./2017-02-09_15-35-01.nmapper_out.json | jq .
[
  "172.16.101.11",
  "172.16.101.12",
  "172.16.101.13",
  "172.16.101.14",
  "172.16.101.15"
]

