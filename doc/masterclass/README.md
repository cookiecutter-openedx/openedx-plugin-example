# Open edX Plugin Masterclass

A collaborative project to create an online course, hosted on Open edX software obviously, that provides comprehensive instruction on the development of good Open edX plugins.

## Syllabus

### Module I: "Hello World!"

(instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md))

the classical starting point. this module will be a detailed step-by-step green shoots project to create a plugin from scratch that implements a new URL that returns a json dict with a "hello-world" key and value. the teaching objective is to demonstrate the exact minimum necessities for creating a plugin that is discoverable by open edx and that returns a static result from a new URL endpoint.

### Module II: The Open edX plugin framework's technical architecture

(instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md))

This will be a detailed deep-dive into how Open edX and Django discover and consume an Open edX plugin, as well as what a plugin needs to include in order for it to be discovered, and why.

### Module III: Good programming practice

(instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md))

this modules begins with hello world, and then adds the following:

- refactor to leverage openedx helper constants and plugin utility functions
- a README
- additional meta data to setup.py
- add __about__.py
- add a makefile
- add a LICENSE.txt
- add a CHANGELOG.md

### Module IV: Creating an effective plugin development environment in Windows/macOS

(instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md))

### Module V: Programming techniques

#### Part 1 - Fundamentals

- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) requirements, and how these work
- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) Mako templating and static assets
- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) Adding a Django model to your plugin and exposing its contents in Django admin
- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) Creating custom Django settings variables
- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) Creating a manage.py command

#### Part 2 - Advanced programming techniques

- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) A repo with multiple Django apps
- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) Create custom oauth backend
- (instructor: [Lawrence McDaniel](https://github.com/lpm0073)) Using middleware to set login page to an upstream platform
- (instructor: [Lawrence McDaniel](https://github.com/lpm0073)) Using middleware to alter the behavior of lms and cms urls
- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) Using Django signals to create event-driven custom functionality
- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) Using Waffle flags to control your custom functionality at run time

### Module VI: System management

- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) Leveraging the app logs
- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) Automatically initializing your Django models at app install/startup
- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) Passing secrets/passwords to your plugin
- (instructor: [Lawrence McDaniel](https://github.com/lpm0073)) Verifying that your plugins are installed and running, and are correctly configured

### Module VII: Taking code quality to the next level

- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) add pre-commit with black and flake8
- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) unit tests
- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) implementing semantic versioning, in Pythin, github, pip, and PyPi
- (instructor: [Volunteer to instruct this lesson](./CONTRIBUTORS.md)) publishing your Open edX plugin to PyPi
