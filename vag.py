#
# VAG - Varnish Administration GUI
#
from flask import *
from lib.vag import *
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

app = Flask(__name__)
app.secret_key = 'aYG>.k*((*@jjkh>>'

# Index
@app.route("/")
def index():
	vag = Vag()
	return render_template('home.html', clt=vag.varnishByCluster())

# Manage Cluster/Varnish
@app.route("/manage")
def manage():
	vag = Vag()
	return render_template('manage.html', clt=vag.varnishByCluster())

# Manage users
@app.route("/users")
def users():
	vag = Vag()
	return render_template('users.html')

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

# Delete cluster
@app.route('/delete_cluster/<idCluster>', methods=['GET'])
def deleteCluster(idCluster):
	if request.method == 'GET':
		vag = Vag()
		rtn = vag.deleteCluster(idCluster)
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

# Varnish Edit
@app.route('/varnish/<idVarnish>', methods=['GET'])
def varnish(idVarnish):
	if request.method == 'GET':
		vag = Vag()
		return render_template('varnish.html', data=vag.varnishInfo(idVarnish))

@app.route('/varnish_edit', methods=['POST'])
def varnishEdit():
	if request.method == 'POST':
		vag = Vag()
		rtn = vag.editVarnish(request.form['varnishID'],request.form['name'],request.form['ip'])
	flash(rtn)
	return redirect(url_for('index'))

# Delete varnish
@app.route('/delete_varnish/<idVarnish>', methods=['GET'])
def deleteVarnish(idVarnish):
	if request.method == 'GET':
		vag = Vag()
		rtn = vag.deleteVarnish(idVarnish)
	flash(rtn)
	return redirect(url_for('index'))

# VCL Edit
@app.route('/vcl')
def vcl():
	vag = Vag()
	return render_template('vcl.html', clusters=vag.returnClusters())

@app.route('/vcl_edit', methods=['POST'])
def vclEdit():
	if request.method == 'POST':
		vag = Vag()
		vclData = vag.returnVcl(vag.returnVclActive(request.form['cluster']),request.form['cluster'])
		return render_template('vcl_edit.html', vcl_name=vag.returnVclActive(request.form['cluster']), vcl_data=vclData, clusterID=request.form['cluster'])

@app.route('/send_vcl', methods=['POST'])
def sendVcl():
	if request.method == 'POST':
		vag = Vag()
		rtn = vag.saveVCL(request.form['clusterID'],request.form['vclConteudo'])
	flash(rtn)
	return redirect(url_for('index'))

if __name__ == '__main__':
	vaIp = config.get('conf','vaIp')
	vaPort = config.get('conf','vaPort')
	app.run(host=vaIp,port=int(vaPort),debug=True)
