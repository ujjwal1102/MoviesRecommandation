# Movie Review API

## Overview

The Movie Review API is a Django REST framework application that allows users to register, log in, and interact with a database of movies and reviews. This API supports JWT authentication, enabling secure access to various endpoints for creating, reading, updating, and deleting movies and reviews. Additionally, the API includes a recommendation system that suggests similar movies based on user interactions.

## Features

- **User Authentication**: Register and log in with JWT tokens.
- **CRUD Operations**: Perform Create, Read, Update, and Delete operations on movies and reviews.
- **Movie Recommendations**: Get recommendations for similar movies based on the selected movie.
- **API Documentation**: Interactive API documentation using Swagger.

## Technologies Used

- **Django**: Web framework for building the API.
- **Django REST framework**: Toolkit for building Web APIs.
- **JWT (JSON Web Tokens)**: Secure authentication mechanism.
- **Swagger**: API documentation and testing tool.
- **Pandas**: Data manipulation and analysis.
- **Scikit-learn**: Machine learning library for implementing the recommendation system.
- **SQLite**: Database for storing movie and review data.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ujjwal1102/MoviesRecommandation.git
    cd movie-review-api
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

## Usage

### Authentication

- **Register**: `POST /api/auth/register/`
- **Login**: `POST /api/auth/login/`
- **Token Refresh**: `POST /api/auth/refresh/`

### Movies

- **List Movies**: `GET /api/movies/`
- **Retrieve Movie**: `GET /api/movies/{id}/`
- **Create Movie**: `POST /api/movies/`
- **Update Movie**: `PUT /api/movies/{id}/`
- **Delete Movie**: `DELETE /api/movies/{id}/`
- **Recommendations**: `GET /api/movies/{id}/recommendations/`

### Reviews

- **List Reviews**: `GET /api/reviews/`
- **Retrieve Review**: `GET /api/reviews/{id}/`
- **Create Review**: `POST /api/reviews/`
- **Update Review**: `PUT /api/reviews/{id}/`
- **Delete Review**: `DELETE /api/reviews/{id}/`

### API Documentation

Access the interactive API documentation at: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

## Postman Workspace

You can test the API using the Postman workspace available at: [Postman Workspace Link](https://web.postman.co/workspace/dda35b36-95cf-41e9-8a85-f03ffbc66006/collection/36195995-f605b5fe-bfe0-4e82-ad97-23418e434e82?action=share&source=copy-link&creator=36195995)

## Thankyou

