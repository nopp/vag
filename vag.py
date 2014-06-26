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
    return render_template('addVarnish.html')

@app.route('/register_varnish', methods=['POST'])
def registerVarnish():
	ip = None
	if request.method == 'POST':
		rtn = addVarnish("juca",request.form['ip'],request.form['port'],request.form['secret'])
	flash(rtn)
	return redirect(url_for('index'))

# Purge varnish url or string
@app.route('/purge')
def purge():
    return render_template('purge.html')

@app.route('/purge_url', methods=['POST'])
def purgeUrl():
    purge = None
    if request.method == 'POST':
        print request.form['ip']
	purge = request.form['ip']
    return render_template('purged.html',purge=ip)


# Purge varnish url or string
@app.route('/vcl')
def vcl():
    return render_template('vcl.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5010,debug=True)
