from __init__ import create_app
import os

app = create_app(config_name=os.getenv('FLASK_CONFIG', 'ProductionConfig'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
