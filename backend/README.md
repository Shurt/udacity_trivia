# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

---

DONE: Start documentation here.

# API Documentation:

* GET `/categories`:
    - Produces a dictionary of available categories from the database.
    - Arguments: None
    - Response: Available categories
        * Example:
            ```json
            {
                "success": true,
                "categories": [
                    {
                        "id": 1,
                        "type": "Science"
                    },
                    {
                        "id": 2,
                        "type": "Art"
                    },
                    {
                        "id": 3,
                        "type": "Geography"
                    },
                    {
                        "id": 4,
                        "type": "History"
                    },
                    {
                        "id": 5,
                        "type": "Entertainment"
                    },
                    {
                        "id": 6,
                        "type": "Sports"
                    },
            ]}
            ```
* GET `/questions?page=[page_number]`:
    - Produces a dictionary of questions, which provides the answer, category, difficulty, id and question text.
    - Arguments: page_number => page number of questions.
    - Response: List of questions, count of total questions, current category, and list of categories.
        * Example:
            ```json
            {
            "questions": [
                {
                    "answer": "Maya Angelou",
                    "category": 4,
                    "difficulty": 2,
                    "id": 5,
                    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                },
                {
                    "answer": "Muhammad Ali",
                    "category": 4,
                    "difficulty": 1,
                    "id": 9,
                    "question": "What boxer's original name is Cassius Clay?"
                },
                {
                    "answer": "Apollo 13",
                    "category": 5,
                    "difficulty": 4,
                    "id": 2,
                    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                },
                {
                    "answer": "Tom Cruise",
                    "category": 5,
                    "difficulty": 4,
                    "id": 4,
                    "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
                },
                {
                    "answer": "Edward Scissorhands",
                    "category": 5,
                    "difficulty": 3,
                    "id": 6,
                    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
                },
                {
                    "answer": "Brazil",
                    "category": 6,
                    "difficulty": 3,
                    "id": 10,
                    "question": "Which is the only team to play in every soccer World Cup tournament?"
                },
                {
                    "answer": "Uruguay",
                    "category": 6,
                    "difficulty": 4,
                    "id": 11,
                    "question": "Which country won the first ever soccer World Cup in 1930?"
                },
                {
                    "answer": "George Washington Carver",
                    "category": 4,
                    "difficulty": 2,
                    "id": 12,
                    "question": "Who invented Peanut Butter?"
                },
                {
                    "answer": "Lake Victoria",
                    "category": 3,
                    "difficulty": 2,
                    "id": 13,
                    "question": "What is the largest lake in Africa?"
                },
                {
                    "answer": "The Palace of Versailles",
                    "category": 3,
                    "difficulty": 3,
                    "id": 14,
                    "question": "In which royal palace would you find the Hall of Mirrors?"
                }
            ],
            "page": 1,
            "totalQuestions": 19,
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            }
            }
            ```
* DELETE `/questions/[question_id]`:
    - Removes a question from the database.
    - Arguments: question_id => ID of the question to be deleted.
        * Example:
            ```json
            {
                "question_id": 10
            }
            ```
    - Response: Success or failure message.
        * Example:
            ```json
            {
                "success": true
            }
            ```
* POST `/questions`:
    - Creates a question with the supplied data.
    - Arguments: question => Question text, answer => Answer text, difficulty => Question difficulty, category => Question category
        * Example:
            ```json
            {
                "question": "What is the secret of life, the universe and everything?",
                "answer": "42",
                "difficulty": "5",
                "category": 1
            }
            ```
    - Response: Success or failure message.
        * Example:
            ```json
            {
                "success": true
            }
            ```
* POST `/searchQuestions`:
    - Searches the database for the supplied query.
    - Arguments: searchTerm => Search query
        * Example:
            ```json
            {
                "searchTerm": "secret to life"
            }
            ```
    - Response: List of questions matching the query, number of questions matching and current category
        * Example:
            ```json
            {
                "current_category": 1,
                "questions": [
                    {
                        "question": "What is the secret of life, the universe and everything?",
                        "answer": "42",
                        "difficulty": "5",
                        "category": 1
                    }
                ],
                "total_questions": 1,
                "success": true
            }
            ```
* GET `/categories/[category_id]/questions?page=[page_number]`:
    - Retrieve questions based on the supplied category ID.
    - Arguments: category_id => Category ID number, page_number => current page of questions
        * Example:
            ```json
            {
                "category_id": 6,
                "page_number": 2
            }
            ```
    - Response: Lists all questions matching the provided category, the total number of questions matching that category, current category and all categories
        * Example:
            ```json
            {
                "questions": [
                    {
                        "answer": "Brazil",
                        "category": 6,
                        "difficulty": 3,
                        "id": 10,
                        "question": "Which is the only team to play in every soccer World Cup tournament?"
                    },
                    {
                        "answer": "Uruguay",
                        "category": 6,
                        "difficulty": 4,
                        "id": 11,
                        "question": "Which country won the first ever soccer World Cup in 1930?"
                    },
                ],
                "totalQuestions": 19,
                "categories": {
                    "1": "Science",
                    "2": "Art",
                    "3": "Geography",
                    "4": "History",
                    "5": "Entertainment",
                    "6": "Sports"
                }
            }
            ```
* POST `/quizzes`:
    - Returns list of questions for starting the quiz.
    - Arguments: quiz_category => Category to select questions from, previous_questions => array containing the previous questions asked during this quiz.
        * Example:
            ```json
            {
                "previous_questions": [],
                "quiz_category": {
                    "type": "Sports",
                    "id": 6
                }
            }
            ```
    - Response: Randomized set of questions from the provided category.
        * Example:
            ```json
            {
                "answer": "Uruguay",
                "category": 6,
                "difficulty": 4,
                "id": 11,
                "question": "Which country won the first ever soccer World Cup in 1930?"
            }
            ```
        


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```