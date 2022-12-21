# Custom API built from misc snippets from the Open edX built-in APIs

Note the following features:

- custom middleware module to redirect LMS urls to this alternative endpoints implemented in this plugin
- Django signal module to extend the functionality of the COURSE_GRADE_NOW_PASSED event
- custom Oauth2 backend implementation
- custom Django models
- Django admin section
- Django manage.py custom commands
- unit tests

## Sample URLs

- http://yourdomain.edu/plugin/api/meta
- http://yourdomain.edu/plugin/api/users
- http://yourdomain.edu/plugin/api/token
- http://yourdomain.edu/plugin/api/api_fragment_view
