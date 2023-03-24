# QuestionGenerator

QuestionGenerator is a small demo API/WebApp that generates questions from an arbitrary amount of text. 

## Installation

To run this project on your local machine, follow the steps below:

1. Clone the repository using the following command:
   ```
   git clone <repository_url>
   ```
2. Navigate to the project directory `cd QuestionGenerator`

### API

3. Navigate to the `api` directory `cd api`

4. Create a virtual environment `python3 -m venv env`

5. Activate the virtual environment `source env/bin/activate`

6. Install the required packages `pip install -r requirements.txt`

7. Run the API `python main.py`

### Frontend

8. Open a new terminal window and navigate to the `frontend` directory `cd ../frontend`

9. Create a virtual environment `python3 -m venv env`

10. Activate the virtual environment `source env/bin/activate`

11. Install the required packages `pip install -r requirements.txt`

12. Run the frontend `python app.py`

### Docker

You can also run this project using Docker. 

1. Clone the repository using the following command:
   ```
   git clone <repository_url>
   ```
2. Navigate tothe project directory `cd QuestionGenerator`

3. Build and start the containers using `docker-compose up`

## Usage

### API

After running the API, you can send a POST request to `http://localhost:8000/generate` with the following JSON payload:

```
{
    "text": "Sample text for generating questions."
}
```

This will return a JSON response with a list of generated questions:

```
{
    "questions": [
        "What is the sample text for generating questions?",
        "What can be generated from sample text?",
        "What is the purpose of generating questions from sample text?"
    ]
}
```

### Frontend

After running the frontend, you can access the web app on `http://localhost:5000`. Simply enter some text into the input field and click the "Generate Questions" button. The generated questions will be displayed below the input field.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.