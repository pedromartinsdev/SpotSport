from dateutil.parser import parse
from flask import Flask, render_template, request, redirect, flash, url_for, session
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from werkzeug.debug import DebuggedApplication
from werkzeug.security import check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required


app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.init_app(app)
app.secret_key = "minha_chave_secreta"

engine = create_engine('sqlite:///database.db')
Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    username = Column(String(80), unique=True)
    password = Column(String(80))
    email = Column(String(200))
    address = Column(String(200))
    country = Column(String(50))
    birth_date = Column(Date)
    gender = Column(String(10))
    phone_number = Column(String(20))
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
    country = Column(String)
    date = Column(Date)
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
        if user and user.password == password:
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
    session.clear()
    session.close()
    logout_user()
    session.pop('usuario', None)
    print(session)
    return redirect('/login')


@app.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    if request.method == 'POST':
        email = request.form['email']
        return render_template('password-apologize.html', email=email)
    return render_template('password.html')


@app.route('/home')
@login_required
def home():
    username = current_user.username
    user_id = current_user.id
    myEvents = session.query(Event).filter_by(creator_id=user_id)
    subscribeEvents = session.query(Record).filter_by(user_id=user_id)

    return render_template('home.html', myEvents=myEvents, subscribeEvents=subscribeEvents, username=username)

@app.route('/records', methods=['GET', 'POST'])
@login_required
def records():
    username = current_user.username
    user_id = current_user.id
    if request.method == 'POST':
        eventId = request.form['id']
        record = Record(user_id=user_id, event_id=eventId)
        session.add(record)
        session.commit()
        session.close()

        return render_template('records.html', records=records, username=username)
    else:
        records = session.query(Record).all()
        return render_template('records.html', records=records, username=username)

@app.route('/')
def index():
    if current_user.is_authenticated:
        username = current_user.username
        events = session.query(Event).all()
        return render_template('home.html', events=events, username=username)
    else:
        print("Não logado")
        return render_template('login.html')


@app.route('/event-list', methods=['GET', 'POST'])
@login_required
def event_list():
    username = current_user.username
    if request.method == 'POST':
        city = request.form['city']
        events = session.query(Event).filter_by(location=city)
        return render_template('event-list.html', events=events, username=username)
    else:
        events = session.query(Event).all()
    return render_template('event-list.html', events=events, username=username)


@app.route('/user-list', methods=['GET', 'POST'])
@login_required
def user_list():
    username = current_user.username
    if request.method == 'POST':
        usernameSearch = request.form['username']
        users = session.query(User).filter_by(username=usernameSearch)
        return render_template('user-list.html', users=users, username=username)
    else:
        users = session.query(User).all()
    return render_template('user-list.html', users=users, username=username)


@app.route('/users', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        country = request.form['country']
        birth_date_str = request.form['birth_date']
        birth_date = parse(birth_date_str).date()
        gender = request.form['gender']
        user_verify = False
        phone_number = request.form['phone_number']

        user = User(name=name, username=username, address=address, country=country,
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
    username = current_user.username
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        country = request.form['country']
        date_str = request.form['date']
        creator_id = current_user.id

        date = parse(date_str).date()

        event = Event(title=title, description=description, location=location,
                      country=country, date=date, creator_id=creator_id)

        session.add(event)
        session.commit()

        return redirect('event-list')

    events = session.query(Event).all()
    session.close()
    return render_template('events.html', events=events, username=username)


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000, debug=True, use_reloader=True)
