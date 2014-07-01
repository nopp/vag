from sqlite3 import dbapi2 as sqlite3

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
    return render_template('ban.html')

@app.route('/ban_url', methods=['POST'])
def purgeUrl():
    banned = None
    if request.method == 'POST':
        print request.form['ip']
	banned = request.form['ip']
    return render_template('banned.html',banned=ip)


# Purge varnish url or string
@app.route('/vcl')
def vcl():
    return render_template('vcl.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5010,debug=True)
