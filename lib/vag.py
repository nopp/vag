import commands
import MySQLdb
import httplib
import urllib
from urlparse import urlparse
import subprocess
import time
import sys

def connect():
	try:
		con = MySQLdb.connect(host='localhost', user='root', passwd='passHere',db='vag')
		return con
	except:
		return "MySQL connection error!"

def returnClusters():
	try:
		con = connect()
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

def listVarnish():
	try:
		con = connect()
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

def addVarnish(name,ip,port,secret,cluster):
	try:
		con = connect()
		c = con.cursor()
		c.execute('select count(*) from varnish where ip = %s',[ip])
		total = c.fetchone()[0]
		print total
		if total >= 1:
			c.close()
			return "This varnish "+ip+" has already been added!"
		else:
			c.execute('insert into varnish (name,ip,port,secret,id_cluster) values (%s, %s, %s, %s, %s)',[name,ip,port,secret,cluster])
			con.commit()
			c.close()
			return "Varnish "+name+" registered!"
	except:
		return "Error to connect on MySQL"

def addCluster(name):
	try:
		con = connect()
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

def urlBan(url,cluster):
	try:
		con = connect()
		c = con.cursor()
		c.execute('select count(*) from varnish where id_cluster = %s',[cluster])
		total = c.fetchone()[0]
		result = urlparse(url)
		#print result
		domain = result.netloc
		uri = result.path
		if total >= 1:
			c.execute('select * from varnish where id_cluster = %s',[cluster])
			for vns in c.fetchall():
				# print vns[2]
				# Varnish IP
				conn = httplib.HTTPConnection(vns[2])
				# Domnain
				headers = {"Host": domain}	
				# URI to BAN
				conn.request("PURGE", uri, "", headers)
			c.close()
			return "Url "+url+" banned!"
		else:
			c.close()
			return "This url "+url+" not exists!"
	except:
		return "Error to connect on MySQL"
