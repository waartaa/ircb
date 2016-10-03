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
