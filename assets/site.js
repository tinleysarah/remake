// Small progressive enhancements. The site reads and navigates fine without this file.
(function () {
  // Mobile menu
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Demo forms: nothing is sent anywhere. Validate, then say so plainly.
  document.querySelectorAll("form[data-demo-form]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var note = form.querySelector(".form-note");
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      if (note) {
        note.textContent = form.getAttribute("data-demo-form");
      }
      form.reset();
    });
  });
})();
