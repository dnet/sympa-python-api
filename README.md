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

License
-------

The whole project is licensed under MIT license.

Dependencies
------------

 - Python 2.x (tested on 2.7)
 - LXML (Debian/Ubuntu package: `python-lxml`)
 - requests (http://docs.python-requests.org/)
