#!/usr/bin/env python3
"""
nmapper.py:  This tool is a wrapper for nmap that will print nicely to the screen
as well as to a JSON output file.

The primary purpose of this tool is to be able to run nmap scans for machines
that are UP on a network, and then get a JSON list of those IP addresses.

This tool can be used to generate IP lists to feed into tools which batch process operations to large lists of IP addresses.

Date: 2/9/2017

Authors: randomInteger
"""
import os
import sys
import json
import nmap  #pip install python-nmap
import datetime
import getopt


def usage():
    """
    Prints usage for nmapper.py
    """
    print('Usage: nmapper.py [-h] -a <nmap_args> -f <outputfile>')
    print('Usage: nmap_args are the normal args you would send to nmap')
    print('Usage: This tool will create a list of every IP that was up on at least one port.')
    print('Usage: This file will be written to ./<timestamp>.nmapper_out.json')


def parse_args():
    """
    Parses input arguments and returns them to main.

    Exits on any raised exception or if any required arguments are missing.
    """
    args = ""
    output_file = ""
    jq = False
    omit_offline = False

    #Attempt to parse args
    try:
        opts, args = getopt.getopt(sys.argv[1:],"ha:f:",["help","args="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    #Populate local variables from args
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-a", "--args"):
            args = arg

    return (args)


def create_config_object(filepath):
    """
    Takes a string that holds a file path and attempts to read the file and
    parse the file as JSON.

    Returns:  Parsed json object via json.loads()

    Rasies:  IOError if the file cannot be read, TypeError on bad Type,
    ValueError on failed parsing.
    """
    try:
        json_raw = open(filepath).read()
        json_object = json.loads(json_raw)
    except IOError as err:
        print("Error:  Failed to open file %s!  Exiting..." % filepath)
        raise
    except TypeError as err:
        print("Error: Parsing of file %s failed!  Exiting..." % filepath)
        raise
    except ValueError as err:
        print("Error: Parsing of file %s failed!  Exiting..." % filepath)
        raise
    return json_object

def nmapper(args):
    #Create the object, exit on exception.
    try:
        nm = nmap.PortScanner()
    except nmap.PortScannerError:
        print('ERROR:  Nmap not found', sys.exc_info()[0])
        sys.exit(1)
    except:
        print('ERRPR:  Unexpected error:', sys.exc_info()[0])
        sys.exit(1)

    nm = nmap.PortScanner()
    nm.scan(arguments=args)
    nm.command_line()  #get the full nmap command
    nm.scaninfo()      #get all scan info
    nm.all_hosts()     #get all host objects

    #nm.all_hosts() will include 127.0.0.1, lets omit that.
    all_hosts = nm.all_hosts()
    try:
        all_hosts.remove("127.0.0.1")
    except ValueError:
        print("ERROR:  We raised ValueError trying to remove 127.0.0.1 from the list of hosts!  Investigate!")

    print("Executing NMAP via the following command:", nm.command_line())
    #Formatted to look nice on the screen
    for host in all_hosts:
        print('****************************************************************')
        print('Host : {0} ({1})'.format(host, nm[host].hostname()))
        print('State : {0}'.format(nm[host].state()))

        for proto in nm[host].all_protocols():
            print('----------')
            print('Protocol : {0}'.format(proto))

            lport = list(nm[host][proto].keys())
            lport.sort()
            for port in lport:
                print('port : {0}\tstate : {1}'.format(port, nm[host][proto][port]))
    print('****************************************************************')

    #Dump the json (just for debugging)
    #print(json.dumps(nm.all_hosts(), sort_keys=True, indent=4, separators=(',',':')))

    #Save the hosts that were confirmed to be UP on at least one port to a list as JSON:
    outputfile = './'+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+'.nmapper_out.json'
    try:
        with open(outputfile, 'w') as outfile:
            json.dump(all_hosts, outfile)
        print("UPDATE:  Output file successfully written to:", outputfile)
    except (OSError, IOError) as e:
        print("ERROR:  Failure to open output file %s!" % (outputfile))
        raise


def main():
    #Run begins
    print("\n**********NMAPper BEGIN RUN**********")

    #Parse args and populate file references
    (args) = parse_args()

    #INFO statements
    print('INFO: nmapper is starting...')

    #Run the nmap tool
    nmapper(args)

    #Run is complete
    print("\n**********NMAPper RUN FINISHED**********")

if __name__ == "__main__":
    main()
