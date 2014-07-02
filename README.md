Varnish Administration GUI 
==========================

Under development!

* VCL Editor
* Purge

Python + Flask

Varnish 3.X 4.X

Varnish config
==============

acl purge {
    "localhost";
    "0.0.0.0"/0;
}

vcl_recv
--------

    if (req.request == "PURGE") {
        if (!client.ip ~purge) {
            error 405 "Not allowed";
        }
        ban("req.http.host == " +req.http.host+" && req.url ~ "+req.url);
        error 200 "Ban added";
    }

How to use
==========

python vag.py

http://ip:5010

Screenhots
==========
![](http://s29.postimg.org/v3p1ohtlj/tela_3.png)
![](http://s29.postimg.org/lpsrfk93r/tela_x.png)
![](http://s17.postimg.org/e5xhb7ntb/tela1.png)
