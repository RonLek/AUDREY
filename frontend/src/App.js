import {React, useState} from 'react';
import { makeStyles } from '@mui/styles';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Avatar from '@mui/material/Avatar';
import Fab from '@mui/material/Fab';
import SendIcon from '@mui/icons-material/Send';
import Audrey from './audrey.png';
import './App.css';
import axios from 'axios';


const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
  chatSection: {
    width: '100%',
    height: '80vh'
  },
  headBG: {
      backgroundColor: '#e0e0e0'
  },
  borderRight500: {
      borderRight: '1px solid #e0e0e0'
  },
  messageArea: {
    height: '70vh',
    overflowY: 'auto'
  }
});



const App = () => {
  const classes = useStyles();
  const [messages, setMessages] = useState(["hello", "how are you?"]);
  const [inputMessage, setInputMessage] = useState("");
  const [loading, setLoading] = useState(false);


  const _handleChange = (e) => {
    setInputMessage(e.target.value);
  }

  const keyPress = (e) => {
    if(e.keyCode == 13){
      setMessages([...messages, inputMessage]);
      setLoading(true);
      axios.post(`http://localhost:5000/message`, { message: inputMessage })
      .then(res => {
        console.log(res);
        console.log(res.data);
        setMessages([...messages, inputMessage, res.data]);
        setLoading(false);
      })
      setInputMessage("");
    }
  }

  const handleAddMessage = () => {
    setMessages([...messages, inputMessage]);
    setInputMessage("");
  }

  return (
      <div>
        <Grid container>
            <Grid item xs={12}>
                <Typography style={{textAlign: "center"}} variant="h5" className="header-message">AUDREY: UMass Dining Assistant</Typography>
            </Grid>
        </Grid>
        <Grid container component={Paper} elevation={0} className={classes.chatSection}>
            <Grid item xs={12}>
                <List className={classes.messageArea}>
                  <Divider/>
                {messages.map((message, index) => (
                  <>
                    <ListItem style={{padding: "30px"}} key={index}>
                        <Grid container flexDirection={(index % 2 == 0 ? "row-reverse": "row")} alignItems="center">
                            
                              {index % 2 == 0 ? 
                                <Grid item style={{marginLeft: "20px"}}>
                                  <Avatar alt="Rohan Lekhwani"/> 
                                </Grid>
                                  :
                                <Grid item style={{marginRight: "20px"}}>
                                  <Avatar alt="Audrey" src={Audrey}/>
                                </Grid>
                                  }
                             
                            <Grid item xs={8}>
                                <p align={(index % 2 == 0 ? "right": "left")}>{message}</p>
                            </Grid>
                        </Grid>
                    </ListItem>
                    <Divider/>
                    </>

                ))}
                {loading ?
                  <ListItem style={{padding: "30px"}}>
                    <Grid container flexDirection="row" alignItems="center">
                      <Grid item style={{marginRight: "20px"}}>
                        <Avatar alt="Audrey" src={Audrey}/>
                      </Grid>
                      <Grid item xs={8}>
                        <h3 className='loading'/>
                      </Grid>
                    </Grid>
                  </ListItem>
                  :
                  <></>
                }
                </List>
                <Grid container style={{padding: '20px'}}>
                    <Grid item xs={11}>
                        <TextField id="outlined-basic-email" label="Ask me for lunch options at Worcester" 
                          fullWidth onChange={_handleChange} onKeyDown={keyPress} value={inputMessage}/>
                    </Grid>
                    <Grid xs={1} align="right">
                        <Fab color="primary" aria-label="add" onClick={handleAddMessage}><SendIcon /></Fab>
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
      </div>
  );
}

export default App;