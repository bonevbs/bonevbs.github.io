// Reassemble obfuscated email addresses in the browser so the full address
// never appears in the page source (keeps simple crawlers from harvesting it).
//
// Markup (see _includes/social.html and _pages/contact.md):
//   <a data-email-user="name" data-email-domain="example.org">...</a>
//     -> gets href="mailto:name@example.org"; content left untouched
//   <span class="obfuscated-email" data-email-user=".." data-email-domain="..">..</span>
//     -> replaced by a mailto link showing the address
(function () {
  function addressOf(el) {
    return el.dataset.emailUser + "@" + el.dataset.emailDomain;
  }

  function run() {
    document.querySelectorAll("a[data-email-user]").forEach(function (a) {
      a.href = "mai" + "lto:" + addressOf(a);
    });
    document.querySelectorAll("span.obfuscated-email[data-email-user]").forEach(function (span) {
      var a = document.createElement("a");
      a.href = "mai" + "lto:" + addressOf(span);
      a.textContent = addressOf(span);
      span.replaceWith(a);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
