#
# VAG - Varnish Administration GUI
#
import re
import json
import pycurl
import urllib2
import ConfigParser
from urllib2 import Request, urlopen, URLError

config = ConfigParser.RawConfigParser()
config.read('/etc/vag/config.cfg')

class vsApi():

	# http://ipAgent/action/extra
	def urlRequest(self,ipAgent,action,extra=None,mtd=None,domain=None):
		uName = config.get('conf','vaName')
		pWord = config.get('conf','vaPass')
		userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
		if (extra != None):
			try:
				# Type of method (POST/PUT)
				if mtd == "POST":
					if action == "ban":
						req = urllib2.Request('http://'+ipAgent+':6085/'+action+'/'+str(extra))
						req.get_method = lambda: 'POST'
					else:
						req = urllib2.Request('http://'+ipAgent+':6085/'+action+'/',str(extra))
						req.get_method = lambda: 'POST'
				elif mtd == "PUT":
					req = urllib2.Request('http://'+ipAgent+':6085/'+action+'/'+str(extra), data=str(extra))
					req.get_method = lambda: 'PUT'
				else:
					req = urllib2.Request('http://'+ipAgent+':6085/'+action+'/'+str(extra))
				if domain != None:
					req.add_header('Host', domain)
				req.add_header('Accept', 'application/json')
				req.add_header("Content-type", "application/x-www-form-urlencoded")
				req.add_header('Authorization', userData)
				return req
			except URLError, e:
				return e.reason
		else:
			try:
				req = urllib2.Request('http://'+str(ipAgent)+':6085/'+str(action)+'/')
				req.add_header('Accept', 'application/json')
				req.add_header("Content-type", "application/x-www-form-urlencoded")
				req.add_header('Authorization', userData)
				return req
			except URLError, e:
				return e.reason

	# Return varnish status
	def vcl_status(self,ipAgent):
		try:
			req = self.urlRequest(ipAgent,"status")
			rtn = urllib2.urlopen(req,timeout = 2)
			return rtn.read()
		except URLError, e:
			return e.reason

	# Return last VCL added
	def lastVCL(self,ipAgent):
		try:
			req = self.urlRequest(ipAgent,"vcl")
			res = []
			res = urllib2.urlopen(req,timeout = 2).read().splitlines()
			return res[-1].split()[2]
		except URLError, e:
			return e.reason

	# Return VCL activated
	def vcl_active(self,ipAgent):
		try:
			req = self.urlRequest(ipAgent,"vclactive")
			rtn = urllib2.urlopen(req,timeout = 2)
			return rtn.read()
		except URLError, e:
			return e.reason

	# Return content of VCL
	def vcl_show(self,ipAgent,vclName):
		try:
			req = self.urlRequest(ipAgent,"vcl",vclName)
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
			return e.reason

	# Save VCL
	def vcl_save(self,ipAgent,vclContent):
		try:
			req = self.urlRequest(ipAgent,"vcl",vclContent,"POST")
			res = urllib2.urlopen(req,timeout = 2)
			vclName = self.lastVCL(ipAgent)
			rtn = res.read()+" "+self.vcl_use(ipAgent,vclName)
			return rtn
		except URLError, e:
			return e.read()

	# Active VCL
	def vcl_use(self,ipAgent,vclName):
		try:
			req = self.urlRequest(ipAgent,"vcldeploy",vclName,"PUT")
			rtn = urllib2.urlopen(req,timeout = 2)
			if rtn.code == 200:
				rtn = "VCL "+vclName+" activated!"
			else:
				rtn = "VCL use error: "+rtn.msg
			return rtn
		except URLError, e:
			return e.reason

	# Ban/Purge
	def vcl_ban(self,ipAgent,domain,uri):
		try:
			uName = config.get('conf','vaName')
			pWord = config.get('conf','vaPass')
			aData = uName+":"+pWord
			postData = "req.http.host ~ "+domain+" && req.url ~ /"+uri
			c = pycurl.Curl()
			c.setopt(pycurl.URL, 'http://'+ipAgent+':6085/ban')
			c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
			c.setopt(pycurl.HTTPHEADER, ['Host: '+str(domain)])
			c.setopt(pycurl.POST, 1)
			c.setopt(c.TIMEOUT, 2)
			c.setopt(pycurl.POSTFIELDS, str(postData))
			c.setopt(pycurl.USERPWD, aData)
			c.perform()
			return ipAgent+" Ban OK! "
		except:
			return ipAgent+" Ban failed! "

	# List last 5 bans 
	def vcl_ban_list(self,ipAgent):
		try:
			req = self.urlRequest(ipAgent,"ban")
			rtn = urllib2.urlopen(req,timeout = 1)
			list = []
			count = 0
			for line in rtn.read().splitlines():
				if not (line == "Present bans:"):
					# 5 last bans by cluter
					if count < 5:
						listBans = line.split()[2:]
						stringBans = ' '.join(listBans)
						list.append(stringBans)
						count = count+1
					else:
						count = 0
						# Sorry about that :(
						break
			return list
		except URLError, e:
			return e.read()

	# Return varnish stats
	def varnish_stats(self,ipAgent):
		try:
			req = self.urlRequest(ipAgent,"stats")
			rtn = urllib2.urlopen(req,timeout = 2)
			return rtn.read()
		except URLError, e:
			return e.read()