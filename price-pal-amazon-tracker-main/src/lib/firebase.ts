// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyD7iee5Hu0vKe3MlzativB_DwdbGmTbFPg",
  authDomain: "price-tracker-appdb.firebaseapp.com",
  databaseURL: "https://price-tracker-appdb-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "price-tracker-appdb",
  storageBucket: "price-tracker-appdb.firebasestorage.app",
  messagingSenderId: "211860055283",
  appId: "1:211860055283:web:6859717b4178d092970386",
  measurementId: "G-ZWFJE2FRLG"
};

// Initialize Firebase
import { getAuth } from "firebase/auth";
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
export const auth = getAuth(app);