kirt
====

REQUIREMENTS
------------
    1.Apache2
    2.mysql-server
    3.python2.7
    4.python-pip
    5.python-mysqldb
    6.django 1.7

For i nstallation of Requiremets, run the following command in terminal

1) Apache2
    
     $ sudo apt-get install apache2
     
2) mysql-server
    
    $ sudo apt-get install mysql-server
    
3) python2.7
    
    $ sudo apt-get install python
    
4) python-pip

    $ sudo apt-get install python-pip

5) python-mysqldb
    
    $ sudo apt-get install python-mysqldb

6) Django 1.7
    
    sudo pip install https://www.djangoproject.com/download/1.7.b4/tarball/


Steps for Installation of Kirt

1) Fork the repositery [kirt](https://github.com/KamalKaur/Kirt) and clone the forked repositery
    
    $ git clone 'link to your forked repository'

2) Create a database.
    
    $ mysql -u root -p
    $ create database kirt
    $ quit
    
3) Edit settings.py file. Things to be edited are:

Line No 10 : DATABASES
    
    NAME : kirt
    USER : Your MySQL username
    PASSWORD : Your MySQl password
    
4) Goto the project directory. 
    
    $ cd kirt

5) Run the following commands.

    $ python manage.py migrate
    $ python manage.py runserver 127.0.0.1:8090
    
6) Open 'localhost:8090' in your browser.
