window.onload = function() {

  function post(path, params) {
    method = "post";

    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
  }

  var textarea = document.getElementById("post-body");
  var count = document.getElementById("count");

  document.addEventListener('keypress', function(e) {
    var active_element = document.activeElement;
    if (active_element.hasAttribute("id")) {
      var active_id = active_element.getAttribute('id');
      if (active_id == "post-body") {
        var text = active_element.value;
        console.log(text);
      }
    }
  })

  if(/^[0-9]+$/.test(textarea.getAttribute("maxlength"))) {

    var func = function() {
      var max = this.getAttribute("maxlength");
      var len = this.value.length;
      count.innerHTML = len.toString() + "/" +  max.toString();

      if(len <= 90) {
        count.style = "color: #5cb85c;"
      }
      else if(len <= 120) {
        count.style = "color: #ecc52c;"
      }
      else {
        count.style = "color: #d9534e;"
      }
    }

    textarea.onkeyup = func;
    textarea.onblur = func;

  }
}
