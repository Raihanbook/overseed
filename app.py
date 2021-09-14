import os
from overseed import create_app

app = create_app()

# We should not enable debug mode in production
debug_mode = False if os.environ.get('FLASK_ENV') == 'production' else True

if __name__ == '__main__':
    app.run(debug=debug_mode)
