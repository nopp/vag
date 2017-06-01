Varnish Administration GUI 
=============================
(Open source VAC alternative)

* VCL Editor
* Purge/Ban
* Real time cluster info
* VCL change history

Obs:. I'm not a programmer :), do not expect a good code!

Required
========

* Python + Flask
* Varnish 3.x
* Varnish-agent 2.2
* MySQL

How to install
==============

VAGENT2.2
  # yum install libmicrohttpd-devel libcurl-devel varnish-libs-devel
  # wget https://github.com/varnish/vagent2/archive/2.2.0.tar.gz
  # tar zxvf 2.2.0.tar.gz
  # cd vagent2-2.2.0/ && ./autoge.sh && ./configure && make && make install
  # echo "varnish:yourPass" > /etc/varnish/agent_secret
  # varnish-agent

VAG
  # yum install python-devel mariadb-devel mysql-devel
  # pip install mysql-python
  # git clone https://github.com/nopp/vag
  # python setup.py install
  # Create database VAG (on MySQL) and import /etc/vag/vag.sql
  # Verify workdir on /etc/init.d/vag, if necessary change to the correct.
  # Start the application: /etc/init.d/vag start
  Put vcl_updater.sh on cron, on all varnish agents: 

  10 * * * * vcl_updater.sh
  
  This little "hammer" will be fixed on the new versions.

How to access
=============

http://ip:5010

* Admin user: admin/admin
* View user: view/view

Screenshots
===========
![Image Alt](http://i66.tinypic.com/whzc.png)
![Image Alt](http://i67.tinypic.com/w9tzb8.png)
![Image Alt](http://i67.tinypic.com/29xuhlj.png)
![Image Alt](http://i65.tinypic.com/25in39w.png)
