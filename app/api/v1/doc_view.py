from flask import render_template, url_for, current_app
from . import api_v1


@api_v1.documentation
def custom_ui():
    http_scheme = current_app.config['PREFERRED_URL_SCHEME'] \
        if current_app.config.get('PREFERRED_URL_SCHEME') else 'http'
    specs_url = url_for(api_v1.endpoint('specs'), _external=True, _scheme=http_scheme)
    return render_template('api/v1/docs.html', title=api_v1.title, specs_url=specs_url)
