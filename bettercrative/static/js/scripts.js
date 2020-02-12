$('.navTrigger').click(function () {
    $(this).toggleClass('active');
    console.log("Clicked menu");
    $("#navlistcontents").toggleClass("show_list");
    $("#navlistcontents").fadeIn();

});