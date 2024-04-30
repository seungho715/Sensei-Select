import React, { useState } from 'react';
import { IconButton, InputBase, Paper, Typography, Box, Select, MenuItem } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { styled } from '@mui/material/styles';

// Styled components moved outside the functional component
const StyledSearchBar = styled(Paper)({
    borderRadius: 4, // Assuming a default radius as theme is not used
    backgroundColor: 'paper', // Assuming default color as theme is not used
    display: 'flex',
    alignItems: 'center',
    padding: '2px 4px',
    maxWidth: 400,
    margin: 'auto',
});

const StyledSearchInput = styled(InputBase)({
    marginLeft: 8, // Assuming default spacing as theme is not used
    flex: 1,
});

const StyledSearchIconButton = styled(IconButton)({
    padding: 10,
});

function AnimeCard() {
    const [title, setTitle] = useState('');
    const [recommendations, setRecommendations] = useState<string[]>([]);
    const [selectedRecommendation, setSelectedRecommendation] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showDropdown, setShowDropdown] = useState(false);

    const fetchRecommendations = async () => {
        setIsLoading(true);
        try {
            const response = await fetch('http://localhost:5000/recommendations', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title })
            });
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            setRecommendations(data);
            setShowDropdown(true);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setTitle(event.target.value);
        if (event.target.value.trim() !== '') {
            fetchRecommendations();
        } else {
            setShowDropdown(false);
            setRecommendations([]);
        }
    };

    return (
        <Box className="mt-10 mx-auto max-w-md shadow-lg" style={{ textAlign: 'center' }}>
    <Typography variant="h5" gutterBottom component="div" style={{ margin: '20px 0' }}>
    Anime Recommendations
    </Typography>
    <form onSubmit={(event) => event.preventDefault()} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
    <StyledSearchBar elevation={1}>
    <StyledSearchInput
        placeholder="Enter Anime Title"
    inputProps={{ 'aria-label': 'search anime' }}
    value={title}
    onChange={handleInputChange}
    />
    <StyledSearchIconButton type="submit" aria-label="search">
        <SearchIcon />
        </StyledSearchIconButton>
        </StyledSearchBar>
        </form>
    {showDropdown && recommendations.length > 0 && (
        <Box className="p-4">
        <Typography variant="h6" component="div">
        Select a recommendation:
        </Typography>
        <Select
        label="Recommendations"
        value={selectedRecommendation}
        onChange={(e) => setSelectedRecommendation(e.target.value)}
        displayEmpty
        fullWidth
        >
        {recommendations.map((anime, index) => (
                <MenuItem key={index} value={anime}>{anime}</MenuItem>
    ))}
        </Select>
        </Box>
    )}
    {isLoading && (
        <Typography variant="body2" style={{ textAlign: 'center' }}>
        Loading...
        </Typography>
    )}
    </Box>
);
}

export default AnimeCard;

