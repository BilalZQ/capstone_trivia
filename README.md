# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Endpoints
### GET `'/categories'`
- General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
- Sample: `curl http://127.0.0.1:5000/categories`
``` json5
{
	"categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
	},
	"success": true
}
```


### GET `'/questions'`
- General:
    - Returns a dictionary of categories, list of questions including id, questions, answer, category, difficulty & current category along with total count of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    - Request Arguments: Page Number
    - Returns: Dictionary of categories, list of questions & total count of questions
- Sample: `curl http://127.0.0.1:5000/questions`
``` json5
{
	"categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
	},
	"current_category": null,
	"questions": [{
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
			"answer": "Maya Angelou",
			"category": 4,
			"difficulty": 2,
			"id": 5,
			"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
		},
		{
			"answer": "Edward Scissorhands",
			"category": 5,
			"difficulty": 3,
			"id": 6,
			"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
		},
		{
			"answer": "Muhammad Ali",
			"category": 4,
			"difficulty": 1,
			"id": 9,
			"question": "What boxer's original name is Cassius Clay?"
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
	"success": true,
	"total_questions": 47
}
```
### DELETE `'/questions/<int:question_id>'`
- General:
    - Deletes the questions of the given ID if it exists.
    - Request Arguments: Question ID
    - Returns status true with status code 204 if question was deleted successfully
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/4`
``` json5
{
    "success": true,
}
```
### POST `'/questions'`
- General:
    - Create a new question from request body
    - Request Body: Question, Answer, Difficulty & Category
    - Returns success true, status code 201 along with id of the question that was created successfully
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"TestQ", "answer":"TestA", "category":"1", "difficulty":"1"}'`
``` json5
{
	"id": 83,
	"success": true
}
```

### PATCH `'/questions<int:question_id>'`
- General:
    - Update a question for given question id.
    - Request Body: Question, Answer, Difficulty & Category
    - Returns success true, status code 201 along with id of the question that was created successfully

```json5

{
    "question": "TestQ",
    "answer": "TestA",
    "category": 1,
    "difficulty": 1
}
```

### POST `'/questions/search'`
- General:
    - Searches for questions based on passed search term
    - Request Body: Search Term
    - Returns success true, status code 200 along with list of the questions containing the search term
- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"what"}'`
``` json5
{
	"questions": [{
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
			"answer": "Edward Scissorhands",
			"category": 5,
			"difficulty": 3,
			"id": 6,
			"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
		},
		{
			"answer": "Lake Victoria",
			"category": 3,
			"difficulty": 2,
			"id": 13,
			"question": "What is the largest lake in Africa?"
		},
		{
			"answer": "Mona Lisa",
			"category": 2,
			"difficulty": 3,
			"id": 17,
			"question": "La Giaconda is better known as what?"
		},
		{
			"answer": "The Liver",
			"category": 1,
			"difficulty": 4,
			"id": 20,
			"question": "What is the heaviest organ in the human body?"
		},
		{
			"answer": "Blood",
			"category": 1,
			"difficulty": 4,
			"id": 22,
			"question": "Hematology is a branch of medicine involving the study of what?"
		}
	],
	"success": true
}
```
### GET `'/categories/<int:category_id>/questions'`
- General:
    - Get all the questions belonging to category id passed.
    - Request Arguments: Category ID
    - Returns success true, status code 200 along with list of the questions, count of total questions & current category
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`
``` json5
{
	"current_category": {
		"id": 2,
		"type": "Art"
	},
	"questions": [{
			"answer": "Escher",
			"category": 2,
			"difficulty": 1,
			"id": 16,
			"question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
		},
		{
			"answer": "Mona Lisa",
			"category": 2,
			"difficulty": 3,
			"id": 17,
			"question": "La Giaconda is better known as what?"
		},
		{
			"answer": "One",
			"category": 2,
			"difficulty": 4,
			"id": 18,
			"question": "How many paintings did Van Gogh sell in his lifetime?"
		},
		{
			"answer": "Jackson Pollock",
			"category": 2,
			"difficulty": 2,
			"id": 19,
			"question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
		}
	],
	"success": true,
	"total_questions": 4
}
```
### POST `'/quizzes'`
- General:
    - Gets questions for quiz
    - Request Body: Quiz Category, Previous Questions list
    - Returns a random question from given category excluding previous questions.
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"Science","id":"1"}}'`
``` json5
{
	"question": {
		"answer": "Blood",
		"category": 1,
		"difficulty": 4,
		"id": 22,
		"question": "Hematology is a branch of medicine involving the study of what?"
	},
	"success": true
}
```
### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 401: Unauthorized Request
- 403: Forbidden Request

Permissions
--------------------------------------------------------

- `add-question` permission for POST `'/questions'` api to add new question
- `edit-question` permission for PATCH `'/questions<int:question_id>'` api to edit existing question
- `delete-question` permission for DELETE `'/questions<int:question_id>'` api to delete existing question
- `play-quiz` permission POST `'/quizzes'` api to play quiz

Roles
--------------------------------------------------------
### Admin

Can add/edit/delete question and play quiz

Permissions:

- `add-question`
- `edit-question`
- `delete-question`
- `play-quiz`

### User

Can play quiz

Permissions:

- `play-quiz`

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Deployed Project
Tokens for api end points are available `trivia_tokens.json` file. They have enhanced expiration duration.

Below url can be used to retrieve token.

```
https://udacityfsnd.auth0.com/authorize?audience=capstone&response_type=token&client_id=hZOMNJb2DXT6khq5FWsmeblr7SE3wUNz&redirect_uri=http://localhost:5000/
```


Web app is deployed at:

```
https://capstone-trivia.herokuapp.com/
```