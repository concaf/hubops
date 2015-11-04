#!/usr/bin/python2

import  time,sys,urllib2

# generating  code  for checking  apache http response code
#  remote  host  IP address
rhost_ip=sys.argv[1]

#  generating  function for http response code then page content

def  apache_check(rhost_ip):
#  sending http request to  remote host
	send_request=urllib2.urlopen("http://"+rhost_ip)
#   reading  response code
	response_code=send_request.code
#  checking  response code  
	if  response_code == 200 :
		receive_data=send_request.read()
		original_data=receive_data.split()
		if  original_data[0] == "welcome" :
			print "answer accepted !! "
		else :
			print  "page content is not okey"
	else :
		print  "Apache server is not working fine !!"



if __name__ == "__main__":
	apache_check(rhost_ip)




