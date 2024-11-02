from flask import Flask, render_template, request
import movie_scraper
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST','GET'])
def search_movie():
    
    movie_name = request.form['movie_name']
    print(f"Received movie name: {movie_name}")
    scraper = movie_scraper.movie_scraper(movie_name)
    info = scraper.get_movie_info()
    print("Got the movie info..")
    id=info['imdbID']
    reviews=scraper.get_movie_reviews(id)
    print("Scraped the reviews..")
    summary=str(scraper.contextualize_summary(reviews)[0]['summary_text'])

    poster=info['Poster']
    return render_template('moviepage.html',movie=info,poster=poster, summary=summary)
    

if __name__ == '__main__':
    app.run(debug=True)
    
