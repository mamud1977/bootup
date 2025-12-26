function displayAlert() {
    alert('Hello World!');
}

function addTimestamp() {
    // Get current date-time
    const now = new Date();
    const formatted = now.toLocaleString(); // e.g., "23/11/2025, 11:25:30 pm"

    // Create new list item
    const li = document.createElement("li");
    li.textContent = formatted;

    // Append to ordered list
    document.getElementById("timestampList").appendChild(li);
}
