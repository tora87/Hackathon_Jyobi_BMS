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
        }).error(function (err) {
            console.log(err);
        })
    })

})
