from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#tabla de nuestra BBDD
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #Nuestro atributo 'posts' tiene relacion con nuestro modelo Post, backref es como si fuera otra columna de la clase Post. 
    #posts es una query adicional, no es una columna
    #en el db.relationship va Post en MAYUSCULAS, ya que hace referencia a la clase Post
    posts = db.relationship('Post', backref='author', lazy=True)
    
    #metodo para resetear email y password
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        
        return User.query.get(user_id)
    
    #Como se printea el objeto que se esta instanciando en el momento
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #el foreign key especifica que nuestro user_id tiene relacion con la clase User
    #en el db.ForeignKey va user en MINUSCULAS, ya que hace referencia a una columna en especial, de la clase (tabla) User.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    #Como se printea el objeto que se esta instanciando en el momento
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
    