from transformers import *
from sentence_transformers import SentenceTransformer

from transformers import AutoTokenizer, AutoModel
# import yake
# import re
import nltk.data

import nltk
nltk.download('punkt')

tokenizer_nltk_sentence = nltk.data.load('tokenizers/punkt/PY3/english.pickle')


# TOKENIZER = "allenai/scibert_scivocab_uncased"
# MODEL = 'allenai/scibert_scivocab_uncased'

TOKENIZER = "gsarti/scibert-nli"
MODEL = "gsarti/scibert-nli"

'''
class SciBERT:
    def __init__(self):
        print("Loading SciBERT model")
        self.tokenizer = AutoTokenizer.from_pretrained(TOKENIZER)
        self.model = AutoModel.from_pretrained(MODEL)

    def vectorize(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        outputs = outputs[0].mean(dim=0).mean(dim=0)
        return outputs.detach().numpy()
'''

class SciBERT:
    def __init__(self):
        print("Loading SciBERT model")
        self.tokenizer = AutoTokenizer.from_pretrained(TOKENIZER)
        self.model = AutoModel.from_pretrained(MODEL)
        self.model_sentence = SentenceTransformer(MODEL) #We are just going to use this

    # def vectorizeWithYake(self, text):
    #     kw_extractor = yake.KeywordExtractor()
    #     keywords = kw_extractor.extract_keywords(text)
    #     x = re.sub('[^a-zA-Z]', '', str(keywords))
    #     inputs = self.tokenizer(str(x), return_tensors="pt")
    #     outputs = self.model(**inputs)
    #     outputs = outputs[0].mean(dim=0).mean(dim=0)
    #     return outputs.detach().numpy()
    
    def vectorize(self, text):
        #Hugging face is cool        
        # 1. Tokenize text into a list of sentences
        sentences = tokenizer_nltk_sentence.tokenize(text)

        #2. Get each sentence embeddings
        sentence_embeddings = self.model_sentence.encode(sentences)

        #3. Compute the average embedding vector
        mean_embedding = sentence_embeddings.mean(0) #This is in numpy

        #4. Output the average embedding vector
        return mean_embedding

        # # kw_extractor = yake.KeywordExtractor()
        # # keywords = kw_extractor.extract_keywords(text)
        # # x = re.sub('[^a-zA-Z]', '', str(keywords))
        
        # #1. Tokenize text into a list of sentences
        # # sentences = tokenizer_nltk_sentence.tokenize(text)

        # #2. Add special tokens
        # # marked_sentences = []
        # # for sentence in sentences:           
        # #     marked_sentences.append(" [CLS] " + sentence + " [SEP] ")

        # #3. Merge marked_sentences into one sentence
        # # one_marked_sentences = ' '.join(marked_sentences)

        # #4. bert tokenizing text and return tensor
        # # inputs = self.tokenizer(one_marked_sentences, return_tensors="pt")

        # # #5. Map the token strings to their vocabulary indices
        # # indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        # # segments_ids = [1] * len(tokenized_text)

        # #6. Convert inputs

        # # inputs = self.tokenizer(indexed_tokens, return_tensors="pt")
        # # segments_tensors = torch.tensor([segments_ids])

        # # outputs = self.model(**inputs)
        # # outputs = outputs[0].mean(dim=0).mean(dim=0)
        # return outputs.detach().numpy()