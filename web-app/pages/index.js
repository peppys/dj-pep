import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import ListItemText from '@material-ui/core/ListItemText';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import Head from 'next/head'
import { parsePhoneNumberFromString } from 'libphonenumber-js';
import React, { useEffect, useState } from 'react';
import moment from 'moment-timezone';

import db from '../firestore';

import CustomMusicPlayer from '../components/player';

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

export default function Index() {
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
  const phoneNumber = parsePhoneNumberFromString(process.env.REACT_APP_PHONE_NUMBER).formatNational();

  return (
    <>
      <Head>
        <title>DJ PEP</title>
        <link rel="shortcut icon" href="/favicon.ico"/>
        <meta name="viewport" content="initial-scale=1.0, width=device-width"/>
        <meta
          name="description"
          content="Hate your DJ? DJ Pep has your back. Text your favorite songs to the phone number displayed, and DJ Pep will starting playing each song."
        />
      </Head>
      <div className="App">
        <h1> DJ PEP </h1>
        <h2>🎤🎶 TEXT SONGS TO {phoneNumber} 🎤🎶 </h2>
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
              <ListItem key={song.id} alignItems="flex-start">
                <ListItemAvatar>
                  <Avatar alt="Remy Sharp" src={song.image_url}/>
                </ListItemAvatar>
                <ListItemText
                  primary={song.name}
                  secondary={
                    <>
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
                    </>
                  }
                />
              </ListItem>
            ))}
            <Divider variant="inset" component="li"/>
          </List>
        </div>
      </div>
    </>
  );
}
