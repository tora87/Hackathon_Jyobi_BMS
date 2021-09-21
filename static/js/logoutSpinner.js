$(function(){
    $(".log-out-wrapper a").on("click", function(e) {
        e.preventDefault();
        let url = $(this).attr("href");
        if (url !== "") {
            $(".load-wrapp").show();

            let time = setTimeout(function() {
                window.location = url;
            }, 5000);

            $(".load-wrapp").on("click", function() {
                $(".load-wrapp").hide();
                clearInterval(time);
                return;
            })
        }
        return false;
    });
});