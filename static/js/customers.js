/* =========================================================
   CUSTOMER INTELLIGENCE DASHBOARD
   CUSTOMER EXPLORER JAVASCRIPT
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // ELEMENTS
    // =====================================================

    const searchInput = document.getElementById("tableSearchInput");
    const contractFilter = document.getElementById("contractFilter");
    const churnFilter = document.getElementById("churnFilter");
    const riskFilter = document.getElementById("riskFilter");
    const resetButton = document.getElementById("resetFiltersBtn");

    const tableBody = document.getElementById("customerTableBody");
    const rows = Array.from(
        tableBody.querySelectorAll(".customer-row")
    );

    const visibleCount = document.getElementById("visibleCount");
    const totalRecordCount = document.getElementById("totalRecordCount");

    const noResultsState = document.getElementById("noResultsState");

    const currentPageNum = document.getElementById("currentPageNum");
    const totalPagesNum = document.getElementById("totalPagesNum");

    const prevPageBtn = document.getElementById("prevPageBtn");
    const nextPageBtn = document.getElementById("nextPageBtn");

    const paginationPageNumbers =
        document.getElementById("paginationPageNumbers");


    // =====================================================
    // PAGINATION SETTINGS
    // =====================================================

    const rowsPerPage = 20;

    let currentPage = 1;

    let filteredRows = [...rows];


    // =====================================================
    // INITIAL COUNTS
    // =====================================================

    if (totalRecordCount) {
        totalRecordCount.textContent = rows.length;
    }


    // =====================================================
    // NORMALIZE TEXT
    // =====================================================

    function normalize(value) {

        return String(value || "")
            .trim()
            .toLowerCase();

    }


    // =====================================================
    // FILTER FUNCTION
    // =====================================================

    function applyFilters() {

        const searchValue =
            normalize(searchInput ? searchInput.value : "");

        const contractValue =
            normalize(contractFilter ? contractFilter.value : "");

        const churnValue =
            normalize(churnFilter ? churnFilter.value : "");

        const riskValue =
            normalize(riskFilter ? riskFilter.value : "");


        filteredRows = rows.filter(function (row) {

            // ---------------------------------------------
            // SEARCH
            // ---------------------------------------------

            const searchText =
                normalize(row.dataset.search);

            const searchMatch =
                searchValue === "" ||
                searchText.includes(searchValue);


            // ---------------------------------------------
            // CONTRACT
            // ---------------------------------------------

            const contract =
                normalize(row.dataset.contract);

            const contractMatch =
                contractValue === "" ||
                contract === contractValue;


            // ---------------------------------------------
            // CHURN
            // ---------------------------------------------

            const churn =
                normalize(row.dataset.churn);

            const churnMatch =
                churnValue === "" ||
                churn === churnValue;


            // ---------------------------------------------
            // RISK
            // ---------------------------------------------

            const risk =
                normalize(row.dataset.risk);

            const riskMatch =
                riskValue === "" ||
                risk === riskValue;


            return (
                searchMatch &&
                contractMatch &&
                churnMatch &&
                riskMatch
            );

        });


        // Reset to first page after filtering
        currentPage = 1;

        renderTable();

    }


    // =====================================================
    // RENDER TABLE
    // =====================================================

    function renderTable() {

        // Hide all rows first
        rows.forEach(function (row) {
            row.style.display = "none";
        });


        // If nothing found
        if (filteredRows.length === 0) {

            if (noResultsState) {
                noResultsState.style.display = "block";
            }

            if (tableBody) {
                tableBody.style.display = "none";
            }

            updatePagination();

            updateVisibleCount();

            return;

        }


        // Results available
        if (noResultsState) {
            noResultsState.style.display = "none";
        }

        if (tableBody) {
            tableBody.style.display = "";
        }


        // Calculate pagination
        const startIndex =
            (currentPage - 1) * rowsPerPage;

        const endIndex =
            startIndex + rowsPerPage;


        const pageRows =
            filteredRows.slice(startIndex, endIndex);


        // Show current page rows
        pageRows.forEach(function (row) {

            row.style.display = "";

        });


        updatePagination();

        updateVisibleCount();

    }


    // =====================================================
    // UPDATE VISIBLE COUNT
    // =====================================================

    function updateVisibleCount() {

        if (visibleCount) {

            visibleCount.textContent =
                filteredRows.length;

        }

    }


    // =====================================================
    // PAGINATION
    // =====================================================

    function updatePagination() {

        const totalPages =
            Math.max(
                1,
                Math.ceil(
                    filteredRows.length / rowsPerPage
                )
            );


        // Current page
        if (currentPageNum) {
            currentPageNum.textContent = currentPage;
        }


        // Total pages
        if (totalPagesNum) {
            totalPagesNum.textContent = totalPages;
        }


        // Previous button
        if (prevPageBtn) {

            prevPageBtn.disabled =
                currentPage <= 1;

        }


        // Next button
        if (nextPageBtn) {

            nextPageBtn.disabled =
                currentPage >= totalPages;

        }


        // Page numbers
        renderPageNumbers(totalPages);

    }


    // =====================================================
    // PAGE NUMBER BUTTONS
    // =====================================================

    function renderPageNumbers(totalPages) {

        if (!paginationPageNumbers) {
            return;
        }


        paginationPageNumbers.innerHTML = "";


        // Maximum visible page buttons
        const maxButtons = 5;


        let startPage =
            Math.max(
                1,
                currentPage - 2
            );


        let endPage =
            Math.min(
                totalPages,
                startPage + maxButtons - 1
            );


        // Adjust start page
        if (
            endPage - startPage + 1 <
            maxButtons
        ) {

            startPage =
                Math.max(
                    1,
                    endPage - maxButtons + 1
                );

        }


        for (
            let page = startPage;
            page <= endPage;
            page++
        ) {

            const button =
                document.createElement("button");


            button.type = "button";

            button.className =
                "pagination-btn pagination-number";


            button.textContent = page;


            if (page === currentPage) {

                button.classList.add("active");

            }


            button.addEventListener(
                "click",
                function () {

                    currentPage = page;

                    renderTable();

                    scrollToTable();

                }
            );


            paginationPageNumbers.appendChild(button);

        }

    }


    // =====================================================
    // NEXT PAGE
    // =====================================================

    if (nextPageBtn) {

        nextPageBtn.addEventListener(
            "click",
            function () {

                const totalPages =
                    Math.ceil(
                        filteredRows.length /
                        rowsPerPage
                    );


                if (
                    currentPage <
                    totalPages
                ) {

                    currentPage++;

                    renderTable();

                    scrollToTable();

                }

            }
        );

    }


    // =====================================================
    // PREVIOUS PAGE
    // =====================================================

    if (prevPageBtn) {

        prevPageBtn.addEventListener(
            "click",
            function () {

                if (currentPage > 1) {

                    currentPage--;

                    renderTable();

                    scrollToTable();

                }

            }
        );

    }


    // =====================================================
    // SEARCH EVENT
    // =====================================================

    if (searchInput) {

        searchInput.addEventListener(
            "input",
            function () {

                applyFilters();

            }
        );

    }


    // =====================================================
    // CONTRACT FILTER
    // =====================================================

    if (contractFilter) {

        contractFilter.addEventListener(
            "change",
            function () {

                applyFilters();

            }
        );

    }


    // =====================================================
    // CHURN FILTER
    // =====================================================

    if (churnFilter) {

        churnFilter.addEventListener(
            "change",
            function () {

                applyFilters();

            }
        );

    }


    // =====================================================
    // RISK FILTER
    // =====================================================

    if (riskFilter) {

        riskFilter.addEventListener(
            "change",
            function () {

                applyFilters();

            }
        );

    }


    // =====================================================
    // RESET FILTERS
    // =====================================================

    if (resetButton) {

        resetButton.addEventListener(
            "click",
            function () {

                if (searchInput) {
                    searchInput.value = "";
                }

                if (contractFilter) {
                    contractFilter.value = "";
                }

                if (churnFilter) {
                    churnFilter.value = "";
                }

                if (riskFilter) {
                    riskFilter.value = "";
                }

                currentPage = 1;

                applyFilters();

            }
        );

    }


    // =====================================================
    // SCROLL TO TABLE
    // =====================================================

    function scrollToTable() {

        const table =
            document.getElementById(
                "customerTable"
            );


        if (!table) {
            return;
        }


        const rect =
            table.getBoundingClientRect();


        // Only scroll if table is outside viewport
        if (
            rect.top < 0 ||
            rect.bottom >
            window.innerHeight
        ) {

            table.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }

    }


    // =====================================================
    // CUSTOMER ROW CLICK
    // =====================================================

    rows.forEach(function (row) {

        row.addEventListener(
            "dblclick",
            function () {

                const customerId =
                    row.dataset.customer;


                if (!customerId) {
                    return;
                }


                window.location.href =
                    "/customer/" +
                    encodeURIComponent(
                        customerId
                    );

            }
        );

    });


    // =====================================================
    // INITIAL RENDER
    // =====================================================

    renderTable();

});