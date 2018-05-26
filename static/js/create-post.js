window.onload = function() {
  var textarea = document.getElementById("post-body");
  var count = document.getElementById("count");

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
