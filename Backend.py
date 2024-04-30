from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
import AnimeRecommendation

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

@app.route('/get_anime_recommendation', methods = ['GET', 'OPTIONS'])
@cross_origin()
def anime_recommendation():
    if request.method == "OPTIONS": # CORS preflight
        print("Sending back preflight")
        return _build_cors_preflight_response()
    recommender = AnimeRecommendation.Recommender()
    if request.method == 'GET':
        title = request.args.get('title')
        recommendation_array = recommender.recommendation_flow(title, True)
        only_titles = recommendation_array[['id']].to_numpy().tolist()
        return only_titles
    else:
        return []
    
