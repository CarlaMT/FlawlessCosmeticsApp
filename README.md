## FlawLess Cosmetics Web App

### ABOUT

Flawless Cosmetic App is a web application created for the cosmetic company who wishes to keep track of their company's inventory.  This web application provides a list of items within a variety of categories through an authentication system.  Products are stored in a database and displayed on the website.  Registered users have the ability to post, edit and delete their items. 

### HOW TO USE
  * Install [VirtualBox 5.1.34](https://www.virtualbox.org/wiki/Changelog-5.1#v34)
  * Install [Vagrant](https://www.vagrantup.com/downloads.html)
  * Download this repository into any computer directory.
  * From your terminal, inside the vagrant sub-directory, run the command vagrant up.
  * After vagrant is up and running, run vagrant ssh.
  * At the command prompt, type cd  /vagrant to access the files containing the catalog.
  * Once inside, run the command lotsofproducts.py to fill the database. 
  * Run the command python catalog.py to run the web app from localhost.
  * Go into your preferred browser and type in localhost:5000 to view the index page. 
  * Finally, click on the login button to see the catalog of items.

### TOOLS USED

  * Python
  * Flask
  * SQLAlchemy
  * Boostrap
  * HTML
  * CSS
  * Google Chrome
