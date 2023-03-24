import os

import numpy as np
from tqdm import tqdm

import openai

import torch
import spacy

from transformers import T5ForConditionalGeneration, AutoTokenizer

openai.api_key = os.getenv("OPENAI_API_KEY")

class QuestionGenerater:
    def __init__(self, paragraph_lenght=10):
        self.paragraph_lenght = paragraph_lenght
        
        self.nlp = spacy.load("en_core_web_sm")
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.t5_tokenizer = AutoTokenizer.from_pretrained('ramsrigouthamg/t5_squad_v1')
        self.t5_model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_squad_v1').to(self.device)
  
    def get_question(self, context, answer=""):
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

    def get_question_from_gpt3(self, context):
        response = openai.Completion.create(model="text-davinci-003",
                                            prompt=context+'''
                                            Generate a question from the above text
                                            Question: 
                                            ''',
                                        temperature=0.3,
                                        max_tokens=1024,
                                        top_p=1,
                                        frequency_penalty=0,
                                        presence_penalty=0)
        return response['choices'][0]['text'].strip()

    def __call__(self, input_text):
        cleaned_text = ' '.join([i.strip() for i in input_text.splitlines() if i.strip()])
        sentences = [str(i).strip() for i in list(self.nlp(cleaned_text).sents) if str(i).strip()]

        paragraphs = [' '.join(i) for i in np.array_split(sentences, 
                      int(np.round(len(sentences) / self.paragraph_lenght)))]

        #return paragraphs

        questions = []
        gpt3_questions = []
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
            
            except:
                # using open source T5 Weights
                generated_question = self.get_question(context)
                questions.append({
                    "Context":context,
                    "Question": generated_question,
                    "Source":"T5"
                                })
                                
        return questions
