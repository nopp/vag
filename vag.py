# Flak Module
from flask import *

# VAG Module
from lib.vag import *

# Varnish Socket API
# from lib.vsapi import *

# Lib extras
import json
import ast
import time
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

app = Flask(__name__)
app.secret_key = 'aYG>.k*((*@jjkh>>'

@app.route("/")
def index():
	vag = Vag()
	return render_template('home.html', clt=vag.varnishByCluster())

# Register new cluster
@app.route('/cluster')
def cluster():
	return render_template('addCluster.html')

@app.route('/register_cluster', methods=['POST'])
def registerCluster():
	if request.method == 'POST':
		vag = Vag()
		rtn = vag.addCluster(request.form['name'])
	flash(rtn)
	return redirect(url_for('index'))

# Register new varnish server
@app.route('/register')
def register():
	vag = Vag()
	return render_template('addVarnish.html', clusters=vag.returnClusters())

@app.route('/register_varnish', methods=['POST'])
def registerVarnish():
	ip = None
	if request.method == 'POST':
		vag = Vag()
		rtn = vag.addVarnish(request.form['name'],request.form['ip'],request.form['cluster'])
	flash(rtn)
	return redirect(url_for('index'))

# BAN varnish url or string
@app.route('/ban')
def purge():
	vag = Vag()
	return render_template('ban.html', clusters=vag.returnClusters(), ban=vag.lastBans())

@app.route('/url_ban', methods=['POST'])
def banUrl():
	if request.method == 'POST':
		vag = Vag()
		rtn = vag.urlBan(request.form['ban_domain'],request.form['ban_uri'],request.form['cluster'])
	flash(rtn)
	return redirect(url_for('index'))

@app.route('/vcl')
def vcl():
	vag = Vag()
	return render_template('vcl.html', clusters=vag.returnClusters())

@app.route('/vcl_edit', methods=['POST'])
def vclEdit():
	if request.method == 'POST':
		vag = Vag()
		vclData = vag.returnVcl(vag.returnVclActive(request.form['cluster']),request.form['cluster'])
		return render_template('vcl_edit.html', vcl_data=vclData, clusterID=request.form['cluster'])

@app.route('/send_vcl', methods=['POST'])
def sendVcl():
	if request.method == 'POST':
		vag = Vag()
		rtn = vag.saveVCL(request.form['clusterID'],request.form['vclConteudo'])
	flash(rtn)
	return redirect(url_for('index'))

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(host='127.0.0.1',port=5000,debug=True)
=======
	vaIp = config.get('conf','vaIp')
	vaPort = config.get('conf','vaPort')
	app.run(host=vaIp,port=int(vaPort),debug=True)
>>>>>>> 91c2890dce91f5e908c877771837c2d055e99d6e
