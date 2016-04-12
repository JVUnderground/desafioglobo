var escolha;
$(document).ready(function() {
    $(".retrato").click(function() {
        $(".retrato").css("outline","grey solid 1px");
        $(this).css("outline", "3px solid orange");
        escolha = $(this).attr("alt");
    });

    $(".votar").click(function() {
        $.post("/votar", {escolha: escolha, paredao: $("#votacao").attr("data-pid")}, function(resposta) {
            if(resposta == "sucesso") {
                window.location = "/resultado";
            }
        });
    });
});
