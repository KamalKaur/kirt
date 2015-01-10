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

For the installation of Requiremets, run the following commands in terminal:

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

2) Log into you mysql account using the command:
    
    $ mysql -u root -p

3) Create a new database for Kirt inside mysql shell:
    mysql> create database kirt;
    mysql> quit
    
4) Edit Kirt/kirt/settings.py file. Things to be edited are:

a) Database details: At Lines 69, 70, 80, fill your own details in following fields:
    
    NAME : kirt
    USER : <Your MySQL username>
    PASSWORD : <Your MySQl password>

b) Set all the paths: 

    (i) Line 31

    Modify this path to point your Kirt's template directory (Kirt/templates)
    '/home/username/path-to.../Kirt/templates',

    (ii) Line 95

    Modify this path to point to Kirt's static directory (Kirt/static) 
    '/home/username/path-to.../Kirt/static/'
    
4) Goto the project directory. 
    
    $ cd kirt

5) To fix your settings so that these can't be tracked by git and you can pull all the updates without an issue, run the following command inside cloned directory:

    $ git update-index --assume-unchanged kirt/settings.py


5) Now, run the following commands inside the directory Kirt only:

    $ python manage.py migrate
    $ python manage.py runserver 127.0.0.1:8090
    
6) Open 'http://localhost:8090' in your browser and you'll be greeted by the Kirt login page.
