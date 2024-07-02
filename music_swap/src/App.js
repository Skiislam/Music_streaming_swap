import './App.css';
import authorize from './scripts/authorize.js'
import {useEffect, useState} from "react"
function App() {
  
  const [token, setToken] = useState("")

  useEffect(() => {
    const hash = window.location.hash
    let token = window.localStorage.getItem('token')
    if(!token && hash){
      token = hash.substring(1).split('&').find(elem => elem.startsWith('access_token')).split('-')[1]

      window.location.hash = ''
      window.localStorage.setItem('token', token)
      setToken(token)
    }
  }, [])

  return (
    <div className="App">
      <h2> Welcome to Song Swap</h2>
      
      <button onClick = {authorize}>Login into Spotify</button>

    </div>
  );
}

export default App;
