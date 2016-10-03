
0.3.0
-----

Pull Requests

- (@rtnpro)         #51, Implement basic API server for ircb
  https://github.com/waartaa/ircb/pull/51
- (@slick666)       #53, Changed update method to have immutable arguments.
  https://github.com/waartaa/ircb/pull/53
- (@sayanchowdhury) #55, Add default value to Network.status
  https://github.com/waartaa/ircb/pull/55
- (@slick666)       #57, Load ircb data from file
  https://github.com/waartaa/ircb/pull/57
- (@sayanchowdhury) #59, Implement logging, unified import layout
  https://github.com/waartaa/ircb/pull/59
- (@rtnpro)         #68, Implement logstore plugin
  https://github.com/waartaa/ircb/pull/68
- (@rtnpro)         #70, Realtime publishers
  https://github.com/waartaa/ircb/pull/70
- (@sayanchowdhury) #72, Fix the NetworkStore.create() to use the proper arguments
  https://github.com/waartaa/ircb/pull/72
- (@rtnpro)         #76, Forward sent channel messages for a bot client to it's siblings.
  https://github.com/waartaa/ircb/pull/76
- (@rtnpro)         #78, Allow running bouncer server with SSL. #77
  https://github.com/waartaa/ircb/pull/78
- (@sayanchowdhury) #56, Implement IDENT server.
  https://github.com/waartaa/ircb/pull/56
- (@rtnpro)         #79, Allinone run now runs web server as well.
  https://github.com/waartaa/ircb/pull/79
- (@farhaanbukhsh)  #80, Readdme fix
  https://github.com/waartaa/ircb/pull/80
- (@farhaanbukhsh)  #83, Fix readme for development
  https://github.com/waartaa/ircb/pull/83
- (@rtnpro)         #84, Cli verbose option
  https://github.com/waartaa/ircb/pull/84
- (@rtnpro)         #85, Cli fix allinone
  https://github.com/waartaa/ircb/pull/85
- (@sayanchowdhury) #86, Change the filetype of the CHANGELOG file
  https://github.com/waartaa/ircb/pull/86
- (@sayanchowdhury) #87, Update the MANIFEST.in file
  https://github.com/waartaa/ircb/pull/87
- (@sayanchowdhury) #88, Fix the license classifier in setup.py
  https://github.com/waartaa/ircb/pull/88

Commits

- 91f4d9fd8 Added to_dict() method to models.
  https://github.com/waartaa/ircb/commit/91f4d9fd8
- 0dbd9d51b Zeromq based distributed dispatcher.
  https://github.com/waartaa/ircb/commit/0dbd9d51b
- 97122e7f9 Represent model instances as dict in store response.
  https://github.com/waartaa/ircb/commit/97122e7f9
- ebf79a247 Deserialize dicts in store response to model instances in storeclient.
  https://github.com/waartaa/ircb/commit/ebf79a247
- 5b5bfbaad Return ChoiceField's code in serialized model data.
  https://github.com/waartaa/ircb/commit/5b5bfbaad
- 7c2bd0568 Allow locks and enqueuing messages in dispatcher.
  https://github.com/waartaa/ircb/commit/7c2bd0568
- 1d54c7187 Sync and register storeclient subscribers to store publisher.
  https://github.com/waartaa/ircb/commit/1d54c7187
- c58010396 Updated README.
  https://github.com/waartaa/ircb/commit/c58010396
- 363ed45b6 Added missing run.py in cli module.
  https://github.com/waartaa/ircb/commit/363ed45b6
- f48bdd976 Connect to IRC when status of NetworkStore is set to '0' (connect).
  https://github.com/waartaa/ircb/commit/f48bdd976
- 6dd53ab28 Fix registering first client to bot
  https://github.com/waartaa/ircb/commit/6dd53ab28
- 6eb6c9eaa Initialize dispatcher for storeclient for CLI.
  https://github.com/waartaa/ircb/commit/6eb6c9eaa
- 0269e778f Disconnect bot when network status set to '2'.
  https://github.com/waartaa/ircb/commit/0269e778f
- bd7f9ae68 Added list, connect, disconnect commands for ircb networks.
  https://github.com/waartaa/ircb/commit/bd7f9ae68
- 8ca1d5598 Don't run process_queue in Dispatcher as a long running task.
  https://github.com/waartaa/ircb/commit/8ca1d5598
- 9fd8cf5c9 Speed dispatcher init process.
  https://github.com/waartaa/ircb/commit/9fd8cf5c9
- 2d89224c3 Use loop.run_forever() to run dispatcher server.
  https://github.com/waartaa/ircb/commit/2d89224c3
- 0f83f99b1 Don't keep redis connection open in dispatcher.
  https://github.com/waartaa/ircb/commit/0f83f99b1
- 3c7695da0 Allow re connecting a disconnected bot.
  https://github.com/waartaa/ircb/commit/3c7695da0
- 2503ac2d0 Prevent race condition when registering subscribers to stores.
  https://github.com/waartaa/ircb/commit/2503ac2d0
- af24973b4 Scrap previous flask web app.
  https://github.com/waartaa/ircb/commit/af24973b4
- 5273a3282 Allow authenticating a user from stores.
  https://github.com/waartaa/ircb/commit/5273a3282
- 1b03583f3 Initial work on web API.
  https://github.com/waartaa/ircb/commit/1b03583f3
- 160f16218 Use aiohttp_auth to improve Sign{In,Out} API for user.
  https://github.com/waartaa/ircb/commit/160f16218
- e48a9f777 Added new requirements.
  https://github.com/waartaa/ircb/commit/e48a9f777
- 01286e0dd Implement auth_required decorator and SignoutView.
  https://github.com/waartaa/ircb/commit/01286e0dd
- a24b2d5c2 Allow storclient stores to list available fields.
  https://github.com/waartaa/ircb/commit/a24b2d5c2
- a0160060c Added base web Views for ircb with some utilities:
  https://github.com/waartaa/ircb/commit/a0160060c
- a6435dc76 Added view to list IRC networks for a logged in user.
  https://github.com/waartaa/ircb/commit/a6435dc76
- 461ef51ba Remove unused import.
  https://github.com/waartaa/ircb/commit/461ef51ba
- 81e5e820a Fix to_dict() in network model.
  https://github.com/waartaa/ircb/commit/81e5e820a
- 93c7c4824 Initial implementation of network details, create API.
  https://github.com/waartaa/ircb/commit/93c7c4824
- bc3e90c6a Allow generating a serializable dict representation for a model row.
  https://github.com/waartaa/ircb/commit/bc3e90c6a
- 8156135eb Explicitly specify API version: v1 in routes.
  https://github.com/waartaa/ircb/commit/8156135eb
- 9fb31cbdd Cleaned up network model definition.
  https://github.com/waartaa/ircb/commit/9fb31cbdd
- 0c7011504 Added wtforms-alchemy as a requirement.
  https://github.com/waartaa/ircb/commit/0c7011504
- 25e5f31af Added NetworkForm.
  https://github.com/waartaa/ircb/commit/25e5f31af
- a92a01752 Use NetworkForm to validate data in network create API.
  https://github.com/waartaa/ircb/commit/a92a01752
- b83c48865 Add network update API.
  https://github.com/waartaa/ircb/commit/b83c48865
- d1ad19f08 Added network connect/disconnect API.
  https://github.com/waartaa/ircb/commit/d1ad19f08
- 3a8f01e78 Added user signup API.
  https://github.com/waartaa/ircb/commit/3a8f01e78
- 97182313f Added user form.
  https://github.com/waartaa/ircb/commit/97182313f
- f52170cc2 fix the default utcnow time for generating access token
  https://github.com/waartaa/ircb/commit/f52170cc2
- ce4f2a774 Changed update method to have immutable arguments. bumped SQLAlchemy to 1.0.9 to get the one_or_none function bumped click to 6.3 because I couldn't get it to with 6.2 Added msgpack-python 0.4.7 to suppress error
  https://github.com/waartaa/ircb/commit/ce4f2a774
- c900ded69 models: add default value to Network.status
  https://github.com/waartaa/ircb/commit/c900ded69
- 96cb513eb Load ircb data from file. Fixes #25
  https://github.com/waartaa/ircb/commit/96cb513eb
- b9e194629 Minor typo fix and update requirements.txt
  https://github.com/waartaa/ircb/commit/b9e194629
- 6012aaeac Fix the import layout, Implement logging framework
  https://github.com/waartaa/ircb/commit/6012aaeac
- e596ff271 Added Tox testing configuration Added simple documentation under the tests folder Added trivial test under the tests folder did simple pep8 cleanup to fix the pep8 tox test Added TravisCI integration
  https://github.com/waartaa/ircb/commit/e596ff271
- 0bf606744 Added CLI to launch web server.
  https://github.com/waartaa/ircb/commit/0bf606744
- 1283b735c Bumped SQLAlchemy version to 1.0.13.
  https://github.com/waartaa/ircb/commit/1283b735c
- 58d0d67e0 Updated README.
  https://github.com/waartaa/ircb/commit/58d0d67e0
- 9fc44d7e7 Bump to version 0.2
  https://github.com/waartaa/ircb/commit/9fc44d7e7
- c4da551a6 Added models for storing IRC logs. #64
  https://github.com/waartaa/ircb/commit/c4da551a6
- f87c3a501 Store user id in irc3 bot instance. #64
  https://github.com/waartaa/ircb/commit/f87c3a501
- e05d7658e Added stores for MessageLog and ActivityLog. #64
  https://github.com/waartaa/ircb/commit/e05d7658e
- 36ab0ecfc Added plugin for storing IRC logs. #64
  https://github.com/waartaa/ircb/commit/36ab0ecfc
- 256dedbab Scaffolding realtime publisher.
  https://github.com/waartaa/ircb/commit/256dedbab
- 1ae93af39 Allow fetching raw results from storeclient
  https://github.com/waartaa/ircb/commit/1ae93af39
- e94e77421 Support fetching logs from MessageLog store. #71
  https://github.com/waartaa/ircb/commit/e94e77421
- 06eb88549 Working MessageLog publisher. Fixes #71
  https://github.com/waartaa/ircb/commit/06eb88549
- b9a37b32e Fixed pep8 errors.
  https://github.com/waartaa/ircb/commit/b9a37b32e
- 8cad048cb Fixed out of place debuggers in publisher.
  https://github.com/waartaa/ircb/commit/8cad048cb
- 13954a49d Optimize skip filters for MessageLogPublisher. #71
  https://github.com/waartaa/ircb/commit/13954a49d
- 7fcacfd6d Optimize query to fetch latest N MessageLogs. #71
  https://github.com/waartaa/ircb/commit/7fcacfd6d
- 18ca5807e In publisher, clean up item from index when removed from results.
  https://github.com/waartaa/ircb/commit/18ca5807e
- a71308eff Allow adding callbacks to create/update events of publisher.
  https://github.com/waartaa/ircb/commit/a71308eff
- 090608bf1 Bugfixes in ircb publisher.
  https://github.com/waartaa/ircb/commit/090608bf1
- 13e1202e5 Added 'fetch' callback in publisher.
  https://github.com/waartaa/ircb/commit/13e1202e5
- a508196c6 Fix serializing message logs when publishing from stores.
  https://github.com/waartaa/ircb/commit/a508196c6
- 66bb47044 Created a base publisher class
  https://github.com/waartaa/ircb/commit/66bb47044
- 8c3b16ebb Fix the NetworkStore.create() to use the proper arguments
  https://github.com/waartaa/ircb/commit/8c3b16ebb
- 6883f7e6f Some fixes in base publisher.
  https://github.com/waartaa/ircb/commit/6883f7e6f
- 1a78ab15e Added network publisher.
  https://github.com/waartaa/ircb/commit/1a78ab15e
- 572533017 Improve GET api for channel stores. Fixes #73
  https://github.com/waartaa/ircb/commit/572533017
- bebf7d7e0 Add realtime publisher for channels. Fixes #74
  https://github.com/waartaa/ircb/commit/bebf7d7e0
- 8aa6a32dd Fix serializing & deserializing data. Fixes #75
  https://github.com/waartaa/ircb/commit/8aa6a32dd
- e41a5fa4b Added 'id' property to ChannelPublisher. #75
  https://github.com/waartaa/ircb/commit/e41a5fa4b
- f1fe34e2f Fixed irc3 integration bug: USER not enough params.
  https://github.com/waartaa/ircb/commit/f1fe34e2f
- 643d279da Don't remove builtins from settings module.
  https://github.com/waartaa/ircb/commit/643d279da
- ab232620b Forward sent channel messages for a bot client to it's siblings.
  https://github.com/waartaa/ircb/commit/ab232620b
- d1f7d8bac Update to irc3 0.9.3
  https://github.com/waartaa/ircb/commit/d1f7d8bac
- 084b24d5a Use network.username, if available, for irc3 bot config
  https://github.com/waartaa/ircb/commit/084b24d5a
- 97ff477aa Allow running bouncer server with SSL. #77
  https://github.com/waartaa/ircb/commit/97ff477aa
- cc6ea1a07 Initial work on the ident server
  https://github.com/waartaa/ircb/commit/cc6ea1a07
- 3508fa23d Implement working identd server.
  https://github.com/waartaa/ircb/commit/3508fa23d
- 3894e86c6 Refactor run command to open room for identd server.
  https://github.com/waartaa/ircb/commit/3894e86c6
- 15f69504e Refactor allinone CLI command to move implementation outside of bouncer.
  https://github.com/waartaa/ircb/commit/15f69504e
- 7200a4321 Integrate identd server with CLI
  https://github.com/waartaa/ircb/commit/7200a4321
- c5dd25b75 Fix implementation of identd server
  https://github.com/waartaa/ircb/commit/c5dd25b75
- 78ca6ac2d Bugfix during saving connection info for a IRC connection.
  https://github.com/waartaa/ircb/commit/78ca6ac2d
- 4a11950d4 Allinone run now runs web server as well.
  https://github.com/waartaa/ircb/commit/4a11950d4
- a1ca0b3b7 Fix setup file
  https://github.com/waartaa/ircb/commit/a1ca0b3b7
- 7a3242126 Fix readme and add intructions for development
  https://github.com/waartaa/ircb/commit/7a3242126
- 254596c0b Add virtualwrapper dependency
  https://github.com/waartaa/ircb/commit/254596c0b
- 8800da6c9 Fix readme for development
  https://github.com/waartaa/ircb/commit/8800da6c9
- 4b45e5b3c Minor fix in readme
  https://github.com/waartaa/ircb/commit/4b45e5b3c
- a5a273942 Add steps to configure IRC client
  https://github.com/waartaa/ircb/commit/a5a273942
- d29f9943b Add verbose option in ircb CLI.
  https://github.com/waartaa/ircb/commit/d29f9943b
- fda09d34e Show status message when running stores server.
  https://github.com/waartaa/ircb/commit/fda09d34e
- 929482ee1 Show bouncer endpoint when running in allinone mode.
  https://github.com/waartaa/ircb/commit/929482ee1
- 8d6d82f11 Drop unused variable in bouncer.
  https://github.com/waartaa/ircb/commit/8d6d82f11
- 55b3079bf Make running identd in allinone mode optional.
  https://github.com/waartaa/ircb/commit/55b3079bf
- b61bae91f Print web server endpoint during startup.
  https://github.com/waartaa/ircb/commit/b61bae91f
- 3c51e2b5c Change the filetype of the CHANGELOG file
  https://github.com/waartaa/ircb/commit/3c51e2b5c
- 1b30a0fbf Update the MANIFEST.in file
  https://github.com/waartaa/ircb/commit/1b30a0fbf
- 9a4a4b25b Fix the license classifier in setup.py
  https://github.com/waartaa/ircb/commit/9a4a4b25b
# Change Log

## [0.2](https://github.com/waartaa/ircb/tree/0.2) (2016-05-29)

[Full Changelog](https://github.com/waartaa/ircb/compare/0.1.1...0.2)

**Closed issues:**

- asyncio sqlalchemy compatability? [\#50](https://github.com/waartaa/ircb/issues/50)
- not able to connect python to mysql [\#46](https://github.com/waartaa/ircb/issues/46)
- /.meteor/meteor' is not executable. [\#45](https://github.com/waartaa/ircb/issues/45)
- python.h directory is not there [\#44](https://github.com/waartaa/ircb/issues/44)
- Add a logging framework [\#43](https://github.com/waartaa/ircb/issues/43)
- Replace in memory dispatcher with one based on zeromq [\#30](https://github.com/waartaa/ircb/issues/30)

**Merged pull requests:**

- Implement logging, unified import layout [\#59](https://github.com/waartaa/ircb/pull/59) ([sayanchowdhury](https://github.com/sayanchowdhury))
- Minor typo fix and update requirements.txt [\#58](https://github.com/waartaa/ircb/pull/58) ([sayanchowdhury](https://github.com/sayanchowdhury))
- Load ircb data from file [\#57](https://github.com/waartaa/ircb/pull/57) ([slick666](https://github.com/slick666))
- Add default value to Network.status [\#55](https://github.com/waartaa/ircb/pull/55) ([sayanchowdhury](https://github.com/sayanchowdhury))
- Proposed Tox and TravisCI for CI/CD [\#54](https://github.com/waartaa/ircb/pull/54) ([slick666](https://github.com/slick666))
- Changed update method to have immutable arguments. [\#53](https://github.com/waartaa/ircb/pull/53) ([slick666](https://github.com/slick666))
- Implement basic API server for ircb [\#51](https://github.com/waartaa/ircb/pull/51) ([rtnpro](https://github.com/rtnpro))
- Server side flux for ircb [\#48](https://github.com/waartaa/ircb/pull/48) ([rtnpro](https://github.com/rtnpro))
- Zmq dispatcher. Fixes \#30 [\#41](https://github.com/waartaa/ircb/pull/41) ([rtnpro](https://github.com/rtnpro))

## [0.1.1](https://github.com/waartaa/ircb/tree/0.1.1) (2016-01-01)
[Full Changelog](https://github.com/waartaa/ircb/compare/0.1...0.1.1)

**Fixed bugs:**

- Fix marking user as not AWAY [\#36](https://github.com/waartaa/ircb/issues/36)
- Fix sending AWAY command [\#32](https://github.com/waartaa/ircb/issues/32)

**Merged pull requests:**

- Fix marking nick as not AWAY. Fixes \#36 [\#37](https://github.com/waartaa/ircb/pull/37) ([rtnpro](https://github.com/rtnpro))
- Revert "Fix marking user as away. \#32" [\#35](https://github.com/waartaa/ircb/pull/35) ([rtnpro](https://github.com/rtnpro))
- Fix marking user as away. \#32 [\#34](https://github.com/waartaa/ircb/pull/34) ([rtnpro](https://github.com/rtnpro))

## [0.1](https://github.com/waartaa/ircb/tree/0.1) (2015-12-20)
**Implemented enhancements:**

- Load ircb data from file [\#25](https://github.com/waartaa/ircb/issues/25)
- Autjoin previously joined channels when connected to IRC server [\#27](https://github.com/waartaa/ircb/issues/27)
- Add support for ssl, ssl\_verify fields in "ircb networks create" command [\#22](https://github.com/waartaa/ircb/issues/22)
- Connect to IRC server using SSL [\#18](https://github.com/waartaa/ircb/issues/18)
- Allow SSL connection to IRC networks [\#17](https://github.com/waartaa/ircb/issues/17)
- Dynamically generate IRC joining messages for clients when reusing existing IRC connection [\#11](https://github.com/waartaa/ircb/issues/11)

**Fixed bugs:**

- Don't send ChoiceType field in IrcbBot config for network for ssl\_verify [\#23](https://github.com/waartaa/ircb/issues/23)
- Fix handling multiple IRC clients for same bot [\#8](https://github.com/waartaa/ircb/issues/8)

**Closed issues:**

- ircb networks create does not work [\#20](https://github.com/waartaa/ircb/issues/20)
- Monthly release for ircb [\#10](https://github.com/waartaa/ircb/issues/10)
- Sent messages using IrcbIrcBot is prefixed with ':' [\#6](https://github.com/waartaa/ircb/issues/6)
- Prevent race condition during two clients trying to connect to the same IRC network [\#15](https://github.com/waartaa/ircb/issues/15)

**Merged pull requests:**

- Autjoin previously joined channels when connecting to IRC server. [\#28](https://github.com/waartaa/ircb/pull/28) ([rtnpro](https://github.com/rtnpro))
- Implemented: Add support for ssl, ssl\_verify fields in 'ircb networks create' command. issue \#22 [\#24](https://github.com/waartaa/ircb/pull/24) ([PolBaladas](https://github.com/PolBaladas))
- Fixed issue \#20 'ircb network create does not work' [\#21](https://github.com/waartaa/ircb/pull/21) ([PolBaladas](https://github.com/PolBaladas))
- Allow connecting to IRC server using SSL. Fixes \#18 [\#19](https://github.com/waartaa/ircb/pull/19) ([rtnpro](https://github.com/rtnpro))
- Fixes race condition during multiple clients connecting to same network [\#16](https://github.com/waartaa/ircb/pull/16) ([rtnpro](https://github.com/rtnpro))
- Dynamic irc join messages [\#14](https://github.com/waartaa/ircb/pull/14) ([rtnpro](https://github.com/rtnpro))
- Add local & remote socket info for a IRC network connection [\#13](https://github.com/waartaa/ircb/pull/13) ([rtnpro](https://github.com/rtnpro))
- Add alembic to manage migration [\#12](https://github.com/waartaa/ircb/pull/12) ([rtnpro](https://github.com/rtnpro))
- Improve handling of raw messages from IRC clients. Fixes \#6 [\#7](https://github.com/waartaa/ircb/pull/7) ([rtnpro](https://github.com/rtnpro))
- Use irc3 bot to interact with remote IRC server. [\#5](https://github.com/waartaa/ircb/pull/5) ([rtnpro](https://github.com/rtnpro))
- Added stores for ircb [\#4](https://github.com/waartaa/ircb/pull/4) ([rtnpro](https://github.com/rtnpro))
- minor typo fix in README [\#3](https://github.com/waartaa/ircb/pull/3) ([sayanchowdhury](https://github.com/sayanchowdhury))
- update the README for setting up ircb on dev environments [\#2](https://github.com/waartaa/ircb/pull/2) ([sayanchowdhury](https://github.com/sayanchowdhury))
- Update installation docs from pip to pip3 [\#1](https://github.com/waartaa/ircb/pull/1) ([sayanchowdhury](https://github.com/sayanchowdhury))



\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*
