import commands
import MySQLdb
import urllib
from urlparse import urlparse
import subprocess
import time
import sys
import re
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

# Varnish Agent API
from lib.vsapi import *

class Vag:

		def connect(self):
			mHost = config.get('conf','mysqlHost')
			mUser = config.get('conf','mysqlUser')
			mPass = config.get('conf','mysqlPass')
			mDb = config.get('conf','mysqlDb')
			try:
				con = MySQLdb.connect(host=mHost, user=mUser, passwd=mPass,db=mDb)
				return con
			except:
				return "MySQL connection error!"

		def returnClusters(self):
			try:
				con = self.connect()
				c = con.cursor()
				c.execute('select count(*) from cluster')
				total = c.fetchone()[0]
				clusters = []
				if total >= 1:
					c.execute('select * from cluster')
					for cst in c.fetchall():
						cst = [cst[0],cst[1]]	
						clusters.append(cst)
					c.close()
					return clusters
			except:
				return "Please register your clusters!"

		def listVarnish(self):
			try:
				con = self.connect()
				c = con.cursor()
				c.execute('select count(*) from varnish')
				total = c.fetchone()[0]
				varnishs = []
				if total >= 1:
					c.execute('select * from varnish')
					for vns in c.fetchall():
						vns = [vns[0],vns[1],vns[2],vns[3]]	
						varnishs.append(vns)
					c.close()	
					return varnishs
				else:
					c.close()
					return "Please register your varnish's!"
			except:
				return "Error to connect on sqlite"

		def addVarnish(self,name,ip,cluster):
			try:
				con = self.connect()
				c = con.cursor()
				c.execute('select count(*) from varnish where ip = %s',[ip])
				total = c.fetchone()[0]
				if total >= 1:
					c.close()
					return "This varnish "+ip+" has already been added!"
				else:
					c.execute('insert into varnish (name,ip,id_cluster) values (%s, %s, %s)',[name,ip,cluster])
					con.commit()
					c.close()
					return "Varnish "+name+" registered!"
			except:
				return "Error to connect on MySQL"

		def addCluster(self,name):
			try:
				con = self.connect()
				c = con.cursor()
				c.execute('select count(*) from cluster where name = %s',[name])
				total = c.fetchone()[0]
				if total >= 1:
					c.close()
					return "This cluster "+ip+" has already been added!"
				else:
					c.execute('insert into cluster (name) values (%s)',[name])
					con.commit()
					c.close()
					return "Cluster "+name+" registered!"
			except:
				return "Error to connect on MySQL"

		def urlBan(self,domain,uri,cluster):
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from varnish where id_cluster = %s',[cluster])
			total = c.fetchone()[0]
			if total >= 1:
				c.execute('select * from varnish as v, cluster as c where v.id_cluster = c.id and v.id_cluster = %s',[cluster])
				rtn = ""
				vsapi = vsApi()	
				for vns in c.fetchall():
					rtn = rtn+vsapi.vcl_ban(vns[2],domain,uri)+"\n"
				c.close()
				return rtn
			else:
				c.close()
				return rtn

		def varnishByCluster(self):
			con = self.connect()
			con2 = self.connect()
			c = con.cursor()
			v = con2.cursor()
			c.execute('select count(*) from cluster')
			total = c.fetchone()[0]
			resultClusters = {}
			if total >= 1:
				c.execute('select * from cluster ORDER by name ASC')
				for cluster in c.fetchall():
					aux = []
					v.execute('select * from varnish where id_cluster = %s ORDER BY name ASC',[cluster[0]])
					for varnish in v.fetchall():
						aux.append(varnish[1]+" ("+varnish[2]+")")
					resultClusters[cluster[1]] = aux
			return resultClusters

		def lastBans(self):
			con = self.connect()
			con2 = self.connect()
			c = con.cursor()
			v = con2.cursor()
			c.execute('select count(*) from cluster')
			total = c.fetchone()[0]
			resultBans = {}
			if total >= 1:
				c.execute('select * from cluster ORDER by name ASC')
				for cluster in c.fetchall():
					aux = []
					v.execute('select * from varnish where id_cluster = %s ORDER BY name ASC LIMIT 1',[cluster[0]])
					for varnish in v.fetchall():
						vsapi = vsApi()
						aux.append(vsapi.vcl_ban_list(varnish[2]))
					resultBans[cluster[1]] = aux
			return resultBans

		def returnVclActive(self,cluster):
			con = self.connect()
			c = con.cursor()
			c.execute('select * from varnish as v, cluster as c where v.id_cluster = c.id and v.id_cluster = %s',[cluster])
			result = c.fetchone()
			vsapi = vsApi()
			vclActive = vsapi.vcl_active(result[2])
			return vclActive

		def returnVcl(self,vclName,idCluster):
			try:
				con = self.connect()
				c = con.cursor()
				c.execute('select * from varnish as v, cluster as c where v.id_cluster = c.id and v.id_cluster = %s',[idCluster])
				result = c.fetchone()
				vsapi = vsApi()
				resultVcl = vsapi.vcl_show(result[2],vclName)
				return resultVcl
			except:
				return "Don't have VCL active on this cluster"

		def saveVCL(self,cluster,vclConteudo):
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from varnish where id_cluster = %s',[cluster])
			total = c.fetchone()[0]
			if total >= 1:
				c.execute('select * from varnish as v, cluster as c where v.id_cluster = c.id and v.id_cluster = %s',[cluster])
				for vns in c.fetchall():
					vsapi = vsApi()
					rtn = vsapi.vcl_save(vns[2],vclConteudo)	
				c.close()
				return rtn
			else:
				c.close()
				return "VCL on "+vns[1]+" fail!"
