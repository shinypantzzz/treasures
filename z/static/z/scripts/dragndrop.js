const dragndrops = document.getElementsByClassName('file_label')

for (const dragndrop of dragndrops) {
    dragndropInit(dragndrop);
}

window.addEventListener('dragover', (e) => {
    if (window.drugTimer) {
        clearTimeout(window.drugTimer);
    }
    for (const dragndrop of dragndrops) {
        dragndrop.classList.add("drugndrop_active");
    }
    window.drugTimer = setTimeout(() => {
        for (const dragndrop of dragndrops) {
            dragndrop.classList.remove("drugndrop_active");
        }
    }, 200);
});

/**
 * @param {HTMLElement} dragndrop
 */
function dragndropInit(dragndrop) {

    const input = dragndrop.parentElement.querySelector('input');//[type="file"]

    input.addEventListener('change', (e) => {
        const files = new DataTransfer();
        for (const file of input.files) {
            if (file.type.startsWith("image/")) {
                files.items.add(file);
            }
        }
        input.files = files.files;
        if (files.files.length > 0) {
            dragndrop.textContent = "";
            dragndrop.appendChild(document.createTextNode(files.files[0].name));
            for(let i=1; i<files.files.length; i++) {
                dragndrop.appendChild(document.createElement("br"));
                dragndrop.appendChild(document.createTextNode(files.files[i].name));
            }
        }
        
    });

    dragndrop.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    dragndrop.addEventListener('drop', (e) => {
        e.preventDefault();
        input.files = e.dataTransfer.files;
        input.dispatchEvent(new Event('change'));
    });
}