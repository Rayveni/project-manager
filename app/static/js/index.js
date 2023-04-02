function collapse_sidebar() {
    let collapse_items = document.querySelectorAll("#sidebar>ul>li  span,tooltip");

    collapse_items.forEach(function(item) {
        item.classList.toggle("is-collapsed");
    });
};
