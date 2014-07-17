import urllib2
from urllib2 import Request, urlopen, URLError
import re
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

class vsApi():

		def lastVCL(self,ipAgent):
			uName = config.get('conf','vaName')
			pWord = config.get('conf','vaPass')
			userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
			req = urllib2.Request('http://172.16.253.40:6085/vcl/')
			req.add_header('Accept', 'application/json')
			req.add_header("Content-type", "application/x-www-form-urlencoded")
			req.add_header('Authorization', userData)
			try:
				res = []
				res = urllib2.urlopen(req).read().splitlines()
				return res[-1].split()[2]
			except URLError, e:
				return e.read()

		def vcl_active(self,ipAgent):
			uName = config.get('conf','vaName')
			pWord = config.get('conf','vaPass')
			userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
			req = urllib2.Request('http://'+ipAgent+':6085/vclactive/')
			req.add_header('Accept', 'application/json')
			req.add_header("Content-type", "application/x-www-form-urlencoded")
			req.add_header('Authorization', userData)
			try:
				rtn = urllib2.urlopen(req)
				return rtn.read()
			except URLError, e:
				return e.read()	

		def vcl_show(self,ipAgent,vclName):
			uName = config.get('conf','vaName')
			pWord = config.get('conf','vaPass')
			userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
			req = urllib2.Request('http://'+ipAgent+':6085/vcl/'+vclName)
			req.add_header('Accept', 'application/json')
			req.add_header("Content-type", "application/x-www-form-urlencoded")
			req.add_header('Authorization', userData)
			try:
				res = urllib2.urlopen(req)
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
				res = urllib2.urlopen(req)
				# Use VCL
				vclName = self.lastVCL(ipAgent)
				rtn = res.read()+" "+self.vcl_use(ipAgent,vclName)
				return rtn
			except URLError, e:
				return e.read()

		def vcl_use(self,ipAgent,vclName):
			uName = config.get('conf','vaName')
			pWord = config.get('conf','vaPass')
			userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
			req = urllib2.Request('http://'+ipAgent+':6085/vcldeploy/'+vclName, data=vclName)
			req.add_header('Content-Type', 'text/plain')
			req.get_method = lambda: 'PUT'
			req.add_header('Authorization', userData)
			try:
				rtn = urllib2.urlopen(req)
				if rtn.code == 200:
					rtn = "VCL "+vclName+" activated!"
				else:
					rtn = "VCL use error: "+rtn.msg
				return rtn
			except URLError, e:
				return e.read()

		def vcl_ban(self,ipAgent,domain,uri):
			print domain
			print uri
			uName = config.get('conf','vaName')
			pWord = config.get('conf','vaPass')
			userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
			req = urllib2.Request('http://'+ipAgent+':6085/ban'+uri)
			req.get_method = lambda: 'POST'
			req.add_header('Accept', 'application/json')
			req.add_header('Host', domain)
			req.add_header("Content-type", "application/x-www-form-urlencoded")
			req.add_header('Authorization', userData)
			try:
				rtn = urllib2.urlopen(req)
				if rtn.code == 200:
					rtn = "http://"+domain+"/"+uri+" banned!"
				else:
					rtn = "BAN error: http://"+domain+"/"+uri+" "+rtn.msg
				return rtn
			except URLError, e:
				return e.read()
