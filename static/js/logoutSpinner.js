$(function(){
    $(".log-out-wrapper a").on("click", function(e) {
        e.preventDefault();
        let url = $(this).attr("href");
        let count = 4;
        let timer = $("#timer");
        if (url !== "") {
            $(".load-wrapp").show();

            let time = setTimeout(function() {
                window.location = url;
            }, 5000);

            let counter = setInterval(function(){
                timer.text(count--);
            }, 1000);

            $(".load-wrapp").on("click", function() {
                $(".load-wrapp").hide();
                clearInterval(time);
                clearInterval(count);
                return;
            })
        }
        return false;
    });
});