function filterBloodGroup() {
    var filterValue = document.getElementById("bloodGroupFilter").value;
    var rows = document.querySelectorAll("#donationTable .person-row");

    rows.forEach(function(row) {
        var bloodGroup = row.getAttribute("data-blood-group");

        if (filterValue === "" || bloodGroup === filterValue) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

function filterLocation() {
    var filterValue = document.getElementById("locationFilter").value;
    var rows = document.querySelectorAll("#donationTable .person-row");

    rows.forEach(function(row) {
        var location = row.getAttribute("data-location");

        if (filterValue === "" || location === filterValue) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

function sortTable() {
    var table = document.getElementById("donationTable");
    var rows = Array.from(table.rows).slice(1);
    var sortOption = document.getElementById("sortOption").value;

    rows.sort(function(rowA, rowB) {
        var cellA = rowA.cells[sortOption === "bloodGroup" ? 4 : 6].innerText; 
        var cellB = rowB.cells[sortOption === "bloodGroup" ? 4 : 6].innerText;

        return cellA.localeCompare(cellB);
    });

    rows.forEach(function(row) {
        table.appendChild(row);
    });
}

