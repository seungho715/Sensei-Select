import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import axios from 'axios'
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [data, setData] = useState([]);

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
        console.log("Parsed Data Structure:", parsedData);
        console.log("First Entry:", parsedData.data[0]);
        setData(parsedData.data);
      });
  }, []);

  const handleSearch = () => {
    if (query) {
      console.log("Search Query:", query);

      const filteredData = data.filter(anime =>
        anime['title_romanji'] &&
        anime['title_romanji'].toLowerCase().includes(query.toLowerCase())
      );

      console.log("Filtered Data:", filteredData);
      setResults(filteredData);
    } else {
      setResults([]);
    }
  };

  const handleRecommend = () => {
    // Provide a recommendation, e.g., based on the highest average score
    let recommendation;
    console.log(query)
    axios.get(`http://51.81.33.212:5000/get_anime_recommendation?title=${query}`)
    .then(function (response) {
      console.log(response);
      recommendation = response
    })
    .catch(function (error) {
      console.log(error);
    });

    //const recommendation = data.sort((a, b) => b['average_score'] - a['average_score'])[0];
    if (recommendation) {
      setQuery(recommendation['title_romanji']); // Autofill search bar
      setResults([recommendation]); // Display it directly
    }
  };

  const handleTitleClick = (title) => {
    setQuery(title); // Autofill search bar
    handleSearch(); // Trigger search
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
          <ul className="results">
            {results.map((anime, index) => (
              <li key={index}>
                <button className="title-btn" onClick={() => handleTitleClick(anime['title_romanji'])}>
                  {anime['title_romanji']}
                </button>
              </li>
            ))}
          </ul>
        )}
      </header>
    </div>
  );
}

export default App;
