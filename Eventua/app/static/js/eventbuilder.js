// Mark form as dirty and show "Save your changes"
let isDirty = false;


// Mark form as dirty
function markDirty() {
    if (!isDirty) {
        isDirty = true;
        const status = document.getElementById("eventStatus");
        status.innerText = "Save your changes";
        status.style.color = "red";
    }
}

// Mark form as clean after successful save
function markClean() {
    isDirty = false;
    const status = document.getElementById("eventStatus");
    status.innerText = "Successfully saved";
    status.style.color = "green";
}


// Attach input event listener to mark dirty + update preview
function attachInputEvents(input) {
    input.addEventListener("input", () => {
        markDirty();
        updatePreview();
    });
}

// Add a node (root or child)
// Add a node
function addNode(containerId, parentId = null) {
    const container = document.getElementById(containerId);

    const nodeDiv = document.createElement("div");
    nodeDiv.className = "node";

    let nodeId;
    if (!parentId) {
        const roots = document.querySelectorAll("#rootNode > .node");
        let maxRoot = 0;
        roots.forEach(root => {
            const id = root.dataset.id;
            const num = parseInt(id.replace("L", ""), 10);
            if (num > maxRoot) maxRoot = num;
        });
        nodeId = "L" + (maxRoot + 1);
    } else {
        const siblings = container.querySelectorAll(":scope > .node");
        let maxSuffix = 0;
        siblings.forEach(sib => {
            const parts = sib.dataset.id.split("-");
            const suffix = parseInt(parts[parts.length - 1], 10);
            if (suffix > maxSuffix) maxSuffix = suffix;
        });
        nodeId = parentId + "-" + (maxSuffix + 1);
    }

    nodeDiv.dataset.id = nodeId;

    nodeDiv.innerHTML = `
        <label>ID:</label>
        <input type="text" class="node-id" value="${nodeId}" readonly>
        <label>Label:</label>
        <input type="text" class="node-label" required
            oninput="markDirty(); updatePreview()">
        <button type="button" onclick="addProperty(this)">Add Property</button>
        <button type="button" onclick="addChild(this)">Add Child</button>
        <button type="button" onclick="this.parentElement.remove(); markDirty(); updatePreview()">Delete Node</button>
        <div class="properties"></div>
        <div class="children"></div>
    `;

    container.appendChild(nodeDiv);
    markDirty(); // only once on creation
    updatePreview();
}

// Add property to a node
function addProperty(button) {
    const propsDiv = button.parentElement.querySelector(".properties");
    const propDiv = document.createElement("div");
    propDiv.innerHTML = `
        <input type="text" class="prop-key" placeholder="Key">
        <input type="text" class="prop-value" placeholder="Value">
        <button type="button" onclick="this.parentElement.remove(); markDirty(); updatePreview()">Delete Property</button>
    `;
    propsDiv.appendChild(propDiv);

    // Attach input listeners
    attachInputEvents(propDiv.querySelector(".prop-key"));
    attachInputEvents(propDiv.querySelector(".prop-value"));

    markDirty();
    updatePreview();
}

// Add child node
function addChild(button) {
    const parentNode = button.parentElement;
    const parentId = parentNode.dataset.id;
    const childrenDiv = parentNode.querySelector(".children");

    if (!childrenDiv.id) {
        childrenDiv.id = "children-" + Math.random().toString(36).substr(2, 9);
    }

    addNode(childrenDiv.id, parentId);
}

// Build node recursively
function buildNode(nodeDiv, sortOrder) {
    const id = nodeDiv.querySelector(".node-id").value;
    const label = nodeDiv.querySelector(".node-label").value;

    const propsDiv = nodeDiv.querySelector(".properties");
    const properties = Array.from(propsDiv.children).map((propDiv, index) => ({
        key: propDiv.querySelector(".prop-key").value,
        value: propDiv.querySelector(".prop-value").value,
        sort_order: index + 1
    }));

    const childrenDiv = nodeDiv.querySelector(".children");
    const children = Array.from(childrenDiv.children)
        .filter(childDiv => childDiv.classList.contains("node"))
        .map((childDiv, index) => buildNode(childDiv, index + 1));

    return { id, label, sort_order: sortOrder, properties, children };
}

function buildExistingNode(container, node) {
    const nodeDiv = document.createElement("div");
    nodeDiv.className = "node";
    nodeDiv.dataset.id = node.id;

    nodeDiv.innerHTML = `
        <label>ID:</label>
        <input type="text" class="node-id" value="${node.id}" readonly>

        <label>Label:</label>
        <input type="text" class="node-label"
               value="${node.label || ''}"
               oninput="markDirty(); updatePreview()">

        <button type="button" onclick="addProperty(this)">Add Property</button>
        <button type="button" onclick="addChild(this)">Add Child</button>

        <button type="button"
                onclick="this.parentElement.remove(); markDirty(); updatePreview()">
            Delete Node
        </button>

        <div class="properties"></div>
        <div class="children"></div>
    `;

    /* ---------- properties ---------- */
    const propsDiv = nodeDiv.querySelector(".properties");
    (node.properties || [])
        .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0))
        .forEach(prop => {
            const propDiv = document.createElement("div");
            propDiv.className = "property";

            propDiv.innerHTML = `
                <input type="text" class="prop-key"
                       value="${prop.key || ''}"
                       oninput="markDirty(); updatePreview()">

                <input type="text" class="prop-value"
                       value="${prop.value || ''}"
                       oninput="markDirty(); updatePreview()">

                <button type="button"
                        onclick="this.parentElement.remove(); markDirty(); updatePreview()">
                    Delete Property
                </button>
            `;
            propsDiv.appendChild(propDiv);
        });

    /* ---------- children ---------- */
    const childrenDiv = nodeDiv.querySelector(".children");

    if (node.children && node.children.length) {
        childrenDiv.id = "children-" + Math.random().toString(36).slice(2);
        node.children
            .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0))
            .forEach(child => buildExistingNode(childrenDiv, child));
    }

    container.appendChild(nodeDiv);
}

// Update preview and hidden input
function updatePreview() {
    const eventname = document.getElementById("eventname").value;
    const eventyear = document.getElementById("eventyear").value;
    const eventcountry = document.getElementById("eventcountry").value;
    const eventarea = document.getElementById("eventarea").value;
    const eventareapin = document.getElementById("eventareapin").value;

    const year = eventyear ? parseInt(eventyear, 10) : null;
    const pin = eventareapin ? parseInt(eventareapin, 10) : null;

    const rootNodes = document.querySelectorAll("#rootNode > .node");
    const roots = [];
    rootNodes.forEach((rootDiv, index) => {
        roots.push(buildNode(rootDiv, index + 1));
    });

    const previewStructure = {
        eventName: eventname || "",
        eventYear: year,
        eventCountry: eventcountry || "",
        eventArea: eventarea || "",
        eventAreaPin: pin,
        eventStruct: roots
    };

    document.getElementById("eventPreview").innerText =
        JSON.stringify(previewStructure, null, 4);

    document.getElementById("eventstruct").value =
        JSON.stringify(roots);

}

async function saveform() {
    updatePreview();

    const form = document.getElementById("eventForm");
    if (!form) return;

    const status = document.getElementById("eventStatus");
    const formData = new FormData(form);

    status.innerText = "Saving...";
    status.style.color = "orange";

    try {
        const res = await fetch("/eventbuilder/save_event", {
            method: "POST",
            body: formData
        });

        if (!res.ok) {
            throw new Error("Save failed");
        }

        markClean();
    } catch (err) {
        console.error(err);
        status.innerText = "Save failed";
        status.style.color = "red";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#createevent form");
    const status = document.getElementById("eventStatus");
    const saveBtn = document.getElementById("saveButton");

    if (!saveBtn) {
        console.error("Save button not found");
        return;
    }

    status.innerText = "";


    // make event-level fields live
    const liveFields = [
        "eventname",
        "eventyear",
        "eventcountry",
        "eventarea",
        "eventareapin"
    ];

    liveFields.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener("input", () => {
                markDirty();      // optional but recommended
                updatePreview();  // 🔑 THIS is the fix
            });
        }
    });



    // ✅ SAVE BUTTON (modern way)
    saveBtn.addEventListener("click", (e) => {
        e.preventDefault();
        console.log("Save button clicked");
        saveform();
    });


    // ✅ LEAFLET FILE VALIDATION + THUMBNAIL PREVIEW
    const leafletInput = document.getElementById("eventLeaflet");
    const previewDiv = document.getElementById("leafletPreview");

    leafletInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // validate type
        const validTypes = ["application/pdf", "image/jpeg", "image/png"];
        if (!validTypes.includes(file.type)) {
            status.innerText = "Invalid file type. Only PDF, JPG, PNG allowed.";
            status.style.color = "red";
            leafletInput.value = ""; // reset
            previewDiv.innerHTML = "";
            return;
        }

        // clear old preview
        previewDiv.innerHTML = "";

        const reader = new FileReader();
        reader.onload = function (ev) {
            if (file.type === "application/pdf") {
                const embed = document.createElement("embed");
                embed.src = ev.target.result;
                embed.type = "application/pdf";
                embed.style.width = "120px";
                embed.style.height = "160px";
                previewDiv.appendChild(embed);
            } else if (file.type.startsWith("image/")) {
                const img = document.createElement("img");
                img.src = ev.target.result;
                img.style.maxWidth = "120px";
                img.style.maxHeight = "160px";
                img.style.border = "1px solid #ccc";
                previewDiv.appendChild(img);
            }
        };
        reader.readAsDataURL(file);

        // mark form dirty since leaflet changed
        markDirty();
    });
});

