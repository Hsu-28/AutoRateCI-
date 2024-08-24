import os

# 創建必要的資料夾結構
folders = ['app', 'app/templates', 'app/static', 'migrations', 'tests']
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# 創建必要的文件
files = {
    'app/__init__.py': '''from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    with app.app_context():
        from . import routes

    return app
''',
    'app/routes.py': '''from flask import render_template
from . import create_app

app = create_app()

@app.route('/')
def index():
    return "Hello, World!"
''',
    'app/models.py': '',
    'app/config.py': '''# Flask Configuration
DEBUG = True
SECRET_KEY = 'your_secret_key'
''',
    'tests/__init__.py': '',
    'tests/test_routes.py': '''import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_index(client):
    rv = client.get('/')
    assert b'Hello, World!' in rv.data
''',
    'run.py': '''from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
''',
    'requirements.txt': '''Flask==2.1.0
pytest
'''
}

# 創建文件並寫入內容
for file, content in files.items():
    with open(file, 'w') as f:
        f.write(content)
