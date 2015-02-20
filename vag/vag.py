#
# VAG - Varnish Administration GUI
#
import logging
from flask import *
from lib.vag import *
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('/etc/vag/config.cfg')

app = Flask(__name__)
app.secret_key = 'aYG>.k*((*@jjkh>>'

# Security
def verifyAdmin():
	if "vag_auth" in session:
		if session['vag_group'] == "admin":
			return True
		else:
			return False
	else:
		return False

# Login
@app.route("/login")
def login():
	return render_template('login.html')

# Verify login
@app.route("/verify", methods=['POST'])
def verify():
	if request.method == 'POST':
		vag = Vag()
		if vag.verifyLogin(request.form['login'],request.form['password']):
			session['vag_auth'] = request.form['login']
			session['vag_group'] = vag.returnGroup(request.form['login'])
			return redirect(url_for('index'))
		else:
			flash("Login error!")
			return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
    session.pop('vag_auth', None)
    session.pop('vag_group', None)
    return redirect(url_for('index'))

# Index
@app.route("/")
def index():
	vag = Vag()
	totalVA = vag.vagInfo("varnish")
	totalCL = vag.vagInfo("cluster")
	if "vag_auth" in session:
		return render_template('home.html', clt=vag.varnishByCluster(), totalcl=totalCL, totalva=totalVA)
	else:
		return redirect(url_for('login'))

# Manage Cluster/Varnish
@app.route("/manage")
def manage():
	if "vag_auth" in session:
		vag = Vag()
		return render_template('manage.html', clt=vag.varnishByCluster())
	else:
		flash("Please sign in!")
		return redirect(url_for('login'))

# Cluster
@app.route("/cluster_info/<clusterName>", methods=['GET'])
def clusterInfo(clusterName):
	if "vag_auth" in session:
		if request.method == 'GET':
			vag = Vag()
			return render_template('cluster_info.html', clt=vag.varnishByCluster(name=clusterName), name=clusterName)
	else:
		flash("Please sign in!")
		return redirect(url_for('login'))

# Cluster stats
@app.route("/cluster_stats/<clusterName>", methods=['GET'])
def clusterStats(clusterName):
	if "vag_auth" in session:
		if request.method == 'GET':
			vag = Vag()
			rtn = vag.clusterStats(vag.returnClusterID(clusterName))
		return rtn
	else:
		flash("Please sign in!")
		return redirect(url_for('login'))

# Register new cluster
@app.route('/cluster')
def cluster():
	if(verifyAdmin()):
		return render_template('addCluster.html')
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

@app.route('/register_cluster', methods=['POST'])
def registerCluster():
	if(verifyAdmin()):
			vag = Vag()
			if request.method == 'POST':
				vag = Vag()
				rtn = vag.addCluster(request.form['name'])
			flash(rtn)
			return redirect(url_for('index'))
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

# Delete cluster
@app.route('/delete_cluster/<clusterName>', methods=['GET'])
def deleteCluster(clusterName):
	if(verifyAdmin()):
		if request.method == 'GET':
			vag = Vag()
			cID = vag.returnClusterID(clusterName)
			rtn = vag.deleteCluster(cID)
		flash(rtn)
		return redirect(url_for('manage'))
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

# Register new varnish server
@app.route('/register')
def register():
	if(verifyAdmin()):
		vag = Vag()
		return render_template('addVarnish.html', clusters=vag.returnClusters())
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

@app.route('/register_varnish', methods=['POST'])
def registerVarnish():
	if(verifyAdmin()):
		ip = None
		if request.method == 'POST':
			vag = Vag()
			rtn = vag.addVarnish(request.form['name'],request.form['ip'],request.form['cluster'])
		flash(rtn)
		return redirect(url_for('index'))
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

# BAN varnish url or string
@app.route('/ban')
def purge():
	if(verifyAdmin()):
		vag = Vag()
		return render_template('ban.html', clusters=vag.returnClusters(), ban=vag.lastBans())
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

@app.route('/url_ban', methods=['POST'])
def banUrl():
	if(verifyAdmin()):
		if request.method == 'POST':
			vag = Vag()
			rtn = vag.urlBan(request.form['ban_domain'],request.form['ban_uri'],request.form['cluster'])
		flash(rtn)
		return redirect(url_for('purge'))
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

# Varnish Edit
@app.route('/varnish/<idVarnish>', methods=['GET'])
def varnish(idVarnish):
	if(verifyAdmin()):
		if request.method == 'GET':
			vag = Vag()
			return render_template('varnish.html', data=vag.varnishInfo(idVarnish))
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

@app.route('/varnish_edit', methods=['POST'])
def varnishEdit():
	if(verifyAdmin()):
		if request.method == 'POST':
			vag = Vag()
			rtn = vag.editVarnish(request.form['varnishID'],request.form['name'],request.form['ip'])
		flash(rtn)
		return redirect(url_for('index'))
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

# Delete varnish
@app.route('/delete_varnish/<idVarnish>', methods=['GET'])
def deleteVarnish(idVarnish):
	if(verifyAdmin()):
		if request.method == 'GET':
			vag = Vag()
			rtn = vag.deleteVarnish(idVarnish)
		flash(rtn)
		return redirect(url_for('manage'))
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

# VCL Edit
@app.route('/vcl')
def vcl():
	if "vag_auth" in session:
		vag = Vag()
		return render_template('vcl.html', clusters=vag.returnClusters())
	else:
		return redirect(url_for('login'))

@app.route('/vcl_edit', methods=['POST'])
def vclEdit():
	if "vag_auth" in session:
		if request.method == 'POST':
			vag = Vag()
			vclData = vag.returnVcl(vag.returnVclActive(request.form['cluster']),request.form['cluster'])
			return render_template('vcl_edit.html', vcl_name=vag.returnVclActive(request.form['cluster']), vcl_data=vclData, clusterID=request.form['cluster'])
	else:
		return redirect(url_for('login'))

@app.route('/send_vcl', methods=['POST'])
def sendVcl():
	if(verifyAdmin()):
		if request.method == 'POST':
			vag = Vag()
			rtn = vag.saveVCL(request.form['clusterID'],request.form['user'],request.form['vclConteudo'])
		flash(rtn)
		return redirect(url_for('index'))
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

@app.route('/history')
def history():
	if(verifyAdmin()):
		vag = Vag()
		return render_template('history.html', clusters=vag.returnClusters())
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

@app.route('/vcl_history', methods=['POST'])
def vclHistory():
	if(verifyAdmin()):
		if request.method == 'POST':		
			vag = Vag()
			return render_template('vcl_history.html', vcl_history=vag.vclHistory(request.form['cluster']), cluster_name=vag.returnClusterNAME(request.form['cluster']))
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

@app.route('/vcl_history_view/<vclID>', methods=['GET'])
def vclHistoryView(vclID):
	if(verifyAdmin()):
		if request.method == 'GET':
			vag = Vag()
			return render_template('vcl_history_view.html', vcl_data=vag.returnVclDB(vclID))
		else:
			flash("Restricted area!")
			return redirect(url_for('login'))

if __name__ == '__main__':
	# Log
	logging.basicConfig(filename='/var/log/vag/app.log',level=logging.DEBUG)
	# Run APP
	vaIp = config.get('conf','vaIp')
	vaPort = config.get('conf','vaPort')
	app.run(host=vaIp,port=int(vaPort))
