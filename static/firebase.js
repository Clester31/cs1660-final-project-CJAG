firebase.initializeApp(config);

// Watch for state change from sign in
function initApp() {
  firebase.auth().onAuthStateChanged(user => {
    const signInButton = document.getElementById('signInButton');
    if (user) {
      // User is signed in.
      signInButton.innerText = 'Sign Out';
      document.getElementById('form').style.display = '';
    } else {
      // No user is signed in.
      signInButton.innerText = 'Sign In with Google';
      document.getElementById('form').style.display = 'none';
    }
  });
}

// check if authentication is disabled via query parameter
function authDisabled() {
  const urlParams = new URLSearchParams(window.location.search);
  const hostname = window.location.hostname;
  // Auth is disabled only if running on localhost and `auth=false` is passed
  return urlParams.get('auth') === 'false' && hostname === 'localhost';
}

window.onload = function () {
  if (authDisabled()) {
    console.warn('Running with auth disabled.');
    document.getElementById('signInButton').innerText = '(Auth Disabled)';
    document.getElementById('form').style.display = '';
  } else {
    console.log('Running with auth enabled.');
    initApp();
  }
};

function signIn() {
  const provider = new firebase.auth.GoogleAuthProvider();
  provider.addScope('https://www.googleapis.com/auth/userinfo.email');
  provider.addScope('https://www.googleapis.com/auth/contacts.readonly');
  firebase
    .auth()
    .signInWithPopup(provider)
    .then(result => {
      // get the google access token for use with Google People API
      const credential = result.credential;
      const accessToken = credential.accessToken; 
      //add the access token to local storage so we can use it after refresh
      localStorage.setItem('accessToken', accessToken);
      console.log('local storage token:', localStorage.getItem('GPToken'));

      // Returns the signed in user along with the provider's credential
      console.log(`${result.user.displayName} logged in.`);
      window.alert(`${result.user.displayName} has signed in`);
    })
    .catch(err => {
      console.log(`Error during sign in: ${err.message}`);
      window.alert(`Sign in failed. Retry or check your browser logs.`);
    });
    //window.location.reload();
}

function signOut() {
  firebase
    .auth()
    .signOut()
    .then(() => {
      localStorage.removeItem('accessToken');
    })
    .catch(err => {
      console.log(`Error during sign out: ${err.message}`);
      window.alert(`Sign out failed. Retry or check your browser logs.`);
    });
}

// Toggle Sign in/out button
function toggle() {
  if (authDisabled()) {
    //window.alert('Auth is disabled.');
    return;
  }
  if (!firebase.auth().currentUser) {
    signIn();
  } else {
    signOut();
  }
  window.location.reload();
}

/**
 * Sends the user's vote to the server.
 * @param team
 * @returns {Promise<void>}
 */
async function attendance() {
  console.log("tracking attendance")
  if (firebase.auth().currentUser || authDisabled()) {
    try {
      const token = localStorage.getItem('accessToken');

      //fetch name from google people api
      const res = await fetch('https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const profile = await res.json();
      const name = profile.names?.[0]?.displayName;

      console.log('profile: ', profile);
      console.log('name: ', name);

      const response = await fetch('/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': `Bearer ${token}`
        },
        body: `name=${encodeURIComponent(name)}`
      });


      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }

      const data = await response.json();

      window.location.reload();

    } catch (err) {
      console.log(`Error taking attendance: ${err}`);
      window.alert('There was an error taking your attendance. Try again');
    }
  } else {
    window.alert('User not signed in.');
  }
}
