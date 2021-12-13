$(document).ready(function() {

    $('form').on('submit' , function(event){

        $.ajax({

            data: {

                email: $('#email').val(),
                
                hovaten: $('#hovaten').val(),

                chucvu: $('#chucvu').val(),

                username: $('#username').val(),

                password: $('#password').val(),

                password_check: $('#password_check').val(),

            },

            type: 'POST',

            url: '/Register',

        })

        .done(function(data){

            if (data.message == 'Password Does Not Match'){

                $('#error').show().text(data.message);
            }

            if (data.message == 'TRUE'){
                window.location.replace('/');
            }

            if (data.message == 'User Already Created'){
                $('#error').show().text(data.message);
            }


        });

        event.preventDefault();

    });


});