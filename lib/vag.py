import commands
import MySQLdb
import urllib
from urlparse import urlparse
import subprocess
import time
import sys

# Varnish Socket API
from lib.vsapi import *

def connect():
	try:
		con = MySQLdb.connect(host='localhost', user='root', passwd='yourPassHere',db='vag')
		return con
	except:
		return "MySQL connection error!"

def connectVarnish(ip,secret):
	try:
		varnish = VarnishAdminSocket()
		varnish.host = ip
		varnish.port = 6082
		varnish.secret = secret+"\n" 
		varnish.connect()
		return varnish
	except:
		return "Can't connect on varnish "+ip

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

def addVarnish(name,ip,cluster):
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
			c.execute('insert into varnish (name,ip,id_cluster) values (%s, %s, %s)',[name,ip,cluster])
			con.commit()
			c.close()
			return "Varnish "+name+" registered!"
	except:
		return "Error to connect on MySQL"

def addCluster(name,secret):
	try:
		con = connect()
		c = con.cursor()
		c.execute('select count(*) from cluster where name = %s',[name])
		total = c.fetchone()[0]
		if total >= 1:
			c.close()
			return "This cluster "+ip+" has already been added!"
		else:
			c.execute('insert into cluster (name,secret) values (%s,%s)',[name,secret])
			con.commit()
			c.close()
			return "Cluster "+name+" registered!"
	except:
		return "Error to connect on MySQL"

def urlBan(url,cluster):
	con = connect()
	c = con.cursor()
	c.execute('select count(*) from varnish where id_cluster = %s',[cluster])
	total = c.fetchone()[0]
	result = urlparse(url)
	domain = result.netloc
	uri = result.path
	if total >= 1:
		c.execute('select * from varnish as v, cluster as c where v.id_cluster = c.id and v.id_cluster = %s',[cluster])
		for vns in c.fetchall():
			conVar = connectVarnish(vns[2],vns[6])
			conVar.ban('req.http.host ~ '+domain+' && req.url ~ ^'+uri+'$')	
			conVar.quit()
		c.close()
		return "Url "+url+" banned!"
	else:
		c.close()
		return "This url "+url+" not exists!"

def returnVclActive(cluster):
	try:
		con = connect()
		c = con.cursor()
		c.execute('select * from varnish as v, cluster as c where v.id_cluster = c.id and v.id_cluster = %s',[cluster])
		result = c.fetchone()
		conVar = connectVarnish(result[2],result[6])
		resultVcl = []
		resultVcl = conVar.vcl_list().split("\n")
		for vcl in resultVcl:
			resultAux = re.match("active",vcl)
			if resultAux:
				return vcl.split()[2]
	except:
		return "Don't have VCL active on this cluster"

def returnVcl(vclName,idCluster):
	try:
		con = connect()
		c = con.cursor()
		c.execute('select * from varnish as v, cluster as c where v.id_cluster = c.id and v.id_cluster = %s',[idCluster])
		result = c.fetchone()
		conVar = connectVarnish(result[2],result[6])
		resultVcl = conVar.vcl_show(vclName)
		return resultVcl
	except:
		return "Don't have VCL active on this cluster"
