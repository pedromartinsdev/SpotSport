# SPOTSPORT 🏅

1. [Description](#description) &nbsp;
2. [Routes](#routes) &nbsp;
    2.1. [/](#/) &nbsp;
    2.2. [/landing-page](#landing-page) &nbsp;
    2.3. [/create-user](#create-user) &nbsp;
    2.4. [/passworod](#password) &nbsp;
    2.5. [/login](#login) &nbsp;
    2.6. [/create-event](#create-event) &nbsp;
    2.7. [/user-list](#user-list) &nbsp;
    2.8. [/event-list](#event-list) &nbsp;
    2.9. [/settings](#settings) &nbsp;
    2.10. [/records](#records) &nbsp;

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
## /landing-page

This route renders a landing page promoting the app.
![landing page imagem](/static/landing-page.gif)

## /create-user

This route renders a register page.
![landing page imagem](/static/create-user.gif)


In this route, the user fills in their information for registration.
It's important to note that all fields are mandatory, except for the photo link.

Before allowing a new user to be created, a database query is performed to check if the ```username``` and ```email``` are already in use.

## /password

This route renders a "Forgot Password" page that prompts the user to enter their email address to receive a password reset link.

![landing page imagem](/static/create-user.gif)


## /login

This route renders a login page where the user must enter their email and password, or click on the "Forgot Password" and "Create Account" links. f the email and password are correct, it will render the app's ```/home``` page. If they are incorrect, a flash message will appear with the text "Invalid email or password."

![login](/static/login.gif)

## /
## /home
## /create-event
## /user-list
## /settings
## /records

#### Video Demo:  <URL HERE>