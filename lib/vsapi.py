#
# VAG - Varnish Administration GUI
#
import re
import urllib2
import ConfigParser
from urllib2 import Request, urlopen, URLError

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

class vsApi():
		
	# Return varnish status
	def vcl_status(self,ipAgent):
		uName = config.get('conf','vaName')
		pWord = config.get('conf','vaPass')
		userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
		req = urllib2.Request('http://'+ipAgent+':6085/status/')
		req.add_header('Accept', 'application/json')
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		req.add_header('Authorization', userData)
		try:
			rtn = urllib2.urlopen(req,timeout = 2)
			return rtn.read()
		except URLError, e:
			return e.reason

	# Return last VCL added
	def lastVCL(self,ipAgent):
		uName = config.get('conf','vaName')
		pWord = config.get('conf','vaPass')
		userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
		req = urllib2.Request('http://'+ipAgent+':6085/vcl/')
		req.add_header('Accept', 'application/json')
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		req.add_header('Authorization', userData)
		try:
			res = []
			res = urllib2.urlopen(req,timeout = 2).read().splitlines()
			return res[-1].split()[2]
		except URLError, e:
			return e.read()

	# Return VCL activated
	def vcl_active(self,ipAgent):
		uName = config.get('conf','vaName')
		pWord = config.get('conf','vaPass')
		userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
		req = urllib2.Request('http://'+ipAgent+':6085/vclactive/')
		req.add_header('Accept', 'application/json')
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		req.add_header('Authorization', userData)
		try:
			rtn = urllib2.urlopen(req,timeout = 2)
			return rtn.read()
		except URLError, e:
			return e.reason

	# Return content of VCL
	def vcl_show(self,ipAgent,vclName):
		uName = config.get('conf','vaName')
		pWord = config.get('conf','vaPass')
		userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
		req = urllib2.Request('http://'+ipAgent+':6085/vcl/'+vclName)
		req.add_header('Accept', 'application/json')
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		req.add_header('Authorization', userData)
		try:
			res = urllib2.urlopen(req,timeout = 2)
			conteudo = res.read()
			aux = ""
			for line in conteudo.splitlines():
				if line.strip():
					if re.match("^}",line):
						aux = aux+line+'\n\n'
					else:
						aux = aux+line+'\n'
			conteudo = aux
			return conteudo
		except URLError, e:
			return e.read()

	# Save VCL
	def vcl_save(self,ipAgent,vclContent):
		uName = config.get('conf','vaName')
		pWord = config.get('conf','vaPass')
		userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
		req = urllib2.Request('http://'+ipAgent+':6085/vcl/', vclContent)
		req.get_method = lambda: 'POST'
		req.add_header('Accept', 'application/json')
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		req.add_header('Authorization', userData)
		try:
			res = urllib2.urlopen(req,timeout = 2)
			vclName = self.lastVCL(ipAgent)
			rtn = res.read()+" "+self.vcl_use(ipAgent,vclName)
			return rtn
		except URLError, e:
			return e.read()

	# Active VCL
	def vcl_use(self,ipAgent,vclName):
		uName = config.get('conf','vaName')
		pWord = config.get('conf','vaPass')
		userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
		req = urllib2.Request('http://'+ipAgent+':6085/vcldeploy/'+vclName, data=vclName)
		req.add_header('Content-Type', 'text/plain')
		req.get_method = lambda: 'PUT'
		req.add_header('Authorization', userData)
		try:
			rtn = urllib2.urlopen(req,timeout = 2)
			if rtn.code == 200:
				rtn = "VCL "+vclName+" activated!"
			else:
				rtn = "VCL use error: "+rtn.msg
			return rtn
		except URLError, e:
			return e.read()

	# Ban/Purge
	def vcl_ban(self,ipAgent,domain,uri):
		uName = config.get('conf','vaName')
		pWord = config.get('conf','vaPass')
		userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
		req = urllib2.Request('http://'+ipAgent+':6085/ban/'+uri)
		req.get_method = lambda: 'POST'
		req.add_header('Accept', 'application/json')
		req.add_header('Host', domain)
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		req.add_header('Authorization', userData)
		try:
			rtn = urllib2.urlopen(req,timeout = 2)
			if rtn.code == 200:
				rtn = "http://"+domain+"/"+uri+" banned!"
			else:
				rtn = "BAN error: http://"+domain+"/"+uri
			return rtn
		except URLError, e:
			return str(e.reason)

	# List last 5 bans 
	def vcl_ban_list(self,ipAgent):
		uName = config.get('conf','vaName')
		pWord = config.get('conf','vaPass')
		userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
		req = urllib2.Request('http://'+ipAgent+':6085/ban/')
		req.add_header('Accept', 'application/json')
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		req.add_header('Authorization', userData)
		try:
			rtn = urllib2.urlopen(req,timeout = 1)
			list = []
			count = 0
			for line in rtn.read().splitlines():
				if not (line == "Present bans:"):
					# 5 last bans by cluter
					if count < 5:
						list.append(line.split()[2]+" "+line.split()[3]+" "+line.split()[4])
						count = count+1
					else:
						count = 0
						break
			return list
		except URLError, e:
			return e.reason
