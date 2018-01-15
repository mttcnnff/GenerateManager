from . import db
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x08

class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['MATTER_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role == None:
                self.role = Role.query.filter_by(default=True).first()


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], current_app.config['TOKEN_EXPIRATION'])
        return s.dumps({'confirm': self.id})

    def generate_password_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], current_app.config['TOKEN_EXPIRATION'])
        return s.dumps({'reset': self.id})

    def generate_email_reset_token(self, new_email):
        s = Serializer(current_app.config['SECRET_KEY'], current_app.config['TOKEN_EXPIRATION'])
        return s.dumps({'user_id': self.id, 'new_email': new_email})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'], current_app.config['TOKEN_EXPIRATION'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def change_username(self, new_username):
        if User.query.filter_by(username=new_username).first() is None:
            self.username = new_username
            db.session.add(self)
            return True
        else:
            return False

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'], current_app.config['TOKEN_EXPIRATION'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('user_id') != self.id:
            return False
        self.email = data.get('new_email')
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'], current_app.config['TOKEN_EXPIRATION'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.filter_by(id=data.get('reset')).first()
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    # id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(64), unique=True, index=True)
    # username = db.Column(db.String(64), unique=True, index=True)
    # password_hash = db.Column(db.String(128))
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # confirmed = db.Column(db.Boolean, default=False)

    @staticmethod
    def insert_users():
        users = {
            'Admin': {'username': 'Matt',
                      'email': 'mttcnnff@gmail.com',
                      'password': 'matt',
                      'confirmed': True,
                      'role': 'Administrator'},
            'Mod': {'username': 'John',
                      'email': 'john@example.com',
                      'password': 'john',
                      'confirmed': True,
                      'role': 'Moderator'},
            'User': {'username': 'Bob',
                    'email': 'bob@example.com',
                    'password': 'bob',
                    'confirmed': True,
                    'role': 'User'},
        }
        for u in users:
            params = users[u]
            user = User(username=params['username'],
                        email=params['email'],
                        password=params['password'],
                        confirmed=params['confirmed'],
                        role=Role.query.filter_by(name=params['role']).first())
            db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))