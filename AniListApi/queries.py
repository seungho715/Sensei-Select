
def media_info_query(show_id):
    return """
    {
        Media(id: %d) {
            id
            title {
                romaji
                english
                native
                userPreferred
            }
            type
            format
            status
            description
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            season
            seasonYear
            seasonYear
            seasonInt
            episodes
            duration
            chapters
            volumes
            countryOfOrigin
            isLicensed
            source
            hashtag
            trailer {
                id
                site
                thumbnail
            }
            updatedAt
            coverImage {
                extraLarge
                large
                medium
                color
            }
            bannerImage
            genres
            synonyms
            averageScore
            meanScore
            popularity
            isLocked
            trending
            favourites
            tags {
                id
                rank
                isMediaSpoiler
            }
            relations {
                edges {
                    node {
                        id
                    }
                    relationType
                }
            }
            characters {
                edges {
                    node {
                        id
                        name {
                            full
                            native
                        }
                    }
                    id
                    role
                    name
                    voiceActorRoles {
                        voiceActor {
                            id
                        }
                        roleNotes
                        dubGroup
                    }
                }
            }
            staff {
                edges {
                    node {
                        id
                    }
                    role
                }
            }
            studios {
                edges {
                    isMain
                    node {
                        id
                    }
                }
            }
            isAdult
            siteUrl
            modNotes
        }
    }
    """ % show_id


def media_list_query(user_id, type):
    return """
    {
        MediaListCollection(userId: %d, type: %s) {
            lists {
                entries {
                    media {
                        id
                        relations {
                            edges {
                                node {
                                    id
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """ % (user_id, type)


def media_tag_collection_query():
    return """
    {
        MediaTagCollection {
            id
            name
            description
            category
            isGeneralSpoiler
            isAdult
        }
    }
    """


def staff_info_query(staff_id):
    return """
    {
        Staff(id: %d) {
            id
            name {
                first
                middle
                last
                full
                native
                alternative
            }
            languageV2
            image {
                large
                medium
            }
            description
            primaryOccupations
            gender
            dateOfBirth {
                year
                month
                day
            }
            dateOfDeath {
                year
                month
                day
            }
            yearsActive
            homeTown
            bloodType
            siteUrl
            favourites
            modNotes
        }
    }
    """ % staff_id


def character_info_query(character_id):
    return """
    {
        Character(id: %d) {
            id
            name {
                first
                middle
                last
                full
                native
                alternative
                alternativeSpoiler
            }
            image {
                large
                medium
            }
            description
            gender
            dateOfBirth {
                year
                month
                day
            }
            age
            bloodType
            siteUrl
            favourites
            modNotes
        }
    }
    """ % character_id


def studio_query(studio_id):
    return """
    {
        Studio(id: %d) {
            id
            name
            isAnimationStudio
            siteUrl
            favourites
        }
    }
    """ % studio_id


def genre_collection_query():
    return """
    {
        GenreCollection
    }
    """


def media_stats_query(show_id):
    return """
    {
        Media(id: %d) {
            stats {
                scoreDistribution {
                    score
                    amount
                }
                statusDistribution {
                    status
                    amount
                }
            }
        }  
    }
    """ % show_id


def meda_list_detail_query(user_id, type):
    return """
    {
        MediaListCollection(userId: %d, type: %s) {
            lists {
                name
                entries {
                    media {
                        id
                    }
                    status
                    score
                    progress
                    progressVolumes
                }
            }
        }
    }
    """ % (user_id, type)



