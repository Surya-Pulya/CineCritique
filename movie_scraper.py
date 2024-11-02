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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        search_url = f"https://www.imdb.com/title/{id}/reviews/?ref_=tt_urv_sm"
        response = requests.get(search_url,headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        review_div = soup.find_all('div', class_="ipc-html-content-inner-div")
        print(review_div)
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
        summary = summarizer(parser.document, 20)
        raw_summary = ' '.join([str(sentence) for sentence in summary])
        #pipe = pipeline("summarization", model="mabrouk/amazon-review-summarizer-bart")
        #pipe = pipeline("text2text-generation", model="suthanhcong/movie_summarize_model")
        pipe = pipeline("summarization", model="abhiramd22/t5-base-finetuned-to-summarize-movie-reviews")        #best model
        #pipe = pipeline("summarization", model="openai-community/gpt2")
        contextual_summary= pipe(raw_summary,min_length=200,max_length=300)
        #contextual_summary = str(contextual_summary).replace(f"\\","")
        return contextual_summary



'''
name="interstellar"
obj=movie_scraper(name)
info=obj.get_movie_info()
#print(info)
id=info['imdbID']
print(id)
reviews= obj.get_movie_reviews(id)
print(len(reviews))
print(str(obj.contextualize_summary(reviews)))#[0]['summary_text']))
#with open('output.txt', 'w') as file:
#    file.write(reviews)
'''