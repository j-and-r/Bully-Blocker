window.onload = function() {

  var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
      var anHttpRequest = new XMLHttpRequest();
      anHttpRequest.onreadystatechange = function() {
        if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
          aCallback(anHttpRequest.responseText);
      }

      anHttpRequest.open( "GET", aUrl, true );
      anHttpRequest.send( null );
    }
  }

  var textarea = document.getElementById("post-body");
  var count = document.getElementById("count");
  var rating_element = document.getElementById('rating');
  var client = new HttpClient();
  var last_moderate = 0;
  var last_text= "";

  if (!Date.now) {
    Date.now = function() { return new Date().getTime(); }
  }

  var moderate = function() {
    var time = Math.floor(Date.now() / 1000);
    var text = document.getElementById('post-body').value;
    var modified = text.replace( /\s/g, "");
    var text_diff = diff(text, last_text);
    var difference = "";

    for (var i = 0; i < text_diff.length; i++) {
      var e = text_diff[i];
      if (e[0] != 0) {
        difference += e[1];
      }
    }

    if (last_text != text && modified != last_text && (difference.length > 4 || time - last_moderate > 3)) {

      last_moderate = time;
      last_text = text;

      if (text == "") {
        text = "%20"
      }

      var result = client.get("https://bully-blocker.herokuapp.com/moderate?text=" +  text, function(response) {
        console.log(response);
        rating_element.innerHTML = response;
      });
    }
  }

  setInterval(function() {
    moderate();
  }, 1000);

  document.addEventListener('keyup', function(e) {
    if (e.key == "Space") {
      moderate();
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
