from har import db


class Subject(db.Model):
    device = db.Column(db.String(40), primary_key=True)
    token = db.Column(db.String(60), unique=True)
    user_gender = db.Column(db.String(1))
    user_age = db.Column(db.Integer)
    accelerometer = db.Column(db.Boolean)
    ambient_temperature = db.Column(db.Boolean)
    gravity = db.Column(db.Boolean)
    gyroscope = db.Column(db.Boolean)
    light = db.Column(db.Boolean)
    linear_accelerometer = db.Column(db.Boolean)
    magnetic_field = db.Column(db.Boolean)
    orientation = db.Column(db.Boolean)
    pressure = db.Column(db.Boolean)
    proximity = db.Column(db.Boolean)
    relative_humidity = db.Column(db.Boolean)
    rotation_vector = db.Column(db.Boolean)
    temperature = db.Column(db.Boolean)
    logs = db.relationship('Log', backref='subject')

    def __init__(self, device, token, user_gender, user_age, sensors):
        self.device = device
        self.token = token
        self.user_gender = user_gender
        self.user_age = user_age
        self.accelerometer = sensors.get('accelerometer', False)
        self.ambient_temperature = sensors.get('ambient_temperature', False)
        self.gravity = sensors.get('gravity', False)
        self.gyroscope = sensors.get('gyroscope', False)
        self.light = sensors.get('light', False)
        self.linear_accelerometer = sensors.get('linear_accelerometer', False)
        self.magnetic_field = sensors.get('magnetic_field', False)
        self.orientation = sensors.get('orientation', False)
        self.pressure = sensors.get('pressure', False)
        self.proximity = sensors.get('proximity', False)
        self.relative_humidity = sensors.get('relative_humidity', False)
        self.rotation_vector = sensors.get('rotation_vector', False)
        self.temperature = sensors.get('temperature', False)

    def __repr__(self):
        return '<Device %s>' % self.device
