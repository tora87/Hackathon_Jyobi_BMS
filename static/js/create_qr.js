console.log("create_qr.js")

$(function() {
	$("#search_Btn").on('click', function() {
		let kw = $("#search_text_form").val();
		let sn = $("#select_number_form").val();
		$.ajax({
			type: 'POST',
            url: '/generate-qr/search',
			data: {'selectnum': sn,'keywords': kw},
		}).done(function (res) {
			$('body').html(res);
		}).error(function (err) {
			console.log(err);
		})
	})

	$("#reset_Btn").on('click', function() {
		$.ajax({
			type: "POST",
			url: '/generate-qr/search',
			data: {'selectnum': '', 'keywords': ''},
		}).done(function (res) {
			$('body').html(res);
		}).error(function (err) {
			console.log(err);
		})
	})

	$("#indicator").on("click", function() {
		$("#overlay").show();
	})
})
