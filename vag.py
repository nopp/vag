# Flak Module
from flask import *

# VAG Module
from lib.vag import *

# Varnish Socket API
from lib.vsapi import *

# Lib extras
import json
import ast

app = Flask(__name__)
app.secret_key = 'YG>.k*((*@jjkh>>'

@app.route("/")
def index():
	varnishs = listVarnish() 
	return render_template('home.html', varnishs=varnishs)

# Register new cluster
@app.route('/cluster')
def cluster():
	return render_template('addCluster.html')

@app.route('/register_cluster', methods=['POST'])
def registerCluster():
	if request.method == 'POST':
		rtn = addCluster(request.form['name'],request.form['secret'])
	flash(rtn)
	return redirect(url_for('index'))

# Register new varnish server
@app.route('/register')
def register():
    return render_template('addVarnish.html', clusters=returnClusters())

@app.route('/register_varnish', methods=['POST'])
def registerVarnish():
	ip = None
	if request.method == 'POST':
		rtn = addVarnish(request.form['name'],request.form['ip'],request.form['cluster'])
	flash(rtn)
	return redirect(url_for('index'))

# BAN varnish url or string
@app.route('/ban')
def purge():
    return render_template('ban.html', clusters=returnClusters())

@app.route('/url_ban', methods=['POST'])
def banUrl():
	if request.method == 'POST':
		rtn = urlBan(request.form['ban_url'],request.form['cluster'])
	flash(rtn)
	return redirect(url_for('index'))

@app.route('/vcl')
def vcl():
    return render_template('vcl.html', clusters=returnClusters())

@app.route('/vcl_edit', methods=['POST'])
def vclEdit():
	if request.method == 'POST':
		vclData = returnVcl(returnVclActive(request.form['cluster']),request.form['cluster'])
		return render_template('vcl_edit.html', vcl_data=vclData, clusterID=request.form['cluster'])

@app.route('/send_vcl', methods=['POST'])
def sendVcl():
	aux = ""
	if request.method == 'POST':
		for ln in request.form['vclConteudo'].splitlines():
			aux = aux+ln
		aux = aux.replace('"','\\"')
		aux = aux.replace('\t',' ')
		rtn = saveVCL("jucakk",request.form['clusterID'],aux)
		#rtn = aux
	flash(rtn)
	return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5010,debug=True)
