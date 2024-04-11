import random
import pandas as pd
from helper import *


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
                    repeat
                    priority
                    private
                    notes
                    startedAt {
                        year
                        month
                        day
                    }
                    completedAt {
                        year
                        month
                        day
                    }
                    updatedAt
                    createdAt
                }
            }
        }
    }
    """ % (user_id, type)


visited_pages = pd.read_csv("../ScrapedData/visited_user_pages.csv", header=None, names=(['page']))["page"]


def user_collecting_query():
    global visited_pages

    while True:
        page = random.randint(0, 49648 + 1)
        if page not in visited_pages:
            write_row_to_csv("../ScrapedData/visited_user_pages.csv", [page])
            break

    return """
    {
        Page(page: %d, perPage: 50) {
            users {
                id
                statistics {
                    anime {
                        count
                        episodesWatched
                        minutesWatched
                    }
                }
                siteUrl
            }
        }
    }
    """ % page


def user_query(user_id):
    return """
    {
    User(id: %d) {
        id
        name
        about
        avatar {
            large
            medium
        }
        bannerImage
        bans
        options {
            titleLanguage
            displayAdultContent
            airingNotifications
            profileColor
            timezone
            activityMergeTime
            staffNameLanguage
        }
        mediaListOptions {
            scoreFormat
        }
        statistics {
            anime {
                count
                meanScore
                standardDeviation
                minutesWatched
                episodesWatched
                chaptersRead
                volumesRead
            }
            manga {
                count
                meanScore
                standardDeviation
                minutesWatched
                episodesWatched
                chaptersRead
                volumesRead
            }
        }
        siteUrl
        createdAt
        updatedAt
    }
}
    """ % user_id


def big_user_query(user_id):
    return """
    {
    User(id: %d) {
        id
        name
        about
        avatar {
            large
            medium
        }
        bannerImage
        bans
        options {
            titleLanguage
            displayAdultContent
            airingNotifications
            profileColor
            timezone
            activityMergeTime
            staffNameLanguage
        }
        mediaListOptions {
            scoreFormat
        }
        favourites {
            anime {
                edges {
                    favouriteOrder
                }
                nodes {
                    id
                }
            }
            manga {
                edges {
                    favouriteOrder
                }
                nodes {
                    id
                }
            }
            characters {
                edges {
                    favouriteOrder
                }
                nodes {
                    id
                }
            }
            staff {
                edges {
                    favouriteOrder
                }
                nodes {
                    id
                }
            }
            studios {
                edges {
                    favouriteOrder
                }
                nodes {
                    id
                }
            }
        }
        statistics {
            anime {
                count
                meanScore
                standardDeviation
                minutesWatched
                episodesWatched
                chaptersRead
                volumesRead
                formats(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    format
                }
                statuses(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    status
                }
                scores(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    score
                 }
                lengths(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    length
                }
                releaseYears(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    releaseYear
                }
                startYears(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    startYear
                }
                genres(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    genre
                }
                tags(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    tag {
                        id
                    }
                }
                countries(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    country
                }
                voiceActors(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    voiceActor {
                        id
                    }
                }
                staff(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    staff {
                        id
                    }
                }
                studios(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    studio {
                        id
                    }
                }
            }
            manga {
                count
                meanScore
                standardDeviation
                minutesWatched
                episodesWatched
                chaptersRead
                volumesRead
                formats(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    format
                }
                statuses(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    status
                }
                scores(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    score
                }
                lengths(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    length
                }
                releaseYears(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    releaseYear
                }
                startYears(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    startYear
                }
                genres(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    genre
                }
                tags(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    tag {
                        id
                    }
                }
                countries(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    country
                }
                voiceActors(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    voiceActor {
                        id
                    }
                }
                staff(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    staff {
                        id
                    }
                }
                studios(sort: COUNT_DESC) {
                    count
                    meanScore
                    minutesWatched
                    chaptersRead
                    studio {
                        id
                    }
                }
            }
        }
        siteUrl
        createdAt
        updatedAt
    }
}
    """ % user_id



