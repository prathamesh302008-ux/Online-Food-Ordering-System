// ==========================================
//  FIX: Prevent Bootstrap modals/dropdowns
//  from permanently blocking page scroll
// ==========================================

// 1. On page load — clean up any stale modal-open class
window.addEventListener("load", function () {
    document.body.classList.remove("modal-open");
    document.body.style.overflow = "";
    document.body.style.paddingRight = "";

    // Remove any leftover modal backdrops
    document.querySelectorAll(".modal-backdrop").forEach(function (el) {
        el.remove();
    });
});

// 2. Watch for Bootstrap modals being hidden and force-restore scroll
document.addEventListener("hidden.bs.modal", function () {
    // If no other modals are still open, restore scrolling
    var openModals = document.querySelectorAll(".modal.show");
    if (openModals.length === 0) {
        document.body.classList.remove("modal-open");
        document.body.style.overflow = "";
        document.body.style.paddingRight = "";

        document.querySelectorAll(".modal-backdrop").forEach(function (el) {
            el.remove();
        });
    }
});

// 3. Watch for Bootstrap offcanvas / collapse (mobile navbar)
document.addEventListener("hidden.bs.collapse", function () {
    document.body.style.overflow = "";
    document.body.style.paddingRight = "";
});

document.addEventListener("hidden.bs.offcanvas", function () {
    document.body.classList.remove("modal-open");
    document.body.style.overflow = "";
    document.body.style.paddingRight = "";

    document.querySelectorAll(".offcanvas-backdrop").forEach(function (el) {
        el.remove();
    });
});

// 4. Safety net — MutationObserver to catch any rogue overflow:hidden
(function () {
    var observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (m) {
            if (m.attributeName === "style" || m.attributeName === "class") {
                // If no modal/offcanvas is actually visible, ensure scroll is free
                var hasOpenModal = document.querySelector(".modal.show");
                var hasOpenOffcanvas = document.querySelector(".offcanvas.show");

                if (!hasOpenModal && !hasOpenOffcanvas) {
                    if (
                        document.body.style.overflow === "hidden" ||
                        document.body.classList.contains("modal-open")
                    ) {
                        document.body.classList.remove("modal-open");
                        document.body.style.overflow = "";
                        document.body.style.paddingRight = "";
                    }
                }
            }
        });
    });

    observer.observe(document.body, {
        attributes: true,
        attributeFilter: ["style", "class"],
    });
})();