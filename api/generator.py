import os  # for using environment variables

import numpy as np  # for numerical operations
from tqdm import tqdm  # for displaying progress bars

import openai  # for using OpenAI API

import torch  # for deep learning
import spacy  # for natural language processing

from transformers import T5ForConditionalGeneration, AutoTokenizer  # for text generation

# set the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

class QuestionGenerater:
    """A class for generating a question from a given paragraph"""
    def __init__(self, paragraph_lenght: int = 10):
        """
        Initialize the Question Generator
        
        Args:
            paragraph_lenght (int): Length of the paragraph
        """
        self.paragraph_lenght = paragraph_lenght
        
        self.nlp = spacy.load("en_core_web_sm")
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.t5_tokenizer = AutoTokenizer.from_pretrained('ramsrigouthamg/t5_squad_v1')
        self.t5_model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_squad_v1').to(self.device)
  
    def get_question(self, context: str, answer: str = "") -> str:
        """
        Generate a question from the given context and answer
        
        Args:
            context (str): The context in which the question needs to be generated
            answer (str): The answer to the question
            
        Returns:
            str: The generated question
        """
        text = "context: {} answer: {}".format(context,answer)
      
        encoding = self.t5_tokenizer.encode_plus(text,
                                    max_length = 256, 
                                    pad_to_max_length = False,
                                    truncation = True, 
                                    return_tensors="pt",
                                    ).to(self.device)

        outs = self.t5_model.generate(input_ids=encoding["input_ids"],
                                    attention_mask=encoding["attention_mask"],
                                    early_stopping=True,
                                    num_beams=5,
                                    num_return_sequences=1,
                                    no_repeat_ngram_size=2,
                                    max_length=300)
        dec = [self.t5_tokenizer.decode(ids, skip_special_tokens = True) for ids in outs]

        question = dec[0].replace("question:","")
        question = question.strip()
        return question

    def get_question_from_gpt3(self, context: str) -> str:
        """Generates a question from the given context using GPT-3.
        
        Args:
            self (object): The class instance.
            context (str): The context from which to generate the question.
        
        Returns:
            str: The generated question.
        """
        response = openai.Completion.create(model="text-davinci-003",
                                            prompt=context+'''
                                            Generate a question from the above text
                                            Question: 
                                            ''',
                                        temperature=0.3,
                                        max_tokens=427,
                                        top_p=1,
                                        frequency_penalty=0,
                                        presence_penalty=0)
        # strip() removes any leading or trailing whitespaces
        return response['choices'][0]['text'].strip()

    def __call__(self, input_text: str) -> list:
        """Generate questions from arbitrary paragraphs.

        Args:
            input_text (str): The text to generate questions from.

        Returns:
            list: A list of dictionaries containing the generated context and question, as well as the source.
        """
        cleaned_text = ' '.join([i.strip() for i in input_text.splitlines() if i.strip()])
        sentences = [str(i).strip() for i in list(self.nlp(cleaned_text).sents) if str(i).strip()]

        num_chunks = int(np.round(len(sentences) / self.paragraph_lenght))

        # check if num_chunks is 0
        if num_chunks:
            paragraphs = [' '.join(i) for i in np.array_split(sentences, num_chunks)]
        else:
            paragraphs = [' '.join(sentences)]
        
        questions = []
        for context in tqdm(paragraphs, 
                            desc="Generating Questions from Arbitrary Paragraphs"):

            try:
                # using propietry API for GPT-3.5
                generated_gpt3_question = self.get_question_from_gpt3(context)
                questions.append({
                    "Context":context,
                    "Question": generated_gpt3_question,
                    "Source":"OpenAI API"
                                })
            
            # if OpenAI API fails, use open source T5 Weights 
            except:
                generated_question = self.get_question(context)
                questions.append({
                    "Context":context,
                    "Question": generated_question,
                    "Source":"T5"
                                })

        return questions
