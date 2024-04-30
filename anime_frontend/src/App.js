import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  //const [results, setResults] = beState([]); // Commented this out
  const [results, setResults] = useState([]);
  const [data, setData] = useState([]);
  const [recommendation, setRecommendation] = useState(null);

  useEffect(() => {
    fetch('/Media.csv')
      .then(response => response.text())
      .then(csvText => {
        console.log("CSV Text:", csvText);

        const parsedData = Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          error: (error, row, index) => {
            console.log("Parsing Error:", error, "Row:", row, "Index:", index);
          }
        });

        if (parsedData.errors.length > 0) {
          console.log("Parsing Errors:", parsedData.errors);
          return;
        }

        console.log("Parsed Data Structure:", parsedData);
        console.log("First Entry:", parsedData.data[0]);
        setData(parsedData.data);
      })
      .catch(error => {
        console.log("Error fetching or parsing CSV:", error);
      });
  }, []);

  const handleSearch = () => {
    if (query) {
      console.log("Search Query:", query);

      const filteredData = data.filter(anime =>
        anime['title_english'] &&
        anime['title_english'].toLowerCase().includes(query.toLowerCase())
      );

      console.log("Filtered Data:", filteredData);
      setResults(filteredData);
    } else {
      setResults([]);
    }
  };

  const handleRecommend = () => {
    console.log(query);

    axios.get(`http://51.81.33.212:5000/get_anime_recommendation?title=${encodeURIComponent(query)}`)
    .then(response => {
      console.log(response.data);

      const ids = response.data.map(item => item[0]); // ID Extraction?
      console.log("IDs:", ids);

      const filteredData = data.filter(anime => ids.includes(parseInt(anime['id'], 10)));

      console.log("Filtered Data:", filteredData);
      setRecommendation(filteredData);
    })
    .catch(error => {
      console.log("Error fetching recommendation:", error.message, error.response?.status, error.response?.data);
    });
  };

  const handleTitleClick = (title) => {
    setQuery(title);
    handleSearch();
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Sensei Select</h1>
        <div className="search-container">
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Search anime..."
            className="search-bar"
          />
          <button className="search-btn" onClick={handleSearch}>Search</button>
          <button className="recommend-btn" onClick={handleRecommend}>Recommend Me</button>
        </div>
        {results.length > 0 && (
          <ul class="results">
            {results.map((anime, index) => (
              <li key={index}>
                <div class="anime-item">
                  <img src={anime['cover_image_medium']} alt={anime['title_english']} class="anime-cover" />
                  <button class="title-btn" onClick={() => handleTitleClick(anime['title_english'])}>
                    {anime['title_english']}
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
        {recommendation && (
          <div class="recommendation">
            <h2>Recommendation</h2>
            <ul>
              {recommendation.map((anime, index) => (
                <li key={index}>
                  <div class="anime-item">
                    <img src={anime['cover_image_medium']} alt={anime['title_romanji']} class="anime-cover" />
                    <a href={anime['site_url']} target="_blank" rel="noopener noreferrer">
                      {anime['title_romanji']}
                    </a>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
