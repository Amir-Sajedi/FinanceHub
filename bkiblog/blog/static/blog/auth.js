(function () {
    document.querySelectorAll('[data-password-toggle]').forEach(function (button) {
        var input = document.getElementById(button.getAttribute('data-target'));
        if (!input) {
            return;
        }

        var showIcon = button.querySelector('.password-toggle__icon--show');
        var hideIcon = button.querySelector('.password-toggle__icon--hide');

        button.addEventListener('click', function () {
            var showPassword = input.type === 'password';
            input.type = showPassword ? 'text' : 'password';
            button.setAttribute('aria-pressed', showPassword ? 'true' : 'false');
            if (showIcon) {
                showIcon.hidden = showPassword;
            }
            if (hideIcon) {
                hideIcon.hidden = !showPassword;
            }
        });
    });
})();
