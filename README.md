Alpheios UI Plugin for CapiTainS Nemo
====================================
This repository contains templates, xslt and css for the Alpheios Reader Interface,
implemented as a plugin to https://github.com/Capitains/flask-capitains-nemo

## Development Environment Setup using Docker

Prerequisites: Docker and Docker-Compose

### Without Authentication Support
git clone https://github.com/alpheios-project/alpheios_nemo_ui
cd alpheios_nemo_ui
./get_texts.sh
./docker-compose up

Alpheios Reader environment will be accessible at http://localhost:5000

### With Authentication Support

Prerequisites: alpheios-protected-config repo must be a sibling to the alpheios_nemo_ui clone
add dev.alpheios.net mapping for localhost to your /etc/hosts file
git clone https://github.com/alpheios-project/alpheios_nemo_ui
cd alpheios_nemo_ui
./get_texts.sh
./setup_env.sh
./docker-compose up

Alpheios Reader environment will be accessible at http://dev.alpheios.net:5000


