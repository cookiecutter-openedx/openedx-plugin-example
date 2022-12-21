# Custom Course Content Audit Report for Course Management Studio

[![hack.d Lawrence McDaniel](https://img.shields.io/badge/hack.d-Lawrence%20McDaniel-orange.svg)](https://lawrencemcdaniel.com)

A change log for Course Content. Triggered by Django signals tied to Course content management when publishing, editing and deleting course content from Course Management Studio. write change data into its own Django model. Provides a simple columnar view that is accessible in Course Management Studio via the urls below.

## First Time Installation

```bash
sudo -H -u edxapp bash
cd ~
source edxapp_env
source venvs/edxapp/bin/activate
cd edx-platform
pip install -e /the/file/path/to/openedx-plugin-example
./manage.py cms makemigrations openedx_plugin_cms
./manage.py cms migrate
```

## Features

### Audit Samples URLs

- https://studio.yourdomain.edu/plugin/cms/courses/course-v1:edX+DemoX+Demo_Course/audit/
- https://studio.yourdomain.edu/plugin/cms/courses/course-v1:edX+DemoX+Demo_Course/audit/csv/

### Change Log Sample URLs

- https://studio.yourdomain.edu/plugin/cms/log
- https://studio.yourdomain.edu/plugin/cms/log/csv/
- https://studio.yourdomain.edu/plugin/cms/courses/course-v1:edX+DemoX+Demo_Course/log/
- https://studio.yourdomain.edu/plugin/cms/courses/course-v1:edX+DemoX+Demo_Course/log/csv/

- https://studio.test.global-communications-academy.com/plugin/cms/log/
- https://studio.test.global-communications-academy.com/plugin/cms/log/csv/
- https://studio.test.global-communications-academy.com/plugin/cms/courses/course-v1:plugin/cms+DCa+00005/log/
- https://studio.test.global-communications-academy.com/plugin/cms/courses/course-v1:plugin/cms+DCa+00005/log/csv/

### To run from manage.py

```bash
sudo -H -u edxapp bash
cd ~
source edxapp_env
source venvs/edxapp/bin/activate
cd edx-platform
./manage.py cms eval_course -c course-v1:edX+DemoX+Demo_Course
```
