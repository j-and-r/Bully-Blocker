window.onload = function() {

  function post(path, tweet) {
    return fetch('https://bully-blocker.herokuapp.com/moderate', {
      method: 'POST',
      body: JSON.stringify({text: tweet})
    })
    .then((resp) => resp.json())
    .then(function(response) {
      console.info('fetch()', response);
      return response;
    });
  }

  var textarea = document.getElementById("post-body");
  var count = document.getElementById("count");

  document.addEventListener('keypress', function(e) {
    var active_element = document.activeElement;
    if (active_element.hasAttribute("id")) {
      var active_id = active_element.getAttribute('id');
      if (active_id == "post-body") {
        var text = active_element.value;
        result = post("/moderate/", text);
        console.log(result);
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
