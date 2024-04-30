# Sensei-Select

## Instructions for setting up environment and running

1. Create a Python virtual Environment and install the following packages with `pip`: `numpy pandas tensorflow matplotlib sklearn flask`
2. Run `flask --app Backend run`
3. Now, you can make a GET request to the http backend with cURL: `curl -G -d "title=Naruto" http://localhost:5000/get_anime_recommendation/`. Replace the **title** parameter with the Romaji name of an anime.