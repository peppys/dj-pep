import MusicPlayer from 'react-responsive-music-player'

export default class CustomMusicPlayer extends MusicPlayer {
    constructor(props) {
        super(props);

        if (props.audioContainer) {
            this.audioContainer = props.audioContainer
        }
    }
}
