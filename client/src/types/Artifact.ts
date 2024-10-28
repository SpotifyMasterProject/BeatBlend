class AverageFeatures {
    danceability: number;
    energy: number;
    speechiness: number;
    valence: number;
    tempo: number;

    constructor(data: AverageFeatures) {
        this.danceability = danceability;
        this.energy = energy;
        this.speechiness = speechiness;
        this.valence = valence;
        this.tempo = tempo;
    }
}

class Artifacts {
    songsPlayed: number;
    songsAddedManually: number;
    mostSongsAddedBy: string;
    mostVotesBy: string;
    mostSignificantFeatureOverall: string;
    firstRecommendationVotePercentage: number;
    averageFeatures: AverageFeatures;
    genreStart: string[];
    genreEnd: string[];

    constructor(data: Artifacts) {
        this.songsPlayed = songsPlayed;
        this.songsAddedManually = songsAddedManually;
        this.mostSongsAddedBy = mostSongsAddedBy;
        this.mostVotesBy = mostVotesBy;
        this.mostSignificantFeatureOverall = mostSignificantFeatureOverall;
        this.firstRecommendationVotePercentage = firstRecommendationVotePercentage;
        this.averageFeatures = averageFeatures;
        this.genreStart = genreStart;
        this.genreEnd = genreEnd;
    }
}