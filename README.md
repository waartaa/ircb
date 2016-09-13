
# ircb

A versatile IRC bouncer.

## Requirements

- Python3.5
- Pip3.5


## Setup

- Install dependencies:
``[sudo] pip3.5 install -r requirements.txt``

- Copy and extend ``ircb/config/default_settings.py``, as needed, to a custom location. say, ``/etc/ircb/settings.py``.
- [OPTIONAL] ``export IRCB_SETTINGS=<path to your custom settings file>``

- Install the project as a development dep ``python3.5 setup.py develop``

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
