var font;
var points;
var vehicles = [];

function preload() {
  font = loadFont('./static/SteeringBehaviours/avenir_next.otf');
}

function setup() {
  var canvas = createCanvas(770, 300);
  canvas.parent("title");
  textSize(120);
  points = font.textToPoints("Bully Blocker", 0, 200);
  for (var i = 0; i < points.length; i++) {
    var pt = points[i];
    var vehicle = new Vehicle(pt.x, pt.y);
    vehicles.push(vehicle);
  }
}

function draw() {
  background(255);
  for(var i = 0; i < vehicles.length; i++) {
    var v = vehicles[i];
    v.behaviours();
    v.update();
    v.show();
  }
}
