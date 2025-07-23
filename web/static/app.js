function loadLogBlocks(apiUrl) {
    const container = document.getElementById("log-container");
    container.innerHTML = "";

    fetch(apiUrl)
    .then(res => res.json())
    .then(data => {
        for (const key in data) {
            const wrapper = document.createElement("div");
            wrapper.style.marginBottom = "20px";
            wrapper.style.width = "300px";

            const block = document.createElement("div");
            block.classList.add("square-block");
            block.textContent = key;

            const logContent = document.createElement("div");
            logContent.classList.add("log-content");
            logContent.style.display = "none";

            if (Array.isArray(data[key])) {
                data[key].forEach(entry => {
                    const line = document.createElement("div");
                    line.classList.add("log-line", entry.level.toLowerCase());
                    line.textContent = `[${entry.level}][${entry.time}][${entry.file}] ${entry.message}`;
                    logContent.appendChild(line);
                });
            }
            else {
                const lines = data[key];
                for (const lineno in lines) {
                    const lineHeader = document.createElement("div");
                    lineHeader.classList.add("line-header");
                    lineHeader.textContent = `${key}:${lineno}`;
                    logContent.appendChild(lineHeader);

                    lines[lineno].forEach(entry => {
                        const line = document.createElement("div");
                        line.classList.add("log-line", entry.level.toLowerCase(), "indent");
                        line.textContent = `[${entry.level}][${entry.time}][${entry.name}] ${entry.message}`;
                        logContent.appendChild(line);
                    });
                }
            }

            block.onclick = () => {
                logContent.style.display = logContent.style.display === "none" ? "block" : "none";
            };

            wrapper.appendChild(block);
            wrapper.appendChild(logContent);
            container.appendChild(wrapper);
        }
    })
    .catch(err => {
        container.textContent = "Ошибка загрузки логов: " + err;
    });
}
