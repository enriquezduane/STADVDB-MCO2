# app/run.py
from app import create_app

app = create_app()

# 0.0.0.0 so that it can communicate with the other containers

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
