document.addEventListener("DOMContentLoaded", () => {
    const originalData = [...dataFromFlask];
    let filteredData = [...originalData];
    
    const tbody = document.querySelector("#dataTable tbody");
    const yearFilter = document.getElementById("year");
    const numPerPage = document.getElementById("num-per-page");
    const headers = document.querySelectorAll("#dataTable th");
    const pageInfo = document.getElementById("pageInfo");
    const prevButton = document.getElementById("prevPage");
    const nextButton = document.getElementById("nextPage");

    let currentFilter = {
        column: null,
        ascending: true,
        numPerPage: parseInt(numPerPage.value, 10),
        currentPage: 1
    };

    function renderTable(data) {
        tbody.innerHTML = "";

        const totalPages = Math.ceil(data.length / currentFilter.numPerPage) || 1;

        if (currentFilter.currentPage > totalPages) {
            currentFilter.currentPage = totalPages;
        }
        else if (currentFilter.currentPage < 1) {
            currentFilter.currentPage = 1;
        }

        const start = (currentFilter.currentPage - 1) * currentFilter.numPerPage;
        const end = start + currentFilter.numPerPage;

        const pageData = data.slice(start, end);

        pageData.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${row.id}</td>
                <td>${row.title}</td>
                <td>${row.author}</td>
                <td>${row.year}</td>
            `;
            tbody.appendChild(tr);
        });

        pageInfo.textContent = `Page ${currentFilter.currentPage}`;
        prevButton.disabled = currentFilter.currentPage === 1;
        nextButton.disabled = currentFilter.currentPage === totalPages;
    }

    function updateSortArrows() {
        headers.forEach(header => {
            const arrow = header.querySelector(".sort-arrow");
            const column = header.dataset.column;

            if (!arrow) return;

            if (column === currentFilter.column) {
                arrow.textContent = currentFilter.ascending ? "↑" : "↓";
            } else {
                arrow.textContent = "";
            }
        });
    }

    function sortData(column, ascending = true) {
        filteredData.sort((a,b) => {
            const aValue = a[column];
            const bValue = b[column];

            if (aValue < bValue) return ascending ? -1 : 1;
            if (aValue > bValue) return ascending ? 1 : -1;
            return 0;
        });

        currentFilter.column = column;
        currentFilter.ascending = ascending;
        updateSortArrows();
        return filteredData;
    }

    function applyFilter() {
        const selectedYear = yearFilter.value;

        if (selectedYear === "all") {
            filteredData = [...originalData];
        } else {
            filteredData = originalData.filter(row => String(row.year) === selectedYear);
        }

        if (currentFilter.column) {
            filteredData = sortData(currentFilter.column, currentFilter.ascending);
        }
        renderTable(filteredData);
    }

    function setNumItemsPerPage() {
        currentFilter.numPerPage = numPerPage.value;
        currentFilter.currentPage = 1;
        renderTable(filteredData);
    }

    headers.forEach(header => {
        header.addEventListener("click", () => {
            const column = header.dataset.column;
            let ascending = true;

            if (currentFilter.column === column) {
                ascending = !currentFilter.ascending;
            }

            data = sortData(column, ascending);
            renderTable(data);
        });
    });

    prevButton.addEventListener("click", function () {
        if (currentFilter.currentPage > 1) {
            currentFilter.currentPage--;
            renderTable(filteredData);
        }
    });

    nextButton.addEventListener("click", function () {
        const totalPages = Math.ceil(filteredData.length / currentFilter.numPerPage);
        if (currentFilter.currentPage < totalPages) {
            currentFilter.currentPage++;
            renderTable(filteredData);
        }
    });

    yearFilter.addEventListener("change", applyFilter);
    numPerPage.addEventListener("change", setNumItemsPerPage);

    renderTable(filteredData);
    updateSortArrows();
});