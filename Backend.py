from flask import Flask, request
import AnimeRecommendation

app = Flask(__name__)

@app.route('/get_anime_recommendation/', methods = ['GET'])
def anime_recommendation():
    recommender = AnimeRecommendation.Recommender()
    if request.method == 'GET':
        title = request.args.get('title')
        recommendation_array = recommender.recommendation_flow(title, True)
        only_titles = recommendation_array[['title']].to_numpy().tolist()
        return only_titles
    else:
        return []
    