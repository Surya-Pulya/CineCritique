import requests
from bs4 import BeautifulSoup
import json
from transformers import pipeline
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer  # You can replace this with LexRankSummarizer, LuhnSummarizer, etc.
class movie_scraper:

    def __init__(self,name):
        self.name=name
        
    def get_movie_info(self):
        data_url=f"http://www.omdbapi.com/?t={self.name}&apikey=79ce9d13"
        resp = requests.get(data_url)
        soup1 = BeautifulSoup(resp.text, 'html.parser')
        data=str(soup1.contents[0])
        data_dict=json.loads(data)
        return data_dict

    def get_movie_reviews(self,id):
        search_url = f"https://www.imdb.com/title/{id}/reviews?ref_=tt_ql_3"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        review_div = soup.find_all('div', class_='text show-more__control')
        review_list = ""  
        for idx, review in enumerate(review_div, start=1):
            review_text = review.get_text().strip()  
            #review_dict = {'Review Number': idx, 'Review Text': review_text} 
            review_list= review_list + review_text +". "
            #review_list.append(review_text)
            #print(f"{idx} reviews to csv")
        #df = pd.DataFrame(review_list)
        return review_list
    
        
    def contextualize_summary(self,summary):
        
        parser = PlaintextParser.from_string(summary, Tokenizer("english"))
        summarizer = LsaSummarizer()  # Choose a summarization algorithm
        summary = summarizer(parser.document, 15)
        raw_summary = ' '.join([str(sentence) for sentence in summary])
        #pipe = pipeline("summarization", model="mabrouk/amazon-review-summarizer-bart")
        #pipe = pipeline("text2text-generation", model="suthanhcong/movie_summarize_model")
        pipe = pipeline("summarization", model="abhiramd22/t5-base-finetuned-to-summarize-movie-reviews")        #best model
        contextual_summary= pipe(raw_summary,min_length=150,max_length=250)
        #contextual_summary = str(contextual_summary).replace(f"\\","")
        return contextual_summary
'''
name="vedalam"
obj=movie_scraper(name)
info=obj.get_movie_info()
print(info)
id=info['imdbID']
reviews= obj.get_movie_reviews(id)
#print(reviews)
print(str(obj.contextualize_summary(reviews)))#[0]['summary_text']))
#with open('output.txt', 'w') as file:
#    file.write(reviews)
'''
