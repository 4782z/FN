import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyCAveRa2jgcg2o2K1upuRorm9AzU707C0M",
    authDomain: "fakenewsdetector-ab648.firebaseapp.com",
    projectId: "fakenewsdetector-ab648",
    storageBucket: "fakenewsdetector-ab648.firebasestorage.app",
    messagingSenderId: "298853783575",
    appId: "1:298853783575:web:0026e83afc0e539ddb2452"
  };
  
// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
