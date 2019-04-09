Alpheios Reader
===============
This repository contains templates, xslt and css for the Alpheios Reader Interface,
implemented as a plugin to https://github.com/Capitains/flask-capitains-nemo

## Development Environment Setup using Docker

Prerequisites: Docker and Docker-Compose

### Without Authentication Support
```
git clone https://github.com/alpheios-project/alpheios_nemo_ui
cd alpheios_nemo_ui
./get_texts.sh
./docker-compose up
```

Alpheios Reader flask application will be accessible at http://localhost:5000

### With Authentication Support

Prerequisites: alpheios-protected-config repo must be a sibling to the alpheios_nemo_ui clone
add dev.alpheios.net mapping for localhost to your /etc/hosts file

```
git clone https://github.com/alpheios-project/alpheios_nemo_ui
cd alpheios_nemo_ui
./get_texts.sh
./setup_env.sh
./docker-compose up
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
