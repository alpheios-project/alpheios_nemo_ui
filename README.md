Alpheios Reader
===============
This repository contains templates, xslt and css for the Alpheios Reader Interface,
implemented as a plugin to https://github.com/Capitains/flask-capitains-nemo

## Development Environment Setup using Docker

Prerequisites: Docker and Docker-Compose

### Without Authentication Support
#### For Linux
```
git clone https://github.com/alpheios-project/alpheios_nemo_ui
cd alpheios_nemo_ui
./get_texts.sh
./docker-compose up
```
#### For Windows 10 (with WSL)
```
git clone https://github.com/alpheios-project/alpheios_nemo_ui
cd alpheios_nemo_ui
get_texts.bat
docker-compose up -d
```

Alpheios Reader flask application will be accessible at http://localhost:5000

### With Authentication Support

Prerequisites: alpheios-protected-config repo must be a sibling to the alpheios_nemo_ui clone
add dev.alpheios.net mapping for localhost to your /etc/hosts file

#### For Linux
```
git clone https://github.com/alpheios-project/alpheios_nemo_ui
cd alpheios_nemo_ui
./get_texts.sh
./setup_env.sh
./docker-compose up
```
#### For Windows 10 (with WSL)
```
git clone https://github.com/alpheios-project/alpheios_nemo_ui
cd alpheios_nemo_ui
get_texts.bat
setup_env.bat
docker-compose up -d
```

Alpheios Reader flask application will be accessible at http://dev.alpheios.net:5000


### Updating Alpheios Embedded library and styles

currently this is a manual process -- needs to be improved upon

copy the distribution build of the alpheios embedded library js files to `alpheios_nemo_ui/data/assets/js`
copy the distribution build of the alpheios embedded library css files to `alpheios_nemo_ui/data/assets/css`

rebuild the docker image using `docker-compose up --build`

### Updating the CSS for the Reader

The scss source files for the reader are in alpheios_nemo_ui/data/assets/scss

They are a customization of the Bootstrap 4 css library

Build via

```
cd alpheios_nemo_ui/data/assets
npm install
npm update
npm run build
```

rebuild the docker image using `docker-compose up --build`

### Updating the JS for the Reader

## Production Environment (via Puppet)

The puppet files that are currently used for the production deployment of apheios_nemo_ui can be found at https://github.com/alpheios-project/puppet/tree/master/site-modules/capitains

Important points:

1. the flask application uses a filesystem and redis server to cache some data
2. the flask application itself is served via a gunicorn server behind the firewall
3. an apache server proxies access to the flask application routes and serves the assets (css and javascript) directly

### Flask Application Caching
The flask application is configured to use a file system cache for textual data and a redis server to cache html fragments. Relevant lines from the production app.py:

```
http_cache = Cache(config={'CACHE_TYPE': "redis", "CACHE_REDIS_HOST": "localhost", "CACHE_DEFAULT_TIMEOUT": 0})
nautilus_cache = FileSystemCache("/tmp/ctscache", threshold=10000, default_timeout=28800)
```

The `nautlius_cache` caches the "pickled" python objects that represent the internal structures (i.e the `MyCapytain` data models) created by parsing the XML data files, to speed up retrieval of previously requested structures.

The `http_cache` contains fragments of specific html templates (used only where the templates specifically retrieve from thethe cache, as in the `referenches.html` template)

### Gunicorn config

the flask application is run by a gunicorn server on port 5000

```
CONFIG = {
  'mode': 'wsgi',
  'environment': {
    'LANG': 'en_US.UTF-8',
    'LC_ALL': 'en_US.UTF-8',
    'PYTHONPATH': '/usr/local/capitains/venvs'
  },
  'working_dir': '/usr/local/capitains',
  'user': 'www-data',
  'group': 'www-data',
  'python': '/usr/local/capitains/venvs/bin/python',
  'args': (
    '--bind=localhost:5000',
    '--workers=5',
    '--timeout=30',

    '--log-level=error',
    'app:app',
  ),
}
```

### Apache Config 
An apache server provides a reverse proxy to the gunicorn server (currently only on port 80 but 443 must be added)
apache also intercepts requests for assets. 


```
# ************************************
# Vhost template in module puppetlabs-apache
# Managed by Puppet
# ************************************

<VirtualHost *:80>
  ServerName texts-beta.alpheios.net

  ## Vhost docroot
  DocumentRoot "/tmp/capitains"
  ## Alias declarations for resources outside the DocumentRoot
  Alias /assets/nemo.secondary/static "/usr/local/capitains/alpheios_nemo_ui/data/assets/images"
  Alias /assets/nemo.secondary "/usr/local/capitains/alpheios_nemo_ui/data/assets"

  ## Directories, there should at least be a declaration for /tmp/capitains

  <Directory "/tmp/capitains">
    Options Indexes FollowSymLinks MultiViews
    AllowOverride None
    Require all granted
  </Directory>

  ## Logging
  ErrorLog "/var/log/apache2/texts_error.log"
  ServerSignature Off
  CustomLog "/var/log/apache2/texts_access.log" combined

  ## Header rules
  ## as per http://httpd.apache.org/docs/2.2/mod/mod_headers.html#header
  Header set Access-Control-Allow-Origin '*'
  Header set Access-Control-Allow-Methods 'GET, POST, OPTIONS'

  ## Proxy rules
  ProxyRequests Off
  ProxyPreserveHost Off
  ProxyPass /assets !
  ProxyPassReverse /assets !
  ProxyPass /api/dts http://dts.alpheios.net/api/dts
  ProxyPassReverse /api/dts http://dts.alpheios.net/api/dts
  ProxyPass /api/dts/ http://dts.alpheios.net/api/dts/
  ProxyPassReverse /api/dts/ http://dts.alpheios.net/api/dts/
  ProxyPass / http://localhost:5000/
  ProxyPassReverse / http://localhost:5000/
</VirtualHost>
```

### Other
Updates to the texts can be picked up by a cron job which runs the a script (puppet template for which is at https://github.com/alpheios-project/puppet/blob/master/site-modules/capitains/templates/update_capitains_repos.rb.erb)

