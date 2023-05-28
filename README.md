# SPOTSPORT 🏅

1. [Description](#description) &nbsp;
2. [Routes](#routes) </br>
  2.1. [/index](#index) </br>
  2.2. [/landing-page](#landing-page) </br>
  2.3. [/create-user](#create-user) </br>
  2.4. [/passworod](#password) </br>
  2.5. [/login](#login) </br>
  2.6. [/create-event](#create-event) </br>
  2.7. [/event-list](#event-list) </br>
  2.8. [/user-list](#user-list) </br>
  2.9. [/settings](#settings) </br>
  2.10. [/records](#records) </br>
3. [Functions](#functions)
4. [Video Demo](#video-demo)
5. [Technologies Used](#technologies-used)
6. [Credits](#credits)

## Description

### **(EN)**

This code was created for the final project of the CS50 course at Harvard University, aiming to demonstrate the skills developed throughout the course.

SpotSport's main idea is to centralize and promote events that encourage people to become more active and happy, whether it's a simple picnic or a marathon in the city.

In SpotSport, users can find events that best suit their lifestyle.

### **(PT-BR)**

Esse código foi criado para o projeto final do curso CS50 da Universidade de Harvard, com o objetivo de demonstrar as habilidades desenvolvidas no processo.

O SpotSport tem como ideia principal centralizar e divulgar eventos que incentivem as pessoas a se tornarem mais ativas e felizes, seja através de um simples pique-nique à uma maratona na cidade.

No SpotSport, os usuários podem encontrar eventos que se encaixem melhor em seu estilo de vida.

## Routes

### Index

The `/` route checks if a user is logged in. If there is a logged-in user, it redirects to the `/home` route. If there is no logged-in user, it renders the `/landing-page`.

### /landing-page

This route renders a landing page promoting the app.
![landing-page](/assets/landing-page.gif)

### /create-user

This route renders a register page.
![crete-user](/assets/create-user.gif)

In this route, the user fills in their information for registration.
It's important to note that all fields are mandatory, except for the photo link.

Before allowing a new user to be created, a database query is performed to check if the ```username``` and ```email``` are already in use.

### /password

This route renders a "Forgot Password" page that prompts the user to enter their email address to receive a password reset link.
And then render the page password-apologize.html.

![password](/assets/password.gif)

### /login

This route renders a login page where the user must enter their email and password, or click on the "Forgot Password" and "Create Account" links. f the email and password are correct, it will render the app's ```/home``` page. If they are incorrect, a flash message will appear with the text "Invalid email or password."

![login](/assets/login.gif)

### /home

The `/home` route renders a page that displays all the events you are subscribed to and all the events you have created.

- This route uses the `layout.html` template for the header, navigation (nav), and footer.
- This route requires login (`@login_required`) to access.

![home](/assets/home.png)

### /create-event

This route allows for creating an event and is triggered by the "New Event" button on the Events page.

All fields are required to be filled in, including event `title`, `description`, `cost`, `location`, `date` and `time`.

- This route uses the `layout.html` template for the header, navigation (nav), and footer.
- This route requires login (`@login_required`) to access.

![create-event](/assets/create-event.gif)

### /event-list

This route is responsible for listing all the events that have been created, allowing users to sign up for them. It also includes a search bar that allows users to search for events by name. Additionally, there is a "Create New Event" button that redirects users to the `/events` route.

- This route uses the `layout.html` template for the header, navigation (nav), and footer.
- This route requires login (`@login_required`) to access.

![event-list](/assets/event-list.png)

### /user-list

This route lists all the registered users on SpotSport, excluding the user who is performing the search.

- This route uses the `layout.html` template for the header, navigation (nav), and footer.
- This route requires login (`@login_required`) to access.

![user-list](/assets/user-list.png)

### /settings

This route allows users to change their profile picture and password.

- This route uses the `layout.html` template for the header, navigation (nav), and footer.
- This route requires login (`@login_required`) to access.
- The photo field accepts only a URL for the image.

![settings](/assets/settings.gif)

### /records

This route displays the events in which the user is the creator as well as the events they have signed up for.
The POST request for this route is triggered when the user clicks on "Sign Up" on the events page.

- This route uses the `layout.html` template for the header, navigation (nav), and footer.
- This route requires login (`@login_required`) to access.

![records](/assets/records.png)

## Functions

### Populate countries table

Since it is common in the development environment to delete the database.db file to modify the database, I have decided to insert a countries.json file in the project's root directory. Every time the app starts and there is no data in the countries table, this function will read the .json file and input the data into the database.db.

~~~python
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
~~~

### After request

To avoid issues with threading, it was necessary to use "after_request" to close the sessions.

~~~python
@app.after_request
def after_request(response):
    session.close()
    return response
~~~

### Load user

This function returns the logged-in user so that the data can be reused to populate the application's header.

~~~python
@login_manager.user_loader
def load_user(user_id):
    return session.query(User).filter_by(id=user_id).first()
~~~

## Video-Demo

[Portuguese](https://www.youtube.com/watch?v=rN3hN8QG9Wk)

[English](https://www.youtube.com/watch?v=DF9Nk4Wzqh0) - Translated with the Captions app AI.

## Installation

1 - Download or clone the repository to your machine.

2 - Run the command `pip install -r requirements.txt`

3 - Once all the dependancies have been installed, run the command `python app.py`

4 - Now simply access the localhost on the port indicated in the prompt, and the app will open.

## Technologies-used

- Python
- Flask
- HTML
- CSS
- JavaScript

## Credits

- User icon - [Undraw.co](https://undraw.co/)
- User photos - [This-Person-Does-not-Exist.com](https://this-person-does-not-exist.com/)
- Country list - [Github - jonasruth](https://gist.github.com/jonasruth/61bde1fcf0893bd35eea)
