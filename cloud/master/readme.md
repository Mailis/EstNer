###This installation, for master, is tested on Ubuntu 14.10 and Ubuntu 15.04

sudo apt-get update

sudo apt-get install Apache2

sudo apt-get install php5

sudo apt-get install python-pip

sudo pip install --upgrade google-api-python-client



sudo apt-get install python3-pip

sudo pip3 install rdflib

####----------------------####


sudo apt-get install python-pip

sudo pip install --upgrade google-api-python-client


####--- download master files into folder /var/www/html ---####


####-----------------------####


cd /var/www/html

mv index.html apache2.html

sudo mkdir upload_logfile

sudo mkdir logfiles

sudo mkdir css

sudo mkdir js

sudo mkdir datasets

sudo mkdir SPARQLendpoint

sudo mkdir errors

sudo mkdir updates

sudo mkdir statistics

sudo mkdir statistics/processed_logfiles

sudo mkdir statistics/monthly_updates



