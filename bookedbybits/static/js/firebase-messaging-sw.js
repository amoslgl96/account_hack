importScripts('https://www.gstatic.com/firebasejs/5.0.4/firebase-app.js')
importScripts('https://www.gstatic.com/firebasejs/5.0.4/firebase-messaging.js')
var config = {
    apiKey: "AIzaSyAlY08ZLM3nyXNFHo8oH8FMaCHbQ_UBSTQ",
    authDomain: "bookedbybits.firebaseapp.com",
    databaseURL: "https://bookedbybits.firebaseio.com",
    projectId: "bookedbybits",
    storageBucket: "bookedbybits.appspot.com",
    messagingSenderId: "586068157501"
  };
  firebase.initializeApp(config);
  const messaging = firebase.messaging()