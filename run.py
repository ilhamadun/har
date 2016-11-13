from har import app


# Load configurations
app.config.from_object('config')
app.config.from_pyfile('config.py')

# Run app
app.run(host=app.config['HOST'])
