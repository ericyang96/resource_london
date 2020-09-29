$(document).ready(function(){
$("select").change(function(){
    $(this).find("option:selected").each(function(){
        if($(this).attr("value")=="red"){
            $(".box").not(".red").hide();
            $(".red").show();
        }else if($(this).attr("value")=="green"){
            $(".box").not(".green").hide();
            $(".green").show();
        }else if($(this).attr("value")=="blue"){
            $(".box").not(".blue").hide();
            $(".blue").show();
        }else if($(this).attr("value")=="maroon"){
            $(".box").not(".maroon").hide();
            $(".maroon").show();
        }else{
            $(".box").hide();
        }
    });
}).change();
});

$(document).ready(function(){
    $("#tomato").click(function(){
        $(".numberinput").val("");
    });

});

$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip({'placement': 'top'});
});

$(function () {
  $('[data-toggle="popover"]').popover({
    container: 'body'
  })
})

$(function () {
  $('.popover-dismiss').popover({
    trigger: 'focus'
  })
})
