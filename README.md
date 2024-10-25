# Social Media API


The Social Media API provides a backend service for a 
social media platform. Users can register, log in, 
and perform various actions such as creating posts, 
following other users, and interacting with posts through 
likes and comments. The API is built using Django and 
Django REST Framework, and it is designed to be scalable 
and easily extendable.

## Overview
The Social Media API provides a backend service for a social media platform. Users can register, log in, and perform various actions such as creating posts, following other users, and interacting with posts through likes and comments. The API is built using Django and Django REST Framework, and it is designed to be scalable and easily extendable.

# Features

### User Registration and Authentication: 
* Secure user registration and authentication using JWT tokens.

### User Profiles: 
* Users can create, update, delete their profiles, and upload profile pictures.

### Follow/Unfollow: 
* Users can follow or unfollow other users and view their followers and following lists.

### Posts:
* Users can create, update, delete, and view posts. Posts can include text and optional media attachments.

### Likes and Comments: 
* Users can like/unlike posts and add comments to posts.

### Search: 
* Users can search for other users by email or bio.

### JWT Authentication:
* Secure API access with JSON Web Tokens.

### Image Uploads:
*  Users can upload and manage images as part of their profiles or posts.

### Admin Panel: 
* A built-in admin panel to manage users, posts, and other data.

### Technologies Used
* Django: A high-level Python web framework.
* Django REST Framework: A powerful and flexible toolkit for building Web APIs.
* PostgreSQL: A powerful, open-source relational database.
* Redis: An in-memory data structure store, used as a message broker for Celery.
* Celery: An asynchronous task queue based on distributed message passing.

### API Endpoints
User Endpoints:

- POST /api/user/register/: Register a new user.
- POST /api/user/token/: Obtain a JWT token.
- GET /api/user/me/: Retrieve or update the logged-in user's profile.
- DELETE /api/user/me/: Delete the logged-in user's profile.
- GET /api/user/profile/< id >/: View another user's profile.
- GET /api/user/search/: Search users by email or bio.
- POST /api/user/< pk >/follow/: Follow a user.
- POST /api/user/< pk >/unfollow/: Unfollow a user.
- GET /api/user/me/following/: List users the logged-in user is following.
- GET /api/user/me/followers/: List users following the logged-in user.

Post Endpoints:

- GET /api/media_api/posts/: List all posts.
- POST /api/media_api/posts/: Create a new post.
- GET /api/media_api/posts/< id >/: Retrieve a specific post.
- PUT /api/media_api/posts/< id >/: Update a specific post.
- DELETE /api/media_api/posts/< id >/: Delete a specific post.
- POST /api/media_api/posts/< id >/like/: Like a post.
- POST /api/media_api/posts/< id >/unlike/: Unlike a post.
- POST /api/media_api/posts/< id >/comment/: Comment on a post.

## Installation
Python3 must be already installed
* git clone https://github.com/romanshupak/social-media-api.git
* cd social_media_api
* python -m venv venv
* venv\Scripts\activate (on Windows)
* source venv/bin/activate (on macOS)
* pip install -r requirements.txt
* python manage.py migrate
* python manage.py runserver

### Environment Variables
To configure the application, you need to set up the following environment variables in your .env file:

* POSTGRES_PASSWORD: The password for your PostgreSQL database.
* POSTGRES_USER: The username for your PostgreSQL database.
* POSTGRES_DB: The name of your PostgreSQL database.
* POSTGRES_HOST: The host address for your PostgreSQL database (e.g., localhost or the address of your PostgreSQL server).
* POSTGRES_PORT: The port number on which your PostgreSQL database is running.
* DJANGO_SECRET_KEY: The secret key used by Django for security purposes. This should be a long, random string.
* CELERY_BROKER_URL=CELERY_BROKER_URL
* CELERY_RESULT_BACKEND=CELERY_RESULT_BACKEND

Make sure to replace the placeholder values with your actual configuration settings before running the application.

## Getting access
* create user via /api/user/register/
* get access token via /api/user/token/

## Additional Info
For demonstration purposes, you can use the following token credentials:

1) Email: media_user@media.com, Password: mediauser
2) Email: media_user_1@media.com, Password: mediauser_1
3) Email: media_user_2@media.com, Password: mediauser_2

#### These credentials provide access, allowing you to explore the application's features.