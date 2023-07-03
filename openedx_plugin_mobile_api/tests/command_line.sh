# encoding: UTF-8
# See: https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html

BASE_DOMAIN="courses.yourdomain.edu"
AUTH_URL="https://${BASE_DOMAIN}/oauth2/access_token"
USER="admin"
PASSWORD="set-me-please"

# from 'Android Mobile App' https://stage.turnthebus.org/admin/oauth2_provider/application/4/change/
CLIENT_ID="set-me-please"
CLIENT_SECRET="set-me-please"
GRANT_TYPE="password"

# get a bearer token
curl -X POST -d "grant_type=${GRANT_TYPE}&username=${USER}&password=${PASSWORD}" -u"${CLIENT_ID}:${CLIENT_SECRET}" $AUTH_URL

# expected result:
# ------------------------------
# {"access_token": "some-token-value", "expires_in": 36000, "token_type": "Bearer", "scope": "read write USER_EMAIL profile", "refresh_token": "some-token-value"}

TOKEN="set-me-from-curl-results:access_token"

# ---------------------------------------------------------------------
# API TESTS
# these only work with YOUR username due to permissions classes that are
# added in edx-platform.
# ---------------------------------------------------------------------

REQUEST_PATH="/api/mobile/v0.5/users/${USER}"
REDIRECT_PATH="/turnthebus/api/mobile/v0.5/users/${USER}"

# user details. these should return the same results.
# user details for your username. otherwise returns, {"detail":"You do not have permission to perform this action."}
# both are valid results.
curl -L -H "Authorization: Bearer ${TOKEN}" https://${BASE_DOMAIN}${REQUEST_PATH}
curl -L -H "Authorization: Bearer ${TOKEN}" https://${BASE_DOMAIN}${REDIRECT_PATH}

# other endpoints that are implemented via the plugin but ultimately run the
# original code from edx-platform
curl -L -H "Authorization: Bearer ${TOKEN}" https://${BASE_DOMAIN}${REQUEST_PATH}/course_enrollments
curl -L -H "Authorization: Bearer ${TOKEN}" https://${BASE_DOMAIN}${REQUEST_PATH}/course_status_info
