$(function() {
    if (typeof chrome !== "undefined" && !chrome.app.isInstalled) {
        $("#install-extension").click(function() {
            chrome.webstore.install();
        });
    } else {
        $("#install-extension").prop("disabled", true).addClass("disabled");
    }

    $('input').focus(function() {
        $(this).popover('show');
    });


    $('input').blur(function() {
        $(this).popover('hide');
    });

    $("#login").validate({
        rules: {
            email: {
                required: true,
                email: true
            },
            password: {
                required:true,
                minlength: 4
            }
        },

        errorClass: "help-inline",
        errorElement: "span",
        highlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success');
            $(element).parents('.control-group').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error');
            $(element).parents('.control-group').addClass('success');
        }
    });

    $("#login input[type=submit]").click(function() {
        return $("form").valid();
    });


    // Language Gym
    if ($("#question").length === 0) {
        return;
    }

    $("#lang1, #lang2").select2().change(newQuestion);

    $("#direction").click(function() {
        reverse = !reverse;
        $(this).html('<i class="icon-long-arrow-' + (reverse ? "left" : "right") + '"></i>');
        newQuestion();
    });

    $("#answer").focus().keyup(function(e) {
        if (e.keyCode == 13) {  // Return key
            checkAnswer();
        }
    });

    newQuestion();
});

var last_question = null;
var reverse = false;
var ready = false;

function newQuestion() {
    var from_lang = $("#lang1").val(),
        to_lang = $("#lang2").val();
    if (reverse) {
        var swap = from_lang;
        from_lang = to_lang;
        to_lang = swap;
    }
    $("#question").html('<span class="loading">Loading...</span>');
    $.getJSON("/gym/question/" + from_lang + "/" + to_lang, function(data) {
        console.log(data);
        if (data == "NO CARDS") {
            $("#question").html('<span class="wrong">You don\'t have anything to learn.</span>');
            return;
        }
        $("#question").html('<span>' + data.question + '</span>');
        last_question = data;
        ready = true;
    });
}

function checkAnswer() {
    if (!ready) {
        return;
    }

    var correct = $("#answer").val().toLowerCase() == last_question.answer.toLowerCase();
    var back = flippant.flip(
        $("#question").get(0),
        '<span class="' + (correct ? "correct" : "wrong") + '">' + last_question.answer + '</span>',
        "card",
        "card"
    );
    $.post("/gym/" + (correct ? "correct" : "wrong") + "/" + last_question.id);
    newQuestion();
    $("#answer").prop("disabled", true);
    window.setTimeout(function() {
        back.close();
        $("#answer").val("").prop("disabled", false).focus();
    }, 3000);
}
