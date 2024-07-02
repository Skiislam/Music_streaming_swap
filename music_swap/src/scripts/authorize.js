const CLIENT_ID = process.env.REACT_APP_CLIENT_ID;
  const CLIENT_SECRET = process.env.REACT_APP_CLIENT_SECRET
  const REDIRECT_URI = 'http://localhost:3000/callback'
  const AUTH_ENDPOINT = 'https://accounts.spotify.com/authorize'

function authorize()
 { let url = AUTH_ENDPOINT;
  url +='?response_type=token';
  url +='&client_id=' + CLIENT_ID;
  url +='&scope= user-read-email user-read-private playlist-read-private playlist-read-collaborative' 
  url +='&redirect_uri=' + encodeURI(REDIRECT_URI);
  url +='&show_dialog=true';
  window.location.href = url
}
export default authorize;