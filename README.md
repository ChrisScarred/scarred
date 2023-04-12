# Scarred

This repository contains the source code of a personal web app indended for publishing my educational and personal projects.

## Instructions

1. *If needed,* install mkcert.
2. Make a certificate for localhost, put to the folder `certs/local` as `cert.pem` and `key.pem`.
3. Fill in env values in `example.env` and save as `.env`, fill in config values in `example.yaml` and save it wherever your `APP_CONFIG_PATH` points.
4. *Optionally,* adjust values in `src/resources/locales/en.yaml`, `src/resources/routes.yaml` and `src/resources/templates/favicons.html`. If desired, put your own favicons in `src/resources/static/pics`.
5. *If needed,* make a Python virtual environment, activate it, and install dependencies from `requirements.txt`.
6. Run from the project's root folder via:

```bash
python -m src.app
```

An example flow:

```bash
mkcert -key-file key.pem -cert-file cert.pem example.com *.example.com
echo APP_CONFIG_PATH="myconfig.yaml" > .env
cp example.yaml myconfig.yaml
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.app
```
