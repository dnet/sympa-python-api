Sympa Python API
================

Usage
-----

The `sympa` module offers the `Sympa` class, which represents a Sympa node. The constructor takes only one parameter, the URL of the site, and then the `login` method can be used to authenticate with an e-mail address and password. Currently, supported functionality includes a read-only access to shared files (listing and reading).

	>>> from sympa import Sympa
	>>> s = Sympa()
	>>> s.log_in('https://db.bme.hu/lists', 'username', 'password')
	>>> a.lists
	{'konzi.adatlabor': <MailingList "konzi.adatlabor">}

Also, the `sympafs` module can be used to mount the shared files of mailing lists to the file system using FUSE (Linux, Mac OS X and FreeBSD are supported).

	$ python sympafs.py https://db.bme.hu/lists username konzi.adatlabor /tmp/sympa
	Password:
	$ ls -la /tmp/sympa
	total 16
	dr-xr-xr-x  2 root root     0 Mar 25 22:23 .
	drwxrwxrwx 18 root root 16384 Mar 25 22:20 ..
	dr-xr-xr-x  2 root root     0 Feb 14  2005 2002
	dr-xr-xr-x  2 root root     0 Feb 14  2005 2003
	...
	$ fusermount -u /tmp/sympa

License
-------

The whole project is licensed under MIT license.

Dependencies
------------

 - Python 2.x (tested on 2.7)
 - LXML (Debian/Ubuntu package: `python-lxml`)
 - requests (http://docs.python-requests.org/)
 - fusepy (for SympaFS only, http://code.google.com/p/fusepy/)
