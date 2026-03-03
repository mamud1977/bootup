function myFunction() {
    console.log("Button clicked!");
}

function loadPage(pageName) {
    const workpage = document.getElementById('workpage');
    // Simulate refreshing content
    workpage.innerHTML = `
    <h2>${pageName} Page</h2>
    <p>Content for ${pageName} goes here...</p>
    `;
}

function loadHTML(pageFile) {
    const workpage = document.getElementById('workpage');
    fetch(pageFile)                // fetch the HTML file
        .then(response => response.text())
        .then(html => { workpage.innerHTML = html; })
        .catch(err => {
            workpage.innerHTML = `<p style="color:red;">Error loading ${pageFile}</p>`;
            console.error(err);
        });
}

function setLanguage(langCode) {
    console.log(`Language selected ${langCode}`);
    const map = {
        en: "english",
        hi: "hindi",
        bn: "bengali"
    };
    ime.setLanguage(map[langCode] || "english");
}


/*----------------- */

function getEvent_test() {

    alert('Hello')

}

