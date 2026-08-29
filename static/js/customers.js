/**
 * Customer Directory Search, Filtering & Pagination (customers.js)
 */
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("tableSearchInput");
    const contractFilter = document.getElementById("contractFilter");
    const churnFilter = document.getElementById("churnFilter");
    const riskFilter = document.getElementById("riskFilter");
    const resetBtn = document.getElementById("resetFiltersBtn");
    
    const rows = Array.from(document.querySelectorAll("#customerTableBody .customer-row"));
    const visibleCountEl = document.getElementById("visibleCount");
    const noResultsState = document.getElementById("noResultsState");
    const paginationControls = document.getElementById("paginationControls");
    
    const prevPageBtn = document.getElementById("prevPageBtn");
    const nextPageBtn = document.getElementById("nextPageBtn");
    const currentPageNumEl = document.getElementById("currentPageNum");
    const totalPagesNumEl = document.getElementById("totalPagesNum");
    const pageListEl = document.getElementById("paginationPageNumbers");

    const PAGE_SIZE = 25;
    let currentPage = 1;
    let filteredRows = [...rows];

    // Read URL search param if present (e.g. from navbar global search)
    const urlParams = new URLSearchParams(window.location.search);
    const initialSearch = urlParams.get("search");
    if (initialSearch && searchInput) {
        searchInput.value = initialSearch;
    }

    const applyFilters = () => {
        const query = searchInput ? searchInput.value.trim().toLowerCase() : "";
        const contractVal = contractFilter ? contractFilter.value : "";
        const churnVal = churnFilter ? churnFilter.value : "";
        const riskVal = riskFilter ? riskFilter.value : "";

        filteredRows = rows.filter(row => {
            const rowSearch = (row.getAttribute("data-search") || "").toLowerCase();
            const rowContract = row.getAttribute("data-contract") || "";
            const rowChurn = row.getAttribute("data-churn") || "";
            const rowRisk = row.getAttribute("data-risk") || "";

            const matchesSearch = !query || rowSearch.includes(query);
            const matchesContract = !contractVal || rowContract === contractVal;
            const matchesChurn = !churnVal || rowChurn === churnVal;
            const matchesRisk = !riskVal || rowRisk === riskVal;

            return matchesSearch && matchesContract && matchesChurn && matchesRisk;
        });

        currentPage = 1;
        renderPage();
    };

    const renderPage = () => {
        const totalMatching = filteredRows.length;
        const totalPages = Math.max(1, Math.ceil(totalMatching / PAGE_SIZE));

        if (currentPage > totalPages) currentPage = totalPages;
        if (currentPage < 1) currentPage = 1;

        // Hide all rows first
        rows.forEach(r => r.style.display = "none");

        if (totalMatching === 0) {
            if (noResultsState) noResultsState.style.display = "block";
            if (paginationControls) paginationControls.style.display = "none";
        } else {
            if (noResultsState) noResultsState.style.display = "none";
            if (paginationControls) paginationControls.style.display = "flex";

            // Show slice for current page
            const startIndex = (currentPage - 1) * PAGE_SIZE;
            const endIndex = Math.min(startIndex + PAGE_SIZE, totalMatching);

            for (let i = startIndex; i < endIndex; i++) {
                filteredRows[i].style.display = "";
            }
        }

        // Update counters
        if (visibleCountEl) visibleCountEl.textContent = totalMatching.toLocaleString();
        if (currentPageNumEl) currentPageNumEl.textContent = currentPage;
        if (totalPagesNumEl) totalPagesNumEl.textContent = totalPages;

        // Update Prev / Next Buttons
        if (prevPageBtn) prevPageBtn.disabled = (currentPage === 1);
        if (nextPageBtn) nextPageBtn.disabled = (currentPage === totalPages || totalMatching === 0);

        renderPaginationNumbers(totalPages);
    };

    const renderPaginationNumbers = (totalPages) => {
        if (!pageListEl) return;
        pageListEl.innerHTML = "";

        if (totalPages <= 1) return;

        // Determine window of pages around current page
        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(totalPages, currentPage + 2);

        if (startPage > 1) {
            addPageButton(1);
            if (startPage > 2) addEllipsis();
        }

        for (let p = startPage; p <= endPage; p++) {
            addPageButton(p);
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) addEllipsis();
            addPageButton(totalPages);
        }
    };

    const addPageButton = (pageNum) => {
        const btn = document.createElement("button");
        btn.className = `page-num-btn ${pageNum === currentPage ? "active" : ""}`;
        btn.textContent = pageNum;
        btn.addEventListener("click", () => {
            currentPage = pageNum;
            renderPage();
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
        pageListEl.appendChild(btn);
    };

    const addEllipsis = () => {
        const span = document.createElement("span");
        span.className = "page-ellipsis";
        span.textContent = "...";
        span.style.color = "var(--text-muted)";
        span.style.padding = "0 4px";
        span.style.display = "inline-flex";
        span.style.alignItems = "center";
        pageListEl.appendChild(span);
    };

    // Event Listeners
    if (searchInput) searchInput.addEventListener("input", applyFilters);
    if (contractFilter) contractFilter.addEventListener("change", applyFilters);
    if (churnFilter) churnFilter.addEventListener("change", applyFilters);
    if (riskFilter) riskFilter.addEventListener("change", applyFilters);

    if (resetBtn) {
        resetBtn.addEventListener("click", () => {
            if (searchInput) searchInput.value = "";
            if (contractFilter) contractFilter.value = "";
            if (churnFilter) churnFilter.value = "";
            if (riskFilter) riskFilter.value = "";
            applyFilters();
        });
    }

    if (prevPageBtn) {
        prevPageBtn.addEventListener("click", () => {
            if (currentPage > 1) {
                currentPage--;
                renderPage();
                window.scrollTo({ top: 0, behavior: "smooth" });
            }
        });
    }

    if (nextPageBtn) {
        nextPageBtn.addEventListener("click", () => {
            const totalPages = Math.ceil(filteredRows.length / PAGE_SIZE);
            if (currentPage < totalPages) {
                currentPage++;
                renderPage();
                window.scrollTo({ top: 0, behavior: "smooth" });
            }
        });
    }

    // Run initial filter/pagination on load
    applyFilters();
});
