from dateutil.parser import parse
from flask import Flask, render_template, request, redirect, flash, url_for, session
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey, func, or_
from sqlalchemy.orm import sessionmaker, relationship, join
from sqlalchemy.orm import declarative_base
from werkzeug.debug import DebuggedApplication
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import json

app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.init_app(app)
app.secret_key = "minha_chave_secreta"

engine = create_engine('sqlite:///database.db')
Base = declarative_base()


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
    country = Column(String(50))
    birth_date = Column(Date)
    gender = Column(String(10))
    user_verify = Column(Boolean, default=False)

    def get_id(self):
        return str(self.id)

    def get_email(self):
        return str(self.email)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    location = Column(String)
    date = Column(Date)
    time = Column(String)
    creator_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="events")


class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="records")
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship("Event", backref="records")


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).filter_by(id=user_id).first()


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
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        else:
            print("Senha inválida")
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
        session.close()
        records = session.query(Record).filter_by(user_id=user_id)
        return render_template('records.html', records=records, user=current_user)
    else:
        records = session.query(Record).filter_by(user_id=user_id)
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
        city = request.form['city']
        events = session.query(Event).filter_by(location=city)
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
        users = session.query(User).all()
        for user in users:
            if user.id == user_id:
                index = users.index(user)
                del users[index]
    return render_template('user-list.html', users=users, user=current_user)


@app.route('/users', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        firstName = request.form['first-name']
        lastName = request.form['last-name']
        photo =request.form['photo']
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        country = request.form['country']
        birth_date_str = request.form['birth_date']
        birth_date = parse(birth_date_str).date()
        gender = request.form['gender']
        user_verify = False
        phone_number = request.form['phone_number']

        user = User(firstName=firstName, lastName=lastName, username=username, photo=photo, country=country,
                    birth_date=birth_date, gender=gender, user_verify=user_verify, phone_number=phone_number, email=email, password=password)

        session = Session()
        session.add(user)
        session.commit()
        session.close()
        return redirect('/login')
    return render_template('users.html')


@app.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        date_str = request.form['date']
        time = request.form['time']
        creator_id = current_user.id

        date = parse(date_str).date()

        event = Event(title=title, description=description, location=location,
                      time=time, date=date, creator_id=creator_id)

        session.add(event)
        session.commit()

        return redirect('event-list')

    events = session.query(Event).all()
    session.close()
    return render_template('events.html', events=events, user=current_user)


@app.route('/configure', methods=['GET', 'POST'])
@login_required
def configure():
    if request.method == 'POST':
        print("daqui a pocuo eu termino")
    else:
        return render_template('configure.html', user=current_user)


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000, debug=True, use_reloader=True)
