# Github workflows to Sentry

This app listens to GH webhook events from workflows events and stores the data as
transactions in Sentry.

## Pre-requisites

We're using Flask and for the development server you need to set some env variables. [direnv](https://github.com/direnv/direnv) is used to load the variables from the `env` file.

You're welcome to use some other tool to load these variables

## Requirements

- Python 3
- ngrok (for local dev)

### Set up for local development

Install ngrok, authenticate and start it up:

```shell
ngrok http 5000
```

Take note of the URL given and create a Github webhook (only `workflow` events & make sure to choose `application/json`) with that URL.

To start up the flask app:

```shell
cd 2021
# These steps are not necessary if you have direnv
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt
# direnv loads three env variables
flask run
```
