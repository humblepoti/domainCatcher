# domainCatcher
Script developed in Python 3.5 where its main goal is to check domain list for responding pages with HTTP Status Code. If a domain is identified a email is sent to an email and its hash is persisted in an shelve "db", otherwise a log file is created regarding the exception generated during connection.

It was developed to be executed by a crontab task, periodically.
