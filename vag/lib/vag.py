#
# VAG - Varnish Administration GUI
#
import json
import socket
import urllib
import MySQLdb
import commands
import ConfigParser
from urlparse import urlparse
from time import gmtime, strftime

config = ConfigParser.RawConfigParser()
config.read('/etc/vag/config.cfg')

# Varnish Agent API
from lib.vsapi import *

class Vag:

	# MySQL connection
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

	# Return all clusters from DB
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
			else:
				return "Please register your clusters!"
		except:
			return "Please register your clusters!"

	# Return all varnish's from DB
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

	# Return cluter id (with cluster name)
	def returnClusterID(self,clusterName):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from cluster where name = %s',[clusterName])
			total = c.fetchone()[0]
			varnishs = []
			if total >= 1:
				c.execute('select * from cluster where name = %s',[clusterName])
				cID = c.fetchone()[0]
				c.close()	
				return cID
			else:
				c.close()
				return "Cluster "+clusterName+" doens't exists!"
		except:
			return "Error to connect on DB"

	# Return cluter name (with cluster id)
	def returnClusterNAME(self,clusterID):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from cluster where id = %s',[clusterID])
			total = c.fetchone()[0]
			varnishs = []
			if total >= 1:
				c.execute('select * from cluster where id = %s',[clusterID])
				cNAME = c.fetchone()[1]
				c.close()	
				return cNAME
			else:
				c.close()
				return "Cluster "+clusterID+" doens't exists!"
		except:
			return "Error to connect on DB"

	# Register new varnish
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

	# Return varnish info
	def varnishInfo(self,idVarnish):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from varnish where id = %s',[idVarnish])
			total = c.fetchone()[0]
			if total == 1:
				aux = []
				c.execute('select * from varnish where id = %s',[idVarnish])
				vaInfo = c.fetchone()
				# Varnish ID
				aux.append(vaInfo[0])
				# Varnish Name
				aux.append(vaInfo[1])
				# Varnish IP
				aux.append(vaInfo[2])
				# Cluster ID
				aux.append(vaInfo[3])
			return aux
		except:
			return "This varnish doesn't exists!"

	# Edit varnish
	def editVarnish(self,idVarnish,name,ip):
		con = self.connect()
		c = con.cursor()
		c.execute('select count(*) from varnish where id = %s',[idVarnish])
		total = c.fetchone()[0]
		if total >= 1:
			c.execute('update varnish set name = %s, ip = %s where id = %s',[name,ip,idVarnish])
			con.commit()
			c.close()
			return "Varnish edited!"
		else:
			c.close()
			return "VCL on "+vns[1]+" fail!"

	# Delete varnish
	def deleteVarnish(self,idVarnish):
		con = self.connect()
		c = con.cursor()
		c.execute('select count(*) from varnish where id = %s',[idVarnish])
		total = c.fetchone()[0]
		if total >= 1:
			c.execute('delete from varnish where id = %s',[idVarnish])
			con.commit()
			c.close()
			return "Varnish deleted!"
		else:
			c.close()
			return "Varnish delete fail!"

	# Delete cluster
	def deleteCluster(self,idCluster):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from cluster where id = %s',[idCluster])
			total = c.fetchone()[0]
			if total >= 1:
				c.execute('delete from varnish where id_cluster = %s',[idCluster])
				con.commit()
				c.execute('delete from cluster where id = %s',[idCluster])
				con.commit()
				c.close()
				return "Cluster deleted!"
			else:
				c.close()
				return "Cluster delete fail!"
		except:
			return "Cluster delete fail"

	# Register new cluster
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

	# Ban/Purge
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

	# Return all varnish's by cluster
	def varnishByCluster(self,name=None):
		con = self.connect()
		con2 = self.connect()
		c = con.cursor()
		v = con2.cursor()
		if name is None:
			try:
				c.execute('select count(*) from cluster')
				total = c.fetchone()[0]
				resultClusters = {}
				if total >= 1:
					c.execute('select * from cluster ORDER by name ASC')
					for cluster in c.fetchall():
						aux = []
						v.execute('select * from varnish where id_cluster = %s ORDER BY name ASC',[cluster[0]])
						resultClusters[cluster[1]] = []
						for varnish in v.fetchall():
							vsapi = vsApi()
							vsstatus =  vsapi.vcl_status(varnish[2])
							if "running" in vsstatus:
								rtnstatus = "OK"
							else:
								rtnstatus = "DESLIGADO"
							# idVarnish
							aux.append(varnish[0])
							# Varnish Name
							aux.append(varnish[1])
							# Varnish IP
							aux.append(varnish[2])
							# Varnish Status
							aux.append(rtnstatus)
							resultClusters[cluster[1]].append(aux)
							aux = []
			except:
				return "Error to return varnish from cluster!"
		else: 
			try:
				c.execute('select count(*) from cluster where name = %s',[name])
				total = c.fetchone()[0]
				resultClusters = {}
				if total >= 1:
					c.execute('select * from cluster where name = %s ORDER by name ASC',[name])
					for cluster in c.fetchall():
						aux = []
						v.execute('select * from varnish where id_cluster = %s ORDER BY name ASC',[cluster[0]])
						resultClusters[cluster[1]] = []
						for varnish in v.fetchall():
							vsapi = vsApi()
							vsstatus =  vsapi.vcl_status(varnish[2])
							if "running" in vsstatus:
								rtnstatus = "OK"
							else:
								rtnstatus = "DESLIGADO"
							# idVarnish
							aux.append(varnish[0])
							# Varnish Name
							aux.append(varnish[1])
							# Varnish IP
							aux.append(varnish[2])
							# Varnish Status
							aux.append(rtnstatus)
							resultClusters[cluster[1]].append(aux)
							aux = []
			except:
				return "Error to return varnish from specific cluster!"
		return resultClusters

	# Return last bans
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

    # Return status of varnish agent
    def varnishIsOnline(self,varnishIP):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        rst = s.connect_ex((varnishIP,6085))
        # Varnish Agent is on-line
        if rst == 0:
            return True
        # Varnish Agent is down
        else:
            return False

	# Return VCL activated
	def returnVclActive(self,cluster):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select * from varnish as v, cluster as c where v.id_cluster = c.id and v.id_cluster = %s',[cluster])
            for varnish in c.fetchall():
                if self.varnishIsOnline(varnish[2]):
                    varnishON = varnish[2]
                    break
			vsapi = vsApi()
			vclActive = vsapi.vcl_active(varnishON)
			return vclActive
		except:
			return "This cluster doesn't have VCL yet!"

	# Return VCL content
	def returnVcl(self,vclName,idCluster):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select * from varnish as v, cluster as c where v.id_cluster = c.id and v.id_cluster = %s',[idCluster])
            for varnish in c.fetchall():
                if self.varnishIsOnline(varnish[2]):
                    varnishON = varnish[2]
                    break
			vsapi = vsApi()
			resultVcl = vsapi.vcl_show(varnishON,vclName)
			# decode here isn't needed, but, if the user put ascii on default.vcl, this will be util
			if "message" not in dir(resultVcl):
				return resultVcl.decode('ascii','ignore')
			else:
				return "Varnish connection error "+result[2]
		except MySQLdb.Error, e:
			return "Don't have VCL active on this cluster"

	# Return VCL content from DB
	def returnVclDB(self,vclID):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select * from vcl where id = %s',[vclID])
			result = c.fetchone()
			return result
		except MySQLdb.Error, e:
			return "Don't have this VCL on DB!"

    # Save VCL
    def saveVCL(self,cluster,user,vclConteudo):
        con = self.connect()
        c = con.cursor()
        c.execute('select count(*) from varnish where id_cluster = %s',[cluster])
        total = c.fetchone()[0]
        if total >= 1:
            c.execute('select * from varnish as v, cluster as c where v.id_cluster = c.id and v.id_cluster = %s',[cluster])
            rtn = ""
            for vns in c.fetchall():
                if self.varnishIsOnline(vns[2]):
                    vsapi = vsApi()
                    # remove all ascii from VCL config
                    rtn = rtn+vns[2]+" - "+vsapi.vcl_save(vns[2],vclConteudo.encode('ascii','ignore'))
                else:
                    rtn = vns[2]+" down! "
            # Save VCL on DB one time
            self.saveVCLdb(cluster,user,vclConteudo.encode('ascii','ignore'))
            c.close()
            return rtn
        else:
            c.close()
            return "VCL on "+vns[1]+" fail!"

	# Save VCL on DB
	def saveVCLdb(self,cluster,user,content):
		con = self.connect()
		c = con.cursor()
		dateNow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		c.execute('insert into vcl(id_cluster,user,date,content) VALUES(%s,%s,%s,%s)',[cluster,user,dateNow,content])
		con.commit()

	# Return VCL history
	def vclHistory(self,clusterID):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select * from vcl where id_cluster = %s',[clusterID])
			total = c.fetchone()[0]
			vcls = []
			if total >= 1:
				c.execute('select * from vcl where id_cluster = %s order by id ASC LIMIT 10',[clusterID])
				for vns in c.fetchall():
					clusterName = self.returnClusterNAME(vns[1])
					vcl = []
					# VCL id
					vcl.append(vns[0])
					# VCL date
					vcl.append(vns[3])
					# User	
					vcl.append(vns[2])
					# Cluster name
					vcl.append(clusterName)
					vcls.append(vcl)
			return vcls
		except:
			return "VAG - VCL History fail!"

	# Return Cluster Stats
	# Will be sum all values of varnish cluster
	def clusterStats(self,idCluster):
		con = self.connect()
		c = con.cursor()
		c.execute('select count(*) from varnish where id_cluster = %s',[idCluster])
		total = c.fetchone()[0]
		totalVa = 0;
		totalVaMiss = 0;
		if total >= 1:
			c.execute('select * from varnish where id_cluster = %s',[idCluster])
			for vns in c.fetchall():
				vsapi = vsApi()
				# Check if agent is On-line
				vaStats = vsapi.varnish_stats(vns[2])
				rtn = json.loads(vaStats)
				totalVa = rtn["cache_hit"]["value"]+rtn["cache_miss"]["value"]+totalVa
				totalVaMiss = rtn["cache_miss"]["value"]+totalVaMiss
			return str(totalVa)+","+str(totalVaMiss) 

	# Return total of varnish and cluster from DB
	def vagInfo(self,table):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from '+table)
			total = c.fetchone()[0]
			return total
		except:
			return "vagInfo - MySQL error"

		
	# Verify login
	def verifyLogin(self,login,passwd):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from user where login = %s and pass = %s',[login,passwd])
			total = c.fetchone()[0]
			if total == 1:
				c.close()
				return True
			else:
				c.close()
				return False
		except:
			return False

	# Return group from user
	def returnGroup(self,login):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from user where login = %s',[login])
			total = c.fetchone()[0]
			if total == 1:
				c.execute('select * from user where login = %s',[login])
				userGroup = c.fetchone()[3]
				c.close()
				return userGroup
			else:
				c.close()
				return "User "+login+" doesn't exists!"
		except:
			return "returnGroup - Error!"
