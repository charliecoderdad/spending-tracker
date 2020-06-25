# spending-tracker

## Install instructions (debian 10)

### Prepare python environment

Clone this spending tracker repo

  <code>git pull <thisrepo></code>
  
Create a virtual python enviornment to use

  <code>python3 -m venv <your environment></code>
  
Install python dependencies from requirements.txt file in the git repo

  <code>pip install -r requirements.txt</code>
  
### Configure Apache
Install Apache Web Server and dependency libs

<code>sudo apt install apach2e libapache2-mod-wsgi-py3</code>

Create /etc/apache2/sites-available/spending-tracker.conf apache with contents below.. ensure to modify as needed

```
 <VirtualHost :80>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    WSGIDaemonProcess tracker_app user=charlie group=charlie python-home=/home/charlie/python-env/spend-tracker-env threads=5
    WSGIScriptAlias / /home/charlie/git/spending-tracker/tracker_app.wsgi

    <Directory /home/charlie/git/spending-tracker>
  WSGIProcessGroup tracker_app
  WSGIApplicationGroup %{GLOBAL}
  Require all granted
  </Directory>
  </VirtualHost>
```

Disable default site in apache2

<code>sudo a2dissite 000-default.conf</code>

Enable your newly configured site

<code>sudo a2ensite spending-tracker.conf</code>

Restart apache service

<code>sudo apachectl restart</code>

### Database reset

To start with fresh database delete the sqlite db file inside the spending-tracker/tracker_app directory and restart apache.
