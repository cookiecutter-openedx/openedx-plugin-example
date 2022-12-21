# example Open edX Plugin

[![hack.d Lawrence McDaniel](https://img.shields.io/badge/hack.d-Lawrence%20McDaniel-orange.svg)](https://lawrencemcdaniel.com)

A curated collection of code examples for extending the functionality of an Open edX installation using its built-in plugin architecture. Contains the following code examples:

* Extending Course Management Studio functionality with this [custom report](openedx_plugin_cms/README.md). Demonstrates the correct practices for adding custom url endpoints to Studio, advances usage of Mako templating within a plugin, and how to programatically iterate and introspect course content. Also includes a custom Django model, and caching.
* Extending [new user registration](./openedx_plugin/student/registration.py) functionality. Demonstrates how to leverage Django Signals to extend basic native Open edX operations.
* Extending the [login functionality](./openedx_plugin/student/session.py)
* Implementing a [custom api](./openedx_plugin_api/README.md) built from snippets of Open edX's built-in rest api libraries. 
* Implementing a [rest api](./openedx_plugin/api/README.md) from scratch that is accessible from an LMS url.
* Advanced Internationalization: [customizing static page links](./openedx_plugin/locale/README.md) based on the language locale setting
* Create a custom third party auth [Oauth2 provider](./openedx_plugin_api/custom_oauth2_backend.py).

Technical features that are showcased in this repo include:

* semantic version control
* pip configuration, requirements, constraints, setup.py, pyproject.toml
* How to house multiple plugins in a single pip package
* How to override default Open edX urls in lms and cms
* How to add tests to plugin code
* Django app setup
* Open edX Django configuration settings
* Open edX Django urls
* Open edX Django logging
* Open edX Django signals
* Open edX Django RestFramework custom api
* Django models
* Django templating
* Django static assets
* Django Admin
* Django middleware
* Django manage.py custom commands
* Python environment variables


## Getting Started

### Install using Tutor

See [Installing extra xblocks and requirements](https://docs.tutor.overhang.io/configuration.html)

```bash
tutor config save       # to ensure that tutor's root folder system has been created
echo "git+https://github.com/lpm0073/openedx-plugin-example.git" >> "$(tutor config printroot)/env/build/openedx/requirements/private.txt"
cat "$(tutor config printroot)/env/build/openedx/requirements/private.txt"
tutor images build openedx
tutor local quickstart

# you'll also need to run this on your very first install
# -----------------------------------------------------------------------------

# 1. run migrations
tutor local run lms ./manage.py lms makemigrations
tutor local run lms ./manage.py lms migrate
tutor local run cms ./manage.py cms makemigrations
tutor local run cms ./manage.py cms migrate

# 2. add configuration data to custom models
tutor local run lms ./manage.py lms create_oauth_application_client_config
tutor local run lms ./manage.py lms initialize
```



### Local development

* Use the same virtual environment that you use for edx-platform
* Set your Python interpreter to 3.8x
* install black: https://pypi.org/project/black/
* install flake8: https://flake8.pycqa.org/en/latest/

```bash
# Run these from within your edx-platform virtual environment
python3 -m venv venv
source venv/bin/activate

cd /path/to/edx-platform
pip install -r requirements/edx/base.txt
pip install -r requirements/edx/coverage.txt
pip install -r requirements/edx/development.txt
pip install -r requirements/edx/pip-tools.txt
pip install -r requirements/edx/testing.txt
pip install -r requirements/edx/doc.txt
pip install -r requirements/edx/paver.txt

pip install pre-commit black flake8
pre-commit install
```

### Local development good practices

* run `black` on modified code before committing.
* run `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
* run `flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics`
* run `pre-commit run --all-files` before pushing. see: https://pre-commit.com/

#### edx-platform dependencies

To avoid freaky version conflicts in prod it's a good idea to install all of the edx-platform requirements to your local dev virtual environment.

* requirements/edx/base.txt
* requirements/edx/develop.txt,
* requirements/edx/testing.txt

At a minimum this will give you the full benefit of your IDE's linter.

#### Notes regarding development with macOS M1

1. To avoid problems with installing the edx-platform requirements, create your virtual environment with Python >= 3.9.x using the native installer from https://www.python.org/. `which python` should return `/Library/Frameworks/Python.framework/Versions/3.9/bin/python3`. Ignoring this advise will lead to very weird side effects. Note that this is true even though Lilac actually runs on Python 3.8.x

2. Best to install openssl, openblas, zstd, mysql, and mysql-client with Brew. Using brew helps you avoid problems with gcc compilations and linking that have proven problematic on early releases of macOS 11 on M1. If you run into problems while pip installing mysql-client / MongoDBProxy / mongoengine/ pymongo /numpy / scipy / matplotlib then analyze the stack trace for any other straggling dependencies that I might have ommitted here that might also break due to the gcc compiler or linker, and try installing these instead with Brew.

3. In addition to launching your virtual environment it also helps to set the following environment variables in your terminal window. Make sure you pay attention to any further suggestions echoed in Brew installation output:

```bash
export OPENBLAS=/opt/homebrew/opt/openblas/lib/
export LDFLAGS="-L/opt/homebrew/opt/openblas/lib -L/opt/homebrew/opt/mysql-client/lib"
export CPPFLAGS="-I/opt/homebrew/opt/openblas/include -I/opt/homebrew/opt/mysql-client/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/openblas/lib/pkgconfig /opt/homebrew/opt/mysql-client/lib/pkgconfig"
```


### Shell Plus and iPython

The example_edxapi module adds ipython and django-extensions to the stack.  It is then possible to get an enhanced shell via:

```bash
tutor local exec lms ./manage.py lms shell_plus
```
