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
});
