# CHANGE LOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.2.1] (2023-5-18)

- refactor openedx_plugin_mobile_api.middleware
- add secure-logger

## [0.2.0] (2023-3-31)

- publish to PyPi
- add Makefile
- refactor version modules
- add shields to README
- add meta data to pyproject.toml

## [0.1.3] (2023-3-30)

- add AGPLv3 license
- make xmodule imports backward compatible to nutmeg and earlier
- add __about__.py
- enhance setup.up setup() meta data
- bump classifier from alpha to beta
- refactor in order to make repo more condusive to uploading to PyPi
- version bumps to black, flake8 and their supporting plugins
- line entire code base for PEP 263 and B950 compliance
- setup pyproject.toml for PyPi publishing

## [0.1.2] (2023-3-29)

- add a module level IS_READY boolean to prevent ready() from running multiple times during init

## [0.1.1] (2022-12-29)

- add waffle_init() to waffle.py in each plugin
- call waffle_init() from ready() in each app config
- add manage.py init command to each plugin

## [0.1.0] (2022-12-28)

- added openedx_plugin_api code sample
- added openedx_plugin_cms code sample
- added openedx_plugin_mobile_api code sample
- added Waffle Switch feature toggling to all major features in this repo
- added Django Signals receivers scaffolding for all major signals published by openedx
- added middleware to optionally restore the Django Admin login page
- added wordpress_oauth2_backend.py
