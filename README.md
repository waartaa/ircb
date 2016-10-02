
# ircb

A versatile IRC bouncer.

## Requirements

- Python3.5
- Pip3.5


## Setup

- Install dependencies:

    ``[sudo] pip3.5 install -r requirements.txt``

- Copy and extend

    ``ircb/config/default_settings.py``, as needed,     to a custom location. say, ``/etc/ircb/settings.py``.

- [OPTIONAL] ``export IRCB_SETTINGS=<path to your custom settings file>``

- Install the project as a development dep

    ``python3.5 setup.py develop``

## Setup for development

- Install system dependencies:

    `` sudo dnf install python3-devel openssl-devel redis``

    `` sudo pip install virtualenvwrapper``

- Make `python3` virtualenv:

    ``mkvirtualenv --python=/usr/bin/python3 python3``

- Activate virtualenv:

    ``workon python3``

- Install dependencies:

    ``pip3 install -r requirements.txt``

- Install the project as development dep:

    ``python3.5 setup.py develop``

- Make sure `REDIS` is running:

    ``sudo systemctl start redis.service``

- Now, you need to run ``ircb stores``:

    ``ircb run stores``

Continue with `` Setting up data``

## Setting up data
- Creating a user:
  ```
  ircb users create USERNAME EMAIL [PASSWORD]
  ```

- Creating a network for a user:
  ```
  ircb networks create USER NETWORK_NAME HOST PORT NICK
  ```
  You'll get an access token as an output of the above. Use this as
  **server password** when configuring your IRC client to connect to ``ircb``.

## Running the app

### Quickstart
```
sudo ircb run allinone

```

Note: If you are using virtualenv `sudo` will not work this way, you need to
run:

```
sudo ~/.virtualenvs/python3/bin/ircb run allinone

```
### Advanced

You can run the various components of ``ircb``: ``stores``, ``bouncers`` as
different processes.

- Run stores as a different process: ``ircb run stores``
- Run bouncer: ``ircb run bouncer``
- Run web server: ``ircb run web``
- Run identd server: ``sudo ircb run identd``

## Connecting for IRC client

Now, you should be able to connect to ``ircb`` from your IRC client at:

- host/port: ``localhost/9000``

- server password: ``<your network access token>``

- IRC client should have the following settings enabled:

    * Use SSL for all server on this network
    * Accept invalid SSL certificate

### Configure HexChat

- Go to HexChat -> Network List

- Change the nick to the nick you have given while configuring network

- Under ``Network`` Click `Add` and name the server ``ircb``

- Click on `Edit` then `Add` and type `localhost/9000`

- Under ``Server`` tab check the ``SSL`` option mentioned above

- Enter the ``Server Password`` in `Password` field

- Close the dialog box and then connect to the network

Note: In case the problem persist try to ``restart`` ircb server
