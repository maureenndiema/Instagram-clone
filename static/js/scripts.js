$(document).ready(function() {
    $("#screenshots > div:gt(0)").hide();

    setInterval(function() {
        $('#screenshots > div:first')
            .fadeOut(2000)
            .next()
            .fadeIn(2000)
            .end()
            .appendTo('#screenshots');
    }, 4000);


})

document.getElementById('go-back').addEventListener('click', () => {
    history.back();
});