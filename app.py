from dateutil.parser import parse
from flask import Flask, render_template, request, redirect, flash, url_for, session
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Float, Text, ForeignKey, func, or_, not_
from sqlalchemy.orm import sessionmaker, relationship, join, joinedload
from sqlalchemy.orm import declarative_base
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import json

app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.init_app(app)
app.secret_key = "minha_chave_secreta"
Base = declarative_base()

""" modelo das tabelas users, events, records e countries """
class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstName = Column(String(80))
    lastName = Column(String(80))
    photo = Column(String)
    email = Column(String(200))
    phone_number = Column(String(20))
    username = Column(String(80), unique=True)
    password = Column(String(80))
    birth_date = Column(Date)
    gender = Column(String(10))
    user_verify = Column(Boolean, default=False)
    country_id = Column(Integer, ForeignKey('countries.id'))
    country = relationship("Country", backref="users")

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    location = Column(String)
    date = Column(Date)
    time = Column(String)
    cost = Column(Float)
    creator_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="events")

class Record(Base):
    __tablename__ = 'records'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="records")
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship("Event", backref="records")

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    country_name_int = Column(String)


""" Cria as tabelas do banco no modelo acima e inicia a session """
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

""" Quando o banco nao tiver nenhum pais popula com os países do countries.json """
def populate_countries():
    row = session.query(Country).all()

    if (len(row) == 0):
        file_path = 'countries.json'

        with open(file_path, 'r') as file:
            json_content = json.load(file)

        for item in json_content:
            country_name_int = item['country_name_int']
            country = Country(country_name_int=country_name_int)
            session.add(country)  
        session.commit()

populate_countries()

""" Trata o codigo para evitar multi thread """
@app.after_request
def after_request(response):
    session.close()
    return response

""" retorna o usuário que esta logado """
@login_manager.user_loader
def load_user(user_id):
    return session.query(User).filter_by(id=user_id).first()

""" Rotas da aplicacao """
@app.route('/landing-page')
def landing_page():
    return render_template('landing-page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = session.query(User).filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        email = request.form['email']
        return render_template('password-apologize.html', email=email)
    return render_template('password.html')

@app.route('/home')
@login_required
def home():
    user_id = current_user.id
    myEvents = session.query(Event).filter_by(creator_id=user_id)
    subscribeEvents = session.query(Record).filter_by(user_id=user_id)
    
    return render_template('home.html', myEvents=myEvents, subscribeEvents=subscribeEvents, user=current_user)

@app.route('/records', methods=['GET', 'POST'])
@login_required
def records():
    user_id = current_user.id
    if request.method == 'POST':
        eventId = request.form['id']
        record = Record(user_id=user_id, event_id=eventId)

        row = session.query(Record).filter_by(
            user_id=user_id, event_id=eventId).all()

        if (len(row) != 0):
            events = session.query(Event).all()

            return render_template('event-list.html', events=events, user=current_user)

        session.add(record)
        session.commit()
        records = session.query(Record).filter_by(user_id=user_id).all()
        return render_template('records.html', records=records, user=current_user)
    else:
        records = session.query(Record).filter_by(user_id=user_id).all()
        return render_template('records.html', records=records, user=current_user)

@app.route('/')
def index():
    if current_user.is_authenticated:
        user_id = current_user.id
        myEvents = session.query(Event).filter_by(creator_id=user_id)
        subscribeEvents = session.query(Record).filter_by(user_id=user_id)
        return render_template('home.html', myEvents=myEvents, subscribeEvents=subscribeEvents, user=current_user)
    else:
        return render_template('landing-page.html')

@app.route('/event-list', methods=['GET', 'POST'])
@login_required
def event_list():
    if request.method == 'POST':
        name = request.form['name']
        events = session.query(Event).filter_by(title=name.lower()).all()
        return render_template('event-list.html', events=events, user=current_user)
    else:
        events = session.query(Event).all()
    
    return render_template('event-list.html', events=events, user=current_user)

@app.route('/user-list', methods=['GET', 'POST'])
@login_required
def user_list():
    user_id = current_user.id
    if request.method == 'POST':
        username = request.form['username']
        users = session.query(User).filter_by(username=username)
        return render_template('user-list.html', users=users, user=current_user)
    else:
        users = session.query(User).options(joinedload(User.country)).all()
        for user in users:
            if user.id == user_id:
                index = users.index(user)
                del users[index]
    
    return render_template('user-list.html', users=users, user=current_user)

@app.route('/create-user', methods=['GET', 'POST'])
def createUser():
    countries = session.query(Country).order_by(Country.country_name_int.asc()).all()
    if request.method == 'POST':
        firstName = request.form['first-name']
        lastName = request.form['last-name']
        photo = request.form['photo']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirm-password']
        country = request.form['country']
        birth_date_str = request.form['birth_date']
        birth_date = parse(birth_date_str).date()
        gender = request.form['gender']
        user_verify = False
        phone_number = request.form['phone_number']
        
        row = session.query(
            User).filter(or_(User.username==username, User.email==email)).all()

        if (len(row) != 0):
            flash("Sentimos muito, mas esse nome de usuário/e-mail já existe!")
            return redirect('/create-user')
   
        if not photo:
            photo = "assets/user-default-profile.png"

        if confirmPassword == password:
            newHash = generate_password_hash(request.form['password'])
            newUser = User(firstName=firstName, lastName=lastName, username=username, photo=photo, country_id=country,
                    birth_date=birth_date, gender=gender, user_verify=user_verify, phone_number=phone_number, email=email, password=newHash)
        else:
            flash("As senhas não são iguais")
            return redirect('/create-user')
        session.add(newUser)
        session.commit()
        return redirect('/login')
    
    return render_template('create-user.html', countries=countries)

@app.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        cost = request.form['cost']
        date_str = request.form['date']
        time = request.form['time']
        creator_id = current_user.id

        date = parse(date_str).date()

        event = Event(title=title.lower(), description=description, location=location,
                      time=time, date=date, creator_id=creator_id, cost=cost)

        session.add(event)
        session.commit()
        return redirect('event-list')

    events = session.query(Event).all()
    
    return render_template('events.html', events=events, user=current_user)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        photo = request.form['photo']
        password = request.form['password']
        confirmPassword = request.form['confirm-password']
        if photo:
            user = session.query(User).filter_by(id=current_user.id).first()
            user.photo = photo
            session.commit()
            flash("Foto alterada!")
        if password or confirmPassword:
            if password == confirmPassword:
                user = session.query(User).filter_by(id=current_user.id).first()
                user.password = generate_password_hash(password)
                session.commit()
                flash("Senha alterada!")
                return render_template('settings.html', user=current_user)
            else:
                flash("Senhas diferentes!")
                return render_template('settings.html', user=current_user)
        else:
            return render_template('settings.html', user=current_user)
    else:
        return render_template('settings.html', user=current_user)

if __name__ == '__main__':
    app.run()
