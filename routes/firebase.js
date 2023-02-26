import {initializeApp} from "firebase/app"
import {getAuth, GoogleAuthProvider, signInWithRedirect, signOut, getRedirectResult, signInWithPopup} from "firebase/auth"

const firebaseConfig = {
    // apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
    // authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
    // databaseURL: process.env.REACT_APP_FIREBASE_DATABASE_URL,
    // projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
    // storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
    // messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
    // appId: process.env.REACT_APP_FIREBASE_APP_ID
    // For Firebase JS SDK v7.20.0 and later, measurementId is optional

    apiKey: "AIzaSyDLLwblV5x0tf9ho-HOhLsk0pMv-6FrcMM",
    authDomain: "hackathon-1c1a9.firebaseapp.com",
    projectId: "hackathon-1c1a9",
    storageBucket: "hackathon-1c1a9.appspot.com",
    messagingSenderId: "585777228268",
    appId: "1:585777228268:web:9b0f62c3773ed77ff9b8c9",
    measurementId: "G-PV5T99PE4G"
  
  }

const app = initializeApp(firebaseConfig)
const auth = getAuth(app)

const googleProvider = new GoogleAuthProvider(); 

const signInWithGoogle = async () => {
    try{
        const res = await signInWithPopup(auth, googleProvider)

    }catch(err){
        console.log(err);
        alert(err.message)
    }

}

const logout =() => {
    signOut(auth);
}

export {signInWithGoogle, auth, logout}; 
