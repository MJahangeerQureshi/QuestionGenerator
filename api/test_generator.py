import os  # for using environment variables
import unittest

import numpy as np  # for numerical operations
from tqdm import tqdm  # for displaying progress bars

import openai  # for using OpenAI API

import torch  # for deep learning
import spacy  # for natural language processing

from transformers import T5ForConditionalGeneration, AutoTokenizer  # for text generation

from generator import QuestionGenerater # for testing the generator

# set the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

class TestQuestionGenerater(unittest.TestCase):
    def test_init(self):
        qg = QuestionGenerater(10)
        self.assertEqual(qg.paragraph_lenght, 10)
        self.assertIsInstance(qg.nlp, spacy.lang.en.English)
        self.assertIsInstance(qg.t5_tokenizer, AutoTokenizer)
        self.assertIsInstance(qg.t5_model, T5ForConditionalGeneration)
        self.assertIn(qg.device, ['cuda', 'cpu'])

    def test_get_question(self):
        qg = QuestionGenerater(10)
        context = "This is a sample context."
        answer = "sample"
        question = qg.get_question(context, answer)
        self.assertIsInstance(question, str)
        self.assertGreater(len(question), 0)

    def test_get_question_from_gpt3(self):
        qg = QuestionGenerater(10)
        context = "This is a sample context."
        question = qg.get_question_from_gpt3(context)
        self.assertIsInstance(question, str)
        self.assertGreater(len(question), 0)

    def test_call(self):
        qg = QuestionGenerater(10)
        input_text = "This is a sample context. This is another sample context."
        questions = qg(input_text)
        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 0)
        for q in questions:
            self.assertIsInstance(q, dict)
            self.assertIn("Context", q)
            self.assertIn("Question", q)
            self.assertIn("Source", q)


if __name__ == '__main__':
    unittest.main()
