from oauth2_wordpress.wp_oauth import WPOpenEdxOAuth2


class WPOAuth2(WPOpenEdxOAuth2):
    """
    A custom Open edX oauth2 backend.

    Requirements for use:
    1. oauth2_wordpress comes from PyPi package
       edx-oauth2-wordpress-backend (https://pypi.org/project/edx-oauth2-wordpress-backend/)
       You'll need to ensure is added to your requirements.txt.

    2. add this backend lms.env.yml

        THIRD_PARTY_AUTH_BACKENDS:
        - social_core.backends.google.GoogleOAuth2
        - social_core.backends.facebook.FacebookOAuth2
        - openedx_plugin.wordpress_oauth2_backend.WPOAuth2

    3. using LMS Django Admin, create a new oauth2 configuration. You *should* find
       this backend included in the backend dropdown of the Django Admin page, listed
       as "wordpress-oauth".

    """

    # This defines the backend name and identifies it during the auth process.
    # The name is used in the URLs /login/<backend name> and /complete/<backend name>.
    #
    # This is the string value that will appear in the LMS Django Admin
    # Third Party Authentication / Provider Configuration (OAuth)
    # setup page drop-down box titled, "Backend name:", just above
    # the "Client ID:" and "Client Secret:" fields.
    name = "wordpress-oauth"

    # setup oauth endpoints:
    # authorization:    https://your-wordpress-site.edu/oauth/authorize
    # token:            https://your-wordpress-site.edu/oauth/token
    # user info:        https://your-wordpress-site.edu/oauth/me
    BASE_URL = "https://your-wordpress-site.edu"
