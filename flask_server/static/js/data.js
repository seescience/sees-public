document.addEventListener("DOMContentLoaded", () => {
    const originalData = [...dataFromFlask];
    let filteredData = [...originalData];

    let currentSort = {
        column: null,
        ascending: true
    };
    
    const tbody = document.querySelector("#dataTable tbody");
    const yearFilter = document.getElementById("year");
    const headers = document.querySelectorAll("#dataTable th");

    function renderTable(data) {
        tbody.innerHTML = "";

        data.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${row.id}</td>
                <td>${row.title}</td>
                <td>${row.author}</td>
                <td>${row.year}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    function updateSortArrows() {
        headers.forEach(header => {
            const arrow = header.querySelector(".sort-arrow");
            const column = header.dataset.column;

            if (!arrow) return;

            if (column === currentSort.column) {
                arrow.textContent = currentSort.ascending ? "↑" : "↓";
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

        currentSort = { column, ascending };
        updateSortArrows();
        renderTable(filteredData);
    }

    function applyFilter() {
        const selectedYear = yearFilter.value;

        if (selectedYear === "all") {
            filteredData = [...originalData];
        } else {
            filteredData = originalData.filter(row => String(row.year) === selectedYear);
        }

        if (currentSort.column) {
            sortData(currentSort.column, currentSort.ascending);
        } else {
            renderTable(filteredData);
        }
    }

    headers.forEach(header => {
        header.addEventListener("click", () => {
            const column = header.dataset.column;
            let ascending = true;

            if (currentSort.column === column) {
                ascending = !currentSort.ascending;
            }

            sortData(column, ascending);
        });
    });

    yearFilter.addEventListener("change", applyFilter);

    renderTable(filteredData);
    updateSortArrows();
});