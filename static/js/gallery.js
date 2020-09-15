$('.gallery-container').each(function () {
    // the containers for all your galleries
    $(this).magnificPopup({
        delegate: 'a',
        type: 'image',
        gallery: {
            enabled: true
        }
    });
});


//Isotope Setup
let elem = document.querySelector('.gallery-container');

let iso = new Isotope(elem, {
    // options
    itemSelector: '.gallery-item',
    layoutMode: 'fitRows',
    percentPosition: true,
    fitRows: {
        gutter: 20
    }
});


function getFilterSelector() {
    let checks = document.querySelectorAll('.category-input');
    let result = '';
    checks.forEach((node) => {
        if (node.checked) {
            result += `${node.dataset.id}`
        }
    });

    return result
}

function filter(event) {
    iso.arrange({filter: getFilterSelector()})
}

document.getElementsByName('filter_category').forEach((node) => {
    node.addEventListener('click', filter)
})


if ('{{ filter }}' !== '') {
    document.querySelector('input[data-id="{{ filter }}"]').checked = true;
    filter()
}