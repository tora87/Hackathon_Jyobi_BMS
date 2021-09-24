$(function () {
    'use strict';
    $(".aTag").on("click", function () {
        let book_jan = $(this).children("input").val();
        $.ajax({
            type: 'POST',
            url: '/booklist/ajax',
            data: {'jan': book_jan},
        }).done(function (res) {
            $('body').html(res);
            $('#book-detail').addClass('active');
        }).fail(function (err) {
            console.log(err);
        })
    })
    $("#search_Btn").on("click", function () {
        let kw = $("#search_text_form").val();
        $.ajax({
            type: 'POST',
            url: '/booklist/search',
            data: {'key': kw},
        }).done(function (res) {
            $('body').html(res);
        }).fail(function (err) {
            console.log(err);
        })
    })

    $("#reset_Btn").on("click", function () {
        $.ajax({
            type: "POST",
            url: '/booklist/search',
            data: {'key': ''},
        }).done(function (res) {
            $('body').html(res);
        }).fail(function (err) {
            console.log(err);
        })
    })

    $('#close-btn').on('click',function(){
        $('#book-detail').removeClass('active');
    })
})
