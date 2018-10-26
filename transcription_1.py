from __future__ import print_function
import time
import boto3
import nltk
import requests
import string 
import collections
from textblob import TextBlob
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from textblob import Word



def aws_transcribe(job_name,job_uri):
    transcribe = boto3.client('transcribe', region_name = 'eu-west-1')
    job_uri = "https://s3-eu-west-1.amazonaws.com/cc18-videos/CC18_audio/09713108-36c7-4232-bde7-2a2ece553088_The_sole_obligation_of_a_firm_is_to_create_wealth_for_its_shareholders.mp3"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    return status



def get_text(response):
    trans_url = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    text = requests.get(trans_url)
    text = text.json()
    text = text['results']['transcripts']
    text = text[0]['transcript']
    return text 


class text_analysis:

    def __init__(self, input_text):
        self.text = input_text
        self.processed_text = input_text 

    def number_of_words(self):
        word_count = lambda x: len(str(x).split(" "))
        n_words = word_count(self.text)            
        return n_words

    def number_of_characters(self):
        return len(self.text) 

    def average_word_length(self):
        words = self.text.split(' ')
        words = [len(i) for i in words]
        awl = sum(words) / len(words)
        return awl 

    def number_of_stopwords(self):
        stop = nltk.corpus.stopwords.words('english')
        f = lambda x : len([x for x in x.split() if x in stop])
        nsw = f(self.text)
        return nsw

    def number_of_special_characters(self):    
        pass

    def number_of_numerics(self):
        pass


    def make_lower_case(self):
        f = lambda x: " ".join(x.lower() for x in x.split())
        out = f(self.text)
        self.processed_text = f(self.processed_text)
        return out

    def remove_punctuation(self):
        table = str.maketrans({key: None for key in string.punctuation})
        out = self.text.translate(table)
        self.processed_text = self.processed_text.translate(table)
        return out


    def remove_stop_words(self):
        stop = stopwords.words('english')
        f = lambda x: " ".join(x for x in x.split() if x not in stop) 
        out = f(self.text)
        self.processed_text = f(self.processed_text)
        return out 

    def remove_common_words(self):
        temp = self.text.split()
        counter = collections.Counter(temp)
        most_common = counter.most_common(10)
        keys = [x[0] for x in most_common]
        f = lambda x: " ".join(x for x in x.split() if x not in keys)
        out = f(self.text)
        self.processed_text = f(self.processed_text)
        return out

    def remove_rare_words(self):
        temp = self.text.split()
        counter = collections.Counter(temp)
        least_common = counter.most_common()[-10:]
        keys = [x[0] for x in least_common]
        f = lambda x: " ".join(x for x in x.split() if x not in keys)
        out = f(self.text)
        self.processed_text = f(self.processed_text)
        return out

    def tokenise(self):
        out = TextBlob(self.text).words
        self.processed_text = TextBlob(self.processed_text).words
        return out

    def stemming(self):
        st = PorterStemmer()
        f = lambda x: " ".join([st.stem(word) for word in x.split()])
        out = f(self.text)
        self.processed_text = f(self.processed_text)
        return out

    def lemmatisation(self):
        f = lambda x : " ".join([Word(word).lemmatize() for word in x.split()])
        out = f(self.text)
        self.processed_text = f(self.processed_text)
        return out 

    def pre_processing(self):
        self.make_lower_case()
        self.remove_punctuation()
        self.remove_stop_words()
        self.remove_common_words()
        self.remove_rare_words()
        #self.tokenise()
        self.lemmatisation()


    def n_gram(self, number):
        return TextBlot(self.processed_text).n_gram(number)

    def term_frequency(self):
        pass







def main():
    pass 
    








