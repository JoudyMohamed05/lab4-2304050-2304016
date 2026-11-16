document.querySelectorAll("form[data-validate]").forEach(function (form) {
    var messages = {
        name: "Name is required",
        email: "Email is required",
        password: "Password is required",
        confirm_password: "Confirm password is required"
    };
    form.addEventListener("submit", function (event) {
        var errors = [];
        Object.keys(messages).forEach(function (field) {
            var input = form.elements[field];
            if (!input) { return; }
            var value = field === "password" || field === "confirm_password" ? input.value : input.value.trim();
            if (!value) { errors.push(messages[field]); }
        });
        var pw = form.elements["password"];
        var cpw = form.elements["confirm_password"];
        if (pw && cpw && pw.value && cpw.value && pw.value !== cpw.value) {
            errors.push("Passwords do not match");
        }
        var box = form.querySelector(".js-errors");
        if (errors.length) {
            event.preventDefault();
            box.innerHTML = "";
            errors.forEach(function (text) {
                var li = document.createElement("li");
                li.textContent = text;
                box.appendChild(li);
            });
            box.hidden = false;
        }
    });
});
