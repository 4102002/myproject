
$(document).ready(function () {
    $('#showPasswordId').click(function () {
        if ($('#showPasswordId').prop('checked')) {
            $('#uPassword').attr('type', 'text');
        } else {
            $('#uPassword').attr('type', 'password');
        }
    });
    $('#loginForm').submit(function (e) {
        e.preventDefault();
        var uEmail = $('#uEmail').val();
        var uPassword = $('#uPassword').val();
        // var remember = $('#remember').prop('checked');
        $.ajax({
            url: '/auth_user/',
            type: 'POST',
            data: {
                uEmail: uEmail,
                uPassword: uPassword,
                // remember: remember,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                console.log(response.status);
                if (response == 'success') {
                    console.log('login success');
                    window.location.href = '/loggedin';
                } else {
                    console.log('login failed');
                    $('#loginFailed').removeClass('d-none');
                }
            },
            error: function (response) {
                if (response.status == 401) {
                    $('#loginFailed').removeClass('d-none');
                }
            }
        });
    });

    $('#signupForm').submit(function (e) {
        e.preventDefault();
        var uEmail = $('#uEmail').val();
        var uPassword = $('#uPassword').val();
        var uFirstName = $('#ufirstName').val();
        var uLastName = $('#ulastName').val();
        var uPhone = $('#uPhone').val();
        $.ajax({
            url: '/auth_user/register/',
            type: 'POST',
            data: {
                uEmail: uEmail,
                uPassword: uPassword,
                uFirstName: uFirstName,
                uLastName: uLastName,
                uPhone: uPhone,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                console.log(response);
                if (response == 'success') {
                    console.log('signup success');
                    window.location.href = '/login';
                } else {
                    console.log('signup failed');
                    // $('#signupFailed').removeClass('d-none');
                }
            },
            error: function (response) {
                if (response.status == 401) {
                    console.log('signup failed');
                    // $('#signupFailed').removeClass('d-none');
                }
            }
        });
    });
});