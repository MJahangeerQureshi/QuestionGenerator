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
    def __init__(self):
        self.qg = QuestionGenerater(10)

    def test_init(self):
        self.assertEqual(self.qg.paragraph_lenght, 10)
        self.assertIsInstance(self.qg.nlp, spacy.lang.en.English)
        self.assertIsInstance(self.qg.t5_model, T5ForConditionalGeneration)
        self.assertIn(self.qg.device, ['cuda', 'cpu'])

    def test_get_question(self):
        context = "This is a sample context."
        answer = "sample"
        question = self.qg.get_question(context, answer)
        self.assertIsInstance(question, str)
        self.assertGreater(len(question), 0)

    def test_get_question_from_gpt3(self):
        context = "This is a sample context."
        question = self.qg.get_question_from_gpt3(context)
        self.assertIsInstance(question, str)
        self.assertGreater(len(question), 0)

    def test_call(self):
        input_text = "This is a sample context. This is another sample context."
        questions = self.qg(input_text)
        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 0)
        for q in questions:
            self.assertIsInstance(q, dict)
            self.assertIn("Context", q)
            self.assertIn("Question", q)
            self.assertIn("Source", q)


if __name__ == '__main__':
    unittest.main()
