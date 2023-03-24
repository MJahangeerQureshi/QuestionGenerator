# Question Generator

Question Generator is a small demo API/WebApp that generates questions from an arbitrary amount of text. 

## Installation

To run this project on your local machine, follow the steps below:

1. Clone the repository using the following command:
   ```
   git clone https://github.com/MJahangeerQureshi/QuestionGenerator
   ```
2. Navigate to the project directory `cd QuestionGenerator`

3. Create a `.env` file in the main directory with the `OPENAI_API_KEY` as follows:
   ```
   OPENAI_API_KEY=<your_openai_api_key>
   ```

### API

4. Navigate to the `api` directory `cd api`

5. Create a virtual environment `python3 -m venv env`

6. Activate the virtual environment `source env/bin/activate`

7. Install the required packages `pip install -r requirements.txt`

8. Run the API `uvicorn main:app --host 0.0.0.0 --port 9004`

### Frontend

9. Open a new terminal window and navigate to the `frontend` directory `cd ../frontend`

10. Create a virtual environment `python3 -m venv env`

11. Activate the virtual environment `source env/bin/activate`

12. Install the required packages `pip install -r requirements.txt`

13. Run the frontend `streamlit run app.py`

### Docker

You can also run this project using Docker. 

1. Clone the repository using the following command:
   ```
   git clone https://github.com/MJahangeerQureshi/QuestionGenerator
   ```
2. Navigate to the project directory `cd QuestionGenerator`

3. Create a `.env` file in the main directory with the `OPENAI_API_KEY` as follows:
   ```
   OPENAI_API_KEY=<your_openai_api_key>
   ```

4. Build and start the containers using `docker-compose up`

## Usage

### API

After running the API, you can send a POST request to `http://localhost:9004/suggest_questions` with the following JSON payload:

```
{
    "input_text": "Sample text for generating questions."
}
```

This will return a JSON response with a list of generated questions:

```
[
   {
      "Context" : "The Context for the Generated Question",
      "Question" : "The Generated Question",
      "Source" : "OpenAI API or T5 if OpenAI isnt available",
   },
   ....
]
```

### Frontend

After running the frontend, you can access the web app on `http://localhost:9007`. Simply enter some text into the input field and click the "Auto Suggest Questions" button. The generated questions will be displayed below the input field.

## Performing Unit Tests

### Testing without Docker

To perform tests on this project, follow the steps below:

1. Navigate to the `api` directory `cd api`

2. Activate the virtual environment `source env/bin/activate`

3. Run the tests using the following command:
   ```
   python -m unittest
   ```

### Testing with Docker

To perform tests on this project with docker, follow the steps below:

1. Run the tests using the following command:
   ```
   docker-compose exec api python -m unittest
   ```

This will run all the tests in the directory and display the results. Make sure that the API is not running while running the tests.

## License

This project is licensed under the GPL License. See the `LICENSE` file for more information.