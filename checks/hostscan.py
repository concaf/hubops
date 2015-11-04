#!/usr/bin/python


import  nmap,time,socket,sys

# creating  host scan requirement
#  storing  ip  address and port of target host  

rhost_ip=sys.argv[1]
rhost_port=sys.argv[2]


def  portstatus(rhost_ip,rhost_port):
	call_scan_function=nmap.PortScanner()
	nmap_reply=call_scan_function.scan(rhost_ip,rhost_port)
	#   nmap_reply variable receive data in dictonary form
	scan_status=nmap_reply['scan']
	#   converting  dictonary in form of list for making output simple
	status_in_list=scan_status.values()
	#  closure to result 
	scan_result=status_in_list[0]['tcp'].values()
	#    final port status 
	port_status=scan_result[0]['state']
	print  "host {0} showing port {1} status {2} !!!".format(rhost_ip,rhost_port,port_status)
#	print "remote is {0} and remote port is {1} ".format(rhost_ip,rhost_port)


portstatus(rhost_ip,rhost_port)




