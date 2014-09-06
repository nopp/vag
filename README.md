Varnish Administration GUI 
=============================
(Open source VAC alternative)

* VCL Editor (vim like :))
* Purge

Obs:. I'm not a programmer :), do not expect a good code!

Required
========

* Python + Flask
* Varnish 3.x 4.x
* Varnish-agent 2.2+
* MySQL

To Do
=====

* Graphics

How to install
==============

1) git clone https://github.com/nopp/vag
2) python setup.py install
3) Create database VAG (on MySQL) and import /etc/vag/vag.sql
4) Verify workdir on /etc/init.d/vag, if necessary change to the correct.
5) Start the application: /etc/init.d/vag start

How to access
=============

http://ip:5010

* Admin user: admin/admin
* View user: view/view


Screenshots
==========
![](http://rapido.taxi.br/img/tela_home.png)
![](http://rapido.taxi.br/img/register_varnish.png)
![](http://rapido.taxi.br/img/tela_ban.png)
![](http://rapido.taxi.br/img/cluster_status.png)
![](http://rapido.taxi.br/img/tela_edit.png)
