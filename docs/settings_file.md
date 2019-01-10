# The Settings File (settings.cfg)

## File Format and Required Fields
Following details are for the settings file that the flask application reads configurations from on startup. It is the main file where things like DB passwords and API keys are stored. In production you will need to pay special attention to the permissions on the file as it will hold sensitive information. Recommended setup is to have the `settings.cfg` file owned by root and allow read only access to the flask applications user group.

### Development
For development servers you will want to create a directory named `configs/` in the root of the project directory. In the config directory create a file named `settings.dev.cfg` with the following content.

```python
# General Settings
SECRET_KEY = '<flask_secret_here>'
PREFERRED_URL_SCHEME = 'http'

# Azure AD Settings
AZURE_TENANT_ID = '<tenant_id_here>'
AZURE_CLIENT_ID = '<client_id_here>'
AZURE_CLIENT_SECRET = '<client_secret_here>'
```

### Production
In production create the `settings.cfg` in the `/etc/flask-starter/` directory with the values below. If this directory does not exist you will need to create it.

```python
# General Settings
SERVER_NAME = ''
SESSION_COOKIE_NAME = 'flask-starter'
SESSION_COOKIE_DOMAIN = ''
SECRET_KEY = '<flask_secret_here>'

# Azure AD Settings
AZURE_TENANT_ID = '<tenant_id_here>'
AZURE_CLIENT_ID = '<client_id_here>'
AZURE_CLIENT_SECRET = '<client_secret_here>'

# Database Settings
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>'
```