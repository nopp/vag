# Flak Module
from flask import *

# VAG Module
from lib.vag import *

app = Flask(__name__)
app.secret_key = 'YG>.k*((*@jjkh>>'

@app.route("/")
def index():
	varnishs = listVarnish() 
	return render_template('login.html', varnishs=varnishs)

# Register new cluster
@app.route('/cluster')
def cluster():
    return render_template('addCluster.html')

@app.route('/register_cluster', methods=['POST'])
def registerCluster():
	if request.method == 'POST':
		rtn = addCluster(request.form['name'])
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
		rtn = addVarnish(request.form['name'],request.form['ip'],request.form['port'],request.form['secret'],request.form['cluster'])
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

# Purge varnish url or string
@app.route('/vcl')
def vcl():
    return render_template('vcl.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5010,debug=True)
