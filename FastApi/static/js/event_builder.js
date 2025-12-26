function addNode(containerId, parentId = null) {
    const container = document.getElementById(containerId);

    const nodeDiv = document.createElement("div");
    nodeDiv.className = "node";

    let nodeId;
    if (!parentId) {
        // Root node: find highest root number
        const roots = document.querySelectorAll("#rootNode > .node");
        let maxRoot = 0;
        roots.forEach(root => {
            const id = root.dataset.id;
            const num = parseInt(id.replace("L", ""), 10);
            if (num > maxRoot) maxRoot = num;
        });
        nodeId = "L" + (maxRoot + 1);
    } else {
        // Child node: find highest suffix among siblings
        const siblings = container.querySelectorAll(":scope > .node");
        let maxSuffix = 0;
        siblings.forEach(sib => {
            const id = sib.dataset.id;
            const parts = id.split("-");
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
            <input type="text" class="node-label" required>
            <button type="button" onclick="addProperty(this)">Add Property</button>
            <button type="button" onclick="addChild(this)">Add Child</button>
            <button type="button" onclick="this.parentElement.remove(); updatePreview()">Delete Node</button>
            <div class="properties"></div>
            <div class="children"></div>
        `;

    container.appendChild(nodeDiv);
    updatePreview();
}


function addProperty(button) {
    const propsDiv = button.parentElement.querySelector(".properties");
    const propDiv = document.createElement("div");
    propDiv.innerHTML = `
        <input type="text" class="prop-key" placeholder="Key" oninput="updatePreview()">
        <input type="text" class="prop-value" placeholder="Value" oninput="updatePreview()">
        <button type="button" onclick="this.parentElement.remove(); updatePreview()">Delete Property</button>
        `;
    propsDiv.appendChild(propDiv);
    updatePreview();
}


function addChild(button) {
    const parentNode = button.parentElement;
    const parentId = parentNode.dataset.id;
    const childrenDiv = parentNode.querySelector(".children");

    if (!childrenDiv.id) {
        childrenDiv.id = "children-" + Math.random().toString(36).substr(2, 9);
    }

    addNode(childrenDiv.id, parentId);
}



function buildNode(nodeDiv, sortOrder) {
    const id = nodeDiv.querySelector(".node-id").value;
    const label = nodeDiv.querySelector(".node-label").value;

    // Properties with sort_order
    const propsDiv = nodeDiv.querySelector(".properties");
    const properties = Array.from(propsDiv.children).map((propDiv, index) => {
        return {
            key: propDiv.querySelector(".prop-key").value,
            value: propDiv.querySelector(".prop-value").value,
            sort_order: index + 1
        };
    });

    // Children with sort_order
    const childrenDiv = nodeDiv.querySelector(".children");
    const children = Array.from(childrenDiv.children)
        .filter(childDiv => childDiv.classList.contains("node"))
        .map((childDiv, index) => buildNode(childDiv, index + 1));

    return {
        id: id,
        label: label,
        sort_order: sortOrder,
        properties: properties,
        children: children
    };
}



function buildExistingNode(container, node) {
    const nodeDiv = document.createElement("div");
    nodeDiv.className = "node";
    nodeDiv.dataset.id = node.id;

    nodeDiv.innerHTML = `
            <label>ID:</label>
            <input type="text" class="node-id" value="${node.id}" readonly>
            <label>Label:</label>
            <input type="text" class="node-label" value="${node.label}">
            <button type="button" onclick="addProperty(this)">Add Property</button>
            <button type="button" onclick="addChild(this)">Add Child</button>
            <button type="button" onclick="this.parentElement.remove(); updatePreview()">Delete Node</button>
            <div class="properties"></div>
            <div class="children"></div>
        `;

    // Properties sorted
    const propsDiv = nodeDiv.querySelector(".properties");
    (node.properties || [])
        .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0))
        .forEach(prop => {
            const propDiv = document.createElement("div");
            propDiv.className = "property";
            propDiv.innerHTML = `
                    <input type="text" class="prop-key" value="${prop.key}">
                    <input type="text" class="prop-value" value="${prop.value}">
                    <button type="button" onclick="this.parentElement.remove(); updatePreview()">Delete Property</button>
                `;
            propsDiv.appendChild(propDiv);
        });

    // Children sorted
    const childrenDiv = nodeDiv.querySelector(".children");
    (node.children || [])
        .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0))
        .forEach(child => buildExistingNode(childrenDiv, child));

    container.appendChild(nodeDiv);
    updatePreview();
}


function updatePreview() {
    const eventname = document.getElementById("eventname").value;
    const rootNodes = document.querySelectorAll("#rootNode > .node");
    if (rootNodes.length === 0) {
        document.getElementById("eventPreview").innerText = "No root node yet.";
        document.getElementById("eventResult").style.color = "red";
        return;
    }

    const roots = [];
    rootNodes.forEach(rootDiv => {
        roots.push(buildNode(rootDiv));
    });

    const structure = { name: eventname || "Untitled Event", roots };

    document.getElementById("eventPreview").innerText = JSON.stringify(structure, null, 4);
    document.getElementById("eventResult").innerText = "Save your changes";
    document.getElementById("eventResult").style.color = "red";
}



async function saveEvent() {
    const eventname = document.getElementById("eventname").value;
    const rootNodes = document.querySelectorAll("#rootNode > .node");
    if (rootNodes.length === 0) {
        document.getElementById("eventPreview").innerText = "No root node yet.";
        document.getElementById("eventResult").style.color = "red";
        return;
    }

    const roots = [];
    rootNodes.forEach((rootDiv, index) => {
        roots.push(buildNode(rootDiv, index + 1));  // assign sort_order here
    });

    const structure = { name: eventname, roots };

    const response = await fetch("/event/save_event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(structure)
    });

    const result = await response.json();
    document.getElementById("eventResult").innerText = result.message;
    document.getElementById("eventResult").style.color = "green";
}

document.addEventListener("keyup", updatePreview);
document.addEventListener("click", updatePreview);
