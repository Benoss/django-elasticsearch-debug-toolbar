var toggle = function(elem) {
if (window.getComputedStyle(elem).display === 'block') {
    elem.style.display = 'none';
    return;
}

elem.style.display = 'block';
};

var uarr = String.fromCharCode(0x25b6),
    darr = String.fromCharCode(0x25bc);

var showHandler = function(e) {

    toggle(this.nextElementSibling)

    var arrow = document.querySelector('a.elasticShowTemplate .toggleArrow')
    arrow.textContent = arrow.textContent == uarr ? darr : uarr

    toggle(this.parentNode.nextElementSibling)

    return false
};

for (var e of document.querySelectorAll('a.elasticShowTemplate')) {
    e.addEventListener('click', showHandler)
}

var textHandler = function(e) {
    var selection = window.getSelection();
    var range = document.createRange();
    range.selectNodeContents(this.parentNode.nextElementSibling.querySelector('code'));
    selection.removeAllRanges();
    selection.addRange(range);
};

for (var e of document.querySelectorAll('.selectText')) {
    e.addEventListener('click', textHandler)
}
