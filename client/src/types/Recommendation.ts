import { Song } from './Song';

export class Recommendation extends Song {
    votes: string[];

    constructor(data: Recommendation) {
        super(data);
        this.votes = data.votes;
    }
}