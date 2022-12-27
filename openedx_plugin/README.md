# Example Plugin for Open edX

[![hack.d Lawrence McDaniel](https://img.shields.io/badge/hack.d-Lawrence%20McDaniel-orange.svg)](https://lawrencemcdaniel.com)

An example Open edX plugin.

-
-
-
-

## Features

### Waffle activated simple REST API with LMS url endpoint, Django model, and Django Admin

Assigns the example api server to use for the Open edX instance on which this plugin is installed.
The api endpoint is: https://lms.example.edu/plugin/api/v1/configuration

source code is located in openedx_plugin/api/

Uses this Django model: https://lms.example.edu/admin/openedx_plugin/configuration/


public url to the api: https://lms.example.edu/plugin/api/v1/configuration


### Waffle activated auto-enrollment URL endpoint with language code parameter

Provides a means to embed localization information about the user in, for example, CTA buttons that send the user from and external marketing site (like Wordpress) to Open edX. The most common url presently is: https://lms.example.edu/example/dashboard?language=es-419

source code is located in [./dashboard/](./dashboard/)

### Waffle activated language-aware marketing site static page urls

The reverse case. Provides a generalized way to seamlessly map the user from the LMS to the most sensible marketing site. An example usage is the "Discover New" link in the LMS site header. The url, assigned inside lms.yml within MKTG_URL_OVERRIDES is, https://lms.example.edu/example/marketing-redirector/?example_page=learning-content/ and will redirect to https://example.org/learning-content/ for a US-based user. Uses the MarketingSites model found in [models.py](./models.py)


### Localized html anchor tags

Same as above, but for html anchor tags. In addition to the URL mapping, these also require language translation of the text of the html element value, bearing in mind that we need to avoid changes to the edx-platform po files since we do not want to fork the edx-platform repo. Uses the Locale in [./dashboard/](./dashboard/)

An example usage would be the "Blog" and "Privacy Policy" links in the LMS site footer. The following is added to the Mako template:

```python
<%!
  from openedx_plugin.locale.utils import anchor, language_from_request
%>

<%

  # figure out the best language code to use based on whatever we
  # know about this user.
  try:
    preferred_language = language_from_request(request) or 'en'
  except:
    preferred_language = 'en'

  # get a Python dict containing the url and element text.
  blog_dict = anchor('example-locale-blog', preferred_language)
%>

```

and the link itself would take the form

```html
    <a id="example-locale-blog" href="${blog_dict.get('url')}">${blog_dict.get('value')}</a>
```

### Waffle activated receivers hooks

Adds listeners (aka Receivers, aka Django Signals) for events defined in Open edX for common operations like new student registration, enrollments, grade changes, course completed, etcetera.

## Language Notes

### UserProfile.language

Language is deprecated and no longer used. Old rows exist that have
user-entered free form text values (ex. "English"), some of which have
non-ASCII values. You probably want UserPreference version of this, which
stores the user's preferred language code.


### openedx/core/djangoapps/lang_pref

Implements an app api to poll information about which languages are released
on this platform. Of particular interest: get_closest_released_language(target_language_code)

## Example REST API

Scaffolded with Django REST Framework Cookie Cutter.

* admin.py: To register models with [Django Admin Console app](https://docs.djangoproject.com/en/2.1/ref/contrib/admin/).
* models.py: All are Generic [Django Models](https://docs.djangoproject.com/en/2.1/topics/db/models/). Nothing noteworthy about any of these.
* Configuration
* serializers.py: Subclasses from [Django REST Framework Serializers](https://www.django-rest-framework.org/api-guide/serializers/) to serialize Django ORM model data into JSON representations.
* urls.py: [rest_framework router](https://www.django-rest-framework.org/api-guide/routers/) configuration for the REST api end points as well as introspection-based documentation
* views.py: implemented using [rest_framework ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/). This is the simplest possible implementation, offering fully-functional list and detail views with default behavior.
