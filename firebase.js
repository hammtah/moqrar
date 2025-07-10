import { initializeApp } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js";
import { getFirestore, collection, addDoc, getDocs, query, where, updateDoc, doc } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyBlOzHz5n2qieJXKudYh-zwMlVCcc7Iorg",
  authDomain: "moqrar-a349a.firebaseapp.com",
  projectId: "moqrar-a349a",
  storageBucket: "moqrar-a349a.firebasestorage.app",
  messagingSenderId: "993635124177",
  appId: "1:993635124177:web:5245aa3da3a772dabd56f0"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

  async function saveData(moqrar) {
    //moqrar example:
    //{
    //     name: "رقائق القرآن (٣٥ - ٦٦)",
    //     url: "pages/10-07-2025/index.html",
    //     image: "pages/10-07-2025/images/cover.jpg",
    //     date: "10-07-2025",
    //     completed: false,
    //     progress: 0.4134522133583607
    //   }
    console.log('clicked');
    try {
      const docRef = await addDoc(collection(db, "moqrarat"), moqrar);
      console.log("Document written with ID: ", docRef.id);
    } catch (e) {
      console.error("Error adding document: ", e);
    }
  }

// Optionally, you can add a loadData function here as well
async function loadData() {
  const querySnapshot = await getDocs(collection(db, "moqrarat"));
  // querySnapshot.forEach((doc) => {
  //   console.log(doc.id, " => ", doc.data());
  // });
  console.log(querySnapshot)
  renderMoqrarat(querySnapshot);
}

function renderMoqrarat(data){
  const container = document.querySelector('.container');
  let renderString = '';
  data.forEach((item) => {
      item = item.data();
      renderString += `
    <a class="card" href="${item.url || ''}">
      <span class="card-date badge">${item.date}</span>
      <img class="card-image" src="${item.image || 'raqaiq_5_35/رقائق القرآن_cover.jpg'}" alt="cover">
      <h2 class="card-title">${item.name}</h2>
      <span class="badge-completed${item.completed ? '' : ' hidden'}">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-check"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M5 12l5 5l10 -10" /></svg>
      </span>
      <div class="progress-bar-container">
        <div class="progress-bar" style="width: ${(item.progress * 100) || 0}%;"></div>
      </div>
    </a>
  `
});
container.innerHTML = renderString;
}

async function updateProgress(progress, date) {
    const db = getFirestore();
    // Query for the document with the matching date
    const q = query(collection(db, "moqrarat"), where("date", "==", date));
    const querySnapshot = await getDocs(q);
    if (querySnapshot.empty) {
        console.warn('No document found with date:', date);
        return;
    }
    // Update all matching documents (should be only one)
    for (const document of querySnapshot.docs) {
        await updateDoc(doc(db, "moqrarat", document.id), { progress });
    }
}

async function getMoqrar(date){
    const db = getFirestore();
    const q = query(collection(db, "moqrarat"), where("date", "==", date));
    const querySnapshot = await getDocs(q);
    if (querySnapshot.empty) {
        console.warn('No document found with date:', date);
        return null;
    }
    // Return the first matching document
    return querySnapshot.docs[0].data();
}
export { saveData, loadData, renderMoqrarat, updateProgress, getMoqrar };
// loadData();
// document.getElementById('save').addEventListener('click', saveData);
