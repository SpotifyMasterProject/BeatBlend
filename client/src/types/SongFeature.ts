export enum SongFeatureCategory {
    TEMPO,
    ENERGY,
    VALENCE,
    DANCEABILITY,
    SPEECHINESS
};

export interface SongFeature {
    readonly category: SongFeatureCategory;
    readonly value: number;
};