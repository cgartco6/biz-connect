from app import app, db
from app.models import User, Business

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Business': Business}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
