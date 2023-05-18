# Open edX Plugin Masterclass

A collaborative project to create an online course, hosted on Open edX software obviously, that provides comprehensive instruction on the development of good Open edX plugins.

## Syllabus

### Module I: "Hello World!"

the classical starting point. this module will be a detailed step-by-step green shoots project to create a plugin from scratch that implements a new URL that returns a json dict with a "hello-world" key and value. the teaching objective is to demonstrate the exact minimum necessities for creating a plugin that is discoverable by open edx and that returns a static result from a new URL endpoint.

### Module II: The Open edX plugin framework's technical architecture

This will be a detailed deep-dive into how Open edX and Django discover and consume an Open edX plugin, as well as what a plugin needs to include in order for it to be discovered, and why.

### Module III: Good programming practice

this modules begins with hello world, and then adds the following:

- refactor to leverage openedx helper constants and plugin utility functions
- a README
- additional meta data to setup.py
- add __about__.py
- add a makefile
- add a LICENSE.txt
- add a CHANGELOG.md

### Module IV: Creating an effective plugin development environment in Windows/macOS

### Module V: Programming techniques

#### Part 1 - Fundamentals

- requirements, and how these work
- Mako templating and static assets
- adding a Django model to your plugin and exposing its contents in Django admin
- creating custom Django settings variables
- creating a manage.py command

#### Part 2 - Advanced programming techniques

- a repo with multiple Django apps
- custom oauth backend
- using middleware to set login page to an upstream platform
- using middleware to alter the behavior of lms and cms urls
- using Django signals to create event-driven custom functionality
- using Waffle flags to control your custom functionality at run time

### Module VI: System management

- leveraging the app logs
- automatically initializing your Django models at app install/startup
- passing secrets/passwords to your plugin
- verifying that your plugins are installed and running, and are correctly configured

### Module VII: Taking code quality to the next level

- add pre-commit with black and flake8
- unit tests
- implementing semantic versioning, in Pythin, github, pip, and PyPi
- publishing your Open edX plugin to PyPi
