import React, {useEffect, useState} from 'react';
import {parsePhoneNumberFromString} from 'libphonenumber-js'
import moment from 'moment-timezone';

import {makeStyles} from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Divider from '@material-ui/core/Divider';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import Typography from '@material-ui/core/Typography';

import CustomMusicPlayer from './components/player'

import db from './firestore';

import './App.css';

const SongStatus = {
    Queued: 'QUEUED',
    Playing: 'PLAYING',
    Played: 'PLAYED',
};

const useStyles = makeStyles(theme => ({
    root: {
        width: '100%',
        maxWidth: 360,
    },
    inline: {
        display: 'inline',
    },
}));

const App = () => {
    const [songs, setSongs] = useState([]);
    const [playingSong, setSongToPlay] = useState(null);
    const classes = useStyles();

    useEffect(() => {
        db.collection('songs')
            .where('status', 'in', [SongStatus.Queued, SongStatus.Playing])
            .onSnapshot(snapshot => {
                const songs = snapshot.docs
                    .map(doc => ({
                        id: doc.id,
                        ...doc.data(),
                    }))
                    .sort((a, b) => moment(a.added_at).unix() - moment(b.added_at).unix());

                const songToPlay = songs.find(({status}) => status === SongStatus.Playing);
                if (songToPlay) {
                    setSongToPlay({
                        progress: 5,
                        id: songToPlay.id,
                        status: songToPlay.status,
                        url: songToPlay.preview_url,
                        cover: songToPlay.image_url,
                        title: songToPlay.name,
                        artist: [
                            ...songToPlay.artists.map(artist => artist.name),
                            `Added by ${songToPlay.added_by_name || parsePhoneNumberFromString(songToPlay.added_by).formatNational()}`,
                        ],
                    })
                } else {
                    setSongToPlay(null)
                }

                setSongs(songs)
            });
    }, []);

    const audioContainerRef = React.createRef();

    return (
        <div className="App">
            <h1> DJ PEP </h1>
            <h2>🎤🎶 TEXT SONGS TO (857) 401-8177 🎤🎶 </h2>
            <div>
                {playingSong && <CustomMusicPlayer
                    playlist={[playingSong]}
                    mode={'vertical'}
                    playMode={'loop'}
                    autoplay={true}
                    audioContainer={audioContainerRef}
                    style={{marginLeft: 'auto', marginRight: 'auto'}}
                />}
                <List className={classes.root} style={{marginLeft: 'auto', marginRight: 'auto'}}>
                    {songs.filter(song => song.status === SongStatus.Queued).map(song => (
                        <ListItem alignItems="flex-start">
                            <ListItemAvatar>
                                <Avatar alt="Remy Sharp" src={song.image_url}/>
                            </ListItemAvatar>
                            <ListItemText
                                primary={song.name}
                                secondary={
                                    <React.Fragment>
                                        <Typography
                                            component="span"
                                            variant="body2"
                                            className={classes.inline}
                                            color="textPrimary"
                                        >
                                            {song.artists.map(artist => artist.name).join(', ')}
                                        </Typography>
                                        <span style={{marginLeft: '10px'}}>
                                        {`Added by ${song.added_by_name || parsePhoneNumberFromString(song.added_by).formatNational()} - ${moment.duration(moment().diff(moment(song.added_at))).humanize()} ago`}
                                        </span>
                                    </React.Fragment>
                                }
                            />
                        </ListItem>
                    ))}
                    <Divider variant="inset" component="li"/>
                </List>
            </div>
        </div>
    );
};


export default App;
