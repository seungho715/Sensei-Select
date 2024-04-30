import React, { useState } from 'react';
import { TextField, Typography, Box, Autocomplete, Popper, PopperProps } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { styled } from '@mui/material/styles';
import Papa from 'papaparse';

const StyledSearchBar = styled(Box)(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    padding: theme.spacing(1),
    maxWidth: 305,
    margin: 'auto',
    backgroundColor: theme.palette.background.paper,
    borderRadius: theme.shape.borderRadius,
}));

interface Anime {
    id: string;
    title: string;
    url: string;  // Include this if you need to use URLs from your CSV
}


function AnimeCard() {
    const [title, setTitle] = useState<string>('');
    const [recommendations, setRecommendations] = useState<Anime[]>([]);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files ? event.target.files[0] : null;
        if (file) {
            const reader = new FileReader();
            reader.onload = (e: ProgressEvent<FileReader>) => {
                const text = e.target?.result as string | null;
                if (text) {
                    Papa.parse<Anime>(text, {
                        header: true,
                        complete: (results) => {
                            const animes = results.data
                                .filter(item => item.type === 'ANIME' && item.format === 'MOVIE')
                                .map(item => ({
                                    id: item.id,
                                    title: item.title_english,
                                    url: item.url
                                }));
                            setRecommendations(animes);
                        }
                    });
                }
            };
            reader.readAsText(file);
        }
    };

    // const handleSelection = async (selectedId: string) => {
    //     try {
    //         const response = await fetch('http://your-backend-url/api', {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //             },
    //             body: JSON.stringify({ id: selectedId })
    //         });
    //         if (!response.ok) {
    //             throw new Error(`HTTP error! status: ${response.status}`);
    //         }
    //         const data = await response.json();
    //         console.log('Response data:', data);
    //         // Assuming data is an array of { id: string, title: string }
    //         const relatedIds = data.map(item => item.id);
    //         const relatedAnimes = recommendations.filter(anime => relatedIds.includes(anime.id));
    //         console.log('Related Animes:', relatedAnimes);
    //     } catch (error) {
    //         console.error('Failed to fetch:', error);
    //     }
    // };


    // Custom Popper that forces the dropdown to always open downwards
    const CustomPopper = (props: PopperProps) => (
        <Popper {...props} placement="bottom-start" />
    );

    return (
        <Box className="mt-10 mx-auto max-w-md shadow-lg" style={{ textAlign: 'center' }}>
            <Typography variant="h5" gutterBottom component="div" style={{ margin: '20px 0' }}>
                Anime Movie Recommendations
            </Typography>
            <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                style={{ display: 'block', margin: '10px auto' }}
            />
            <StyledSearchBar>
                <Autocomplete
                    freeSolo
                    disableClearable
                    options={recommendations}
                    getOptionLabel={(option) => option.title}  // Map option to title for display
                    value={title}
                    onChange={(event, newValue) => {
                        if (typeof newValue === 'string') {
                            setTitle(newValue);
                            const selectedAnime = recommendations.find(anime => anime.title === newValue);
                            if (selectedAnime) {
                                handleSelection(selectedAnime.id);
                            }
                        } else if (newValue && 'title' in newValue) {
                            setTitle(newValue.title);
                            handleSelection(newValue.id);
                        }
                    }}
                    onInputChange={(event, newInputValue) => {
                        setTitle(newInputValue);
                    }}
                    renderInput={(params) => (
                        <TextField
                            {...params}
                            label="Search Anime"
                            margin="normal"
                            variant="outlined"
                            sx={{ width: 300 }}
                            InputProps={{
                                ...params.InputProps,
                                type: 'search',
                                endAdornment: <SearchIcon />
                            }}
                        />
                    )}
                    PopperComponent={CustomPopper}
                />



            </StyledSearchBar>
        </Box>
    );
}

export default AnimeCard;
