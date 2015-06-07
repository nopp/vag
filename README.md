Varnish Administration GUI 
=============================
(Open source VAC alternative)

* VCL Editor (vim like :))
* Purge/Ban
* Real time cluster info
* VCL change history

Obs:. I'm not a programmer :), do not expect a good code!

Required
========

* Python + Flask
* Varnish 3.x
* Varnish-agent 2.2+
* MySQL

How to install
==============

* yum install python-devel mariadb-devel
* pip install mysql-python
* git clone https://github.com/nopp/vag
* python setup.py install
* Create database VAG (on MySQL) and import /etc/vag/vag.sql
* Verify workdir on /etc/init.d/vag, if necessary change to the correct.
* Start the application: /etc/init.d/vag start
* Put vcl_updater.sh on cron, on all varnish agents: 

  10 * * * * vcl_updater.sh
  
  This little "hammer" will be fixed on the new versions.

How to access
=============

http://ip:5010

* Admin user: admin/admin
* View user: view/view
