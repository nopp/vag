import commands
import libvirt
import sqlite3
import time
import sys

# List Varnish's
def listVarnish():
	try:
		db = sqlite3.connect('vag.db')
		query = db.execute('select count(*) from varnish')
		total = int(query.fetchone()[0])
		varnishs = []
		if total >= 1:
			queryVarnish = db.execute('select * from varnish')
			for vns in queryVarnish.fetchall():
				vns = [vns[0],vns[1],vns[2],vns[3]]	
				varnishs.append(vns)
			return varnishs
		else:
			return "Please register your varnish's!"
	except:
		return "Error to connect on sqlite"

def addVarnish(name,ip,port,secret):
	try:
		db = sqlite3.connect('vag.db')
		query = db.execute('select count(*) from varnish where ip = ?', [ip]).fetchone()
		total = int(query[0])
		if total >= 1:
			return "This varnish "+ip+" has already been added!"
		else:
			db.execute('insert into varnish (name,ip,port,secret) values (?, ?, ?, ?)',[name,ip,port,secret])
			db.commit()
			return "Varnish"+name+" registered!"
	except:
		return "Error to connect on sqlite"
