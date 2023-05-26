# SPOTSPORT 🏅

1. [Description](#description) &nbsp;
2. [Routes](#routes) </br>
2.1. [/](#index (/)) </br>
2.2. [/landing-page](#landing-page) </br>
2.3. [/create-user](#create-user) </br>
2.4. [/passworod](#password) </br>
2.5. [/login](#login) </br>
2.6. [/create-event](#create-event) </br>
2.7. [/user-list](#user-list) </br>
2.8. [/event-list](#event-list) </br>
2.9. [/settings](#settings) </br>
2.10. [/records](#records) </br>

#### Description:

###### **(EN)**

This code was created for the final project of the CS50 course at Harvard University, aiming to demonstrate the skills developed throughout the course.

SpotSport's main idea is to centralize and promote events that encourage people to become more active and happy, whether it's a simple picnic or a marathon in the city.

In SpotSport, users can find events that best suit their lifestyle.

###### **(PT-BR)**

Esse código foi criado para o projeto final do curso CS50 da Universidade de Harvard, com o objetivo de demonstrar as habilidades desenvolvidas no processo.

O SpotSport tem como ideia principal centralizar e divulgar eventos que incentivem as pessoas a se tornarem mais ativas e felizes, seja através de um simples pique-nique à uma maratona na cidade.

No SpotSport, os usuários podem encontrar eventos que se encaixem melhor em seu estilo de vida.

# Routes

## Index (/)

The `/` route checks if a user is logged in. If there is a logged-in user, it redirects to the `/home` route. If there is no logged-in user, it renders the `/landing-page`.

## /landing-page

This route renders a landing page promoting the app.
![landing page imagem](/assets/landing-page.gif)

## /create-user

This route renders a register page.
![landing page imagem](/assets/create-user.gif)

In this route, the user fills in their information for registration.
It's important to note that all fields are mandatory, except for the photo link.

Before allowing a new user to be created, a database query is performed to check if the ```username``` and ```email``` are already in use.

## /password

This route renders a "Forgot Password" page that prompts the user to enter their email address to receive a password reset link.

![landing page imagem](/assets/create-user.gif)

## /login

This route renders a login page where the user must enter their email and password, or click on the "Forgot Password" and "Create Account" links. f the email and password are correct, it will render the app's ```/home``` page. If they are incorrect, a flash message will appear with the text "Invalid email or password."

![login](/assets/login.gif)

## /home

The `/home` route renders a page that displays all the events you are subscribed to and all the events you have created.

Observations:
- This route uses the `layout.html` template for the header, navigation (nav), and footer.
- This route requires login (`@login_required`) to access.

## /create-event

This route allows for creating an event and is triggered by the "New Event" button on the Events page.

All fields are required to be filled in, including event `title`, `description`, `cost`, `location`, `date`, and `time`.

![login](/assets/create-event.gif)

## /event-list

## /user-list
## /settings
## /records

#### Video Demo:  <URL HERE>