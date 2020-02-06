function validatePassword() {
    let pass1 = document.getElementById("psw1").value;
    let pass2 = document.getElementById("psw2").value;
    if (pass1 !== pass2) {
        document.getElementById("psw2").setCustomValidity("Passwords don't Match");
    } else {
        document.getElementById("psw2").setCustomValidity('');
        document.getElementById("signup-form").submit();
    }
}

document.getElementById("commit").addEventListener('click', validatePassword);