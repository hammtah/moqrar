// Add data to "articles" collection
function saveData() {
    db.collection("moqrarat").add({
        name: " رقائق القرآن  ٣٥ - ٥ ",
        url: "pages/2025-07-09/index.html",
        image: "pages/2025-07-09/images/cover.jpg",
        date: "2025-07-09",
        completed: false,
        progress: 0.45
    })
    .then((docRef) => {
      console.log("Document written with ID: ", docRef.id);
    })
    .catch((error) => {
      console.error("Error adding document: ", error);
    });
  }
  