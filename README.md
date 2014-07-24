Varnish Administration GUI 
==========================

* VCL Editor (vim like :))
* Purge

Required
========

* Python + Flask
* Varnish 3.x 4.x
* Varnish-agent 2.2+

knowledge "error"
=================
If you have this "error" on save VCL "VCL stored in varnish OK, but persisting to disk failed.", you need to set DAEMON_OPTS:

-n "/tmp" \

Because Varnish try to save in temporary directory /tmp and don't have access to do this.

To Do
=====

* Authentication
* User groups
* Graphics
* Save VCL edited on MySQL.

How to use
==========

This tool works with secret file value.

python vag.py

http://ip:5010

Screenshots
==========
![](http://i57.tinypic.com/scynox.png)
![](http://i62.tinypic.com/cryxj.png)
![](http://i58.tinypic.com/2z7j5lx.png)
![](http://i60.tinypic.com/2n1f20z.png)
![](http://s21.postimg.org/vzdv39r47/tela_editor.png)
