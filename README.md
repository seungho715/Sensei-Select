# Sensei-Select

## Instructions for setting up Backend environment and running

1. Create a Python virtual Environment and install the following packages with `pip`: `numpy pandas tensorflow matplotlib sklearn flask`
2. Run `flask --app Backend run`
3. Now, you can make a GET request to the http backend with cURL: `curl -G -d "title=Naruto" http://localhost:5000/get_anime_recommendation/`. Replace the **title** parameter with the Romaji name of an anime.

## Instructions for setting up Frontend environment and running

1. Either remove or change the `"homepage": "https://seungho715.github.io/Sensei-Select"` field in the `anime_frontend/package.json` file on line 4 to `"homepage": "http://localhost:3000"`
2. Within the `anime_frontend` directory, run the command `npm install` then `npm run start`
3. Log onto localhost:3000 and type in the name of an Anime
4. Click the Search button to select the particular title of your Anime
5. Click the Recommend Me button and scroll to the bottom of the page (after an approximately 10 second loading time) to view your top 10 recommendations
6. Click on the title of the Anime to go to its Anilist page

## Data Set Used

Our data set was gathered from [Anilist.co](https://anilist.co/search/anime) using their [GraphQL API](https://anilist.co/graphiql). This includes extensive information relating to each anime, including tags, characters, voice actors, staff, studios, etc. All of the data scraped has been formatted into tables that can be found in the [Tables](Tables) folder.  

The majority of our data has been collect throughout April 2024. As Anilist will continue to update their database, the tables saved here will eventually become outdated. 
