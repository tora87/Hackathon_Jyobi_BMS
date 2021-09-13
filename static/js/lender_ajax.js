// janコードを読み込んだ後に実行する関数
// input:nameのjanコードを読み込んで送信する
$("#name").on('change', function ajax_communication() {
    'use strict';
    let book_jan = $("#name").val();
    $.ajax({
        type: 'POST',
        url: '/lend-return/search',
        data: {'jan': book_jan },
    }).done(function(res) {
        $('body').html(res);
    }).error(function(err) {
        console.log(err);
    })
})

