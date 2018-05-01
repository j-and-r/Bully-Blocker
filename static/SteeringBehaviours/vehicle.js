function Vehicle(x, y) {
  this.pos = createVector(random(0, width), random(0, height));//p5.Vector.random2D();//createVector(x, y);
  this.target = createVector(x, y);
  this.vel = p5.Vector.random2D();
  this.acc = createVector();
  this.r = 8;
  this.max_speed = 5;
  this.max_force = 0.3;
}

Vehicle.prototype.behaviours = function () {
  var arrive = this.arrive(this.target);
  this.applyForce(arrive);

  var mouse = createVector(mouseX, mouseY);
  var flee = this.flee(mouse);
  this.applyForce(flee);
}

Vehicle.prototype.applyForce = function (f) {
  this.acc.add(f);
}

Vehicle.prototype.flee = function (target) {
  var desired = p5.Vector.sub(target, this.pos);
  var d = desired.mag();
  if (d < 75) {
    desired.setMag(this.max_speed*3);
    desired.mult(-1);
    var steer = p5.Vector.sub(desired, this.vel);
    steer.limit(this.max_force*3);
    return steer;
  } else {
    return createVector(0, 0);
  }
}

Vehicle.prototype.arrive = function (target) {
  var desired = p5.Vector.sub(target, this.pos);
  var d = desired.mag();
  var speed = this.max_speed;
  if (d<100) {
    speed = map(d, 0, 100, 0, this.max_speed);
  }
  desired.setMag(speed);
  var steer = p5.Vector.sub(desired, this.vel);
  steer.limit(this.max_force);
  return steer;
}

Vehicle.prototype.update = function () {
  this.pos.add(this.vel);
  this.vel.add(this.acc);
  this.acc.mult(0);
}

Vehicle.prototype.show = function () {
  stroke(0);
  strokeWeight(this.r);
  point(this.pos.x, this.pos.y);
}
