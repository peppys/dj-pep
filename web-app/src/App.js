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
    const [songToPlay, setSongToPlay] = useState(null);
    const classes = useStyles();

    useEffect(() => {
        db.collection('song_queue')
            .onSnapshot(snapshot => {
                const songs = snapshot.docs
                    .map(doc => ({
                        id: doc.id,
                        ...doc.data(),
                    }));

                setSongs(songs)
            });
    }, []);


    const audioContainerRef = React.createRef();
    useEffect(() => {
        const syncSongState = async () => {
            if (!songToPlay) {
                const nextSongToPlay = songs
                    .map(song => ({
                        id: song.id,
                        status: song.status,
                        url: song.preview_url,
                        cover: song.image_url,
                        title: song.name,
                        artist: [
                            ...song.artists.map(artist => artist.name),
                            `Added by ${parsePhoneNumberFromString(song.added_by).formatNational()}`,
                        ],
                    }))
                    .find(song => song.status === SongStatus.Queued);

                console.log(`Found next song to play`, nextSongToPlay)

                setSongToPlay(nextSongToPlay);
            }

            if (audioContainerRef.current) {
                audioContainerRef.current.addEventListener('timeupdate', async () => {
                    const currentlyPlayingSong = songs
                        .find(song => song.status === SongStatus.Queued && song.preview_url === audioContainerRef.current?.src);

                    console.log(`Song playing:`, currentlyPlayingSong);

                    if (currentlyPlayingSong) {
                        await db.collection('song_queue')
                            .doc(currentlyPlayingSong.id)
                            .update({
                                status: SongStatus.Playing,
                            });
                    }
                })
            }

            if (audioContainerRef.current) {
                audioContainerRef.current.addEventListener('ended', async () => {
                    setSongToPlay(null)

                    console.log(`Song ended:`, songToPlay);

                    await db.collection('song_queue')
                        .doc(songToPlay.id)
                        .update({
                            status: SongStatus.Played,
                        });
                })
            }
        };

        syncSongState()
    }, [audioContainerRef, songs, songToPlay])

    return (
        <div className="App">
            <h1> DJ PEP </h1>
            <h2>🎤🎶 TEXT SONGS TO (857) 401-8177 🎤🎶 </h2>
            <div>
                {songToPlay && <CustomMusicPlayer
                    playlist={[songToPlay]}
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
                                        {`Added by ${parsePhoneNumberFromString(song.added_by).formatNational()} - ${moment(song.added_at).subtract(moment()).seconds()} seconds ago`}
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
