console.log("create_qr.js")

$(function() {
	$("#select_number_form").change( function () {
		console.log("selected")
		let sn = $(this).val();
        $.ajax({
            type: 'POST',
            url: '/generate-qr/search',
            data: {'selectnum': sn},
        }).done(function (res) {
            $('body').html(res);
        }).error(function (err) {
            console.log(err);
        })
    })

})