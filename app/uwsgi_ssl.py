import os

from app import create_app

base_dir = os.path.abspath(os.path.dirname(__file__))

key = os.path.join(base_dir, 'metadata', 'iam-dev.key')
cert = os.path.join(base_dir, 'metadata', 'iam-dev.crt')

app = create_app()


if __name__ == "__main__":
    context = (cert, key)
    app.run(host='0.0.0.0', port=8000, ssl_context=context)
