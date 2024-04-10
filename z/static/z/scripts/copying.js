let elements = document.getElementsByClassName("copyable");

for (const el of elements) {
    el.addEventListener("click", (e) => {
        text = el.textContent;

        navigator.clipboard.writeText(text);

        if (el.copiedTimeoutId) clearTimeout(el.copiedTimeoutId);

        el.classList.add("copied");

        el.copiedTimeoutId = setTimeout(() => {
            el.classList.remove("copied");
            el.copiedTimeoutId = null;
        }, 3000);
    });
}