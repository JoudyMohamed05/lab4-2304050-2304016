document.querySelectorAll(".pw").forEach(function (box) {
    var input = box.querySelector("input");
    var button = box.querySelector(".eye");
    button.addEventListener("click", function () {
        var show = input.type === "password";
        input.type = show ? "text" : "password";
        box.classList.toggle("shown", show);
        button.setAttribute("aria-label", show ? "Hide password" : "Show password");
        button.setAttribute("aria-pressed", show ? "true" : "false");
        input.focus();
    });
});
