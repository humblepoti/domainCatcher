# domainCatcher
Script developed in Python 3.5 to check domain list for responding pages with HTTP Status Code. If a domain is identified an email notification is sent and its related hash is persisted in a shelve "db", otherwise a log file is created recording the exception generated during connection.

It was developed to be executed by a crontab task, periodically.
