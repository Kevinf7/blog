var NUM_STARS;
var stars = [];
var speed;

function setup() {
  NUM_STARS=2000;
  createCanvas(windowWidth,windowHeight);
  for (var i=0; i<NUM_STARS; i++) {
    stars[i] = new Star();
  }
}

function draw() {
    background(0);
    speed=map(mouseX,0,width,2,16);
    translate(width/2, height/2);
    for (var i=0; i<NUM_STARS; i++) {
        stars[i].update();
        stars[i].show();
    }
}


class Star {
  constructor() {
    this.x=random(-width, width);
    this.y=random(-height, height);
    this.z=random(width);
    this.px=this.x;
    this.py=this.y;
    this.s=random(4,24);
    this.p=random(2,8);
  }

  update() {
    this.z=this.z-this.p-speed;
    if (this.z<1) {
      this.z=width;
      this.x=random(-width, width);
      this.y=random(-height, height);
      this.px=this.x;
      this.py=this.y;
      this.s=random(4,24);
      this.p=random(2,12);
    }
  }

  show() {
    fill(255);
    noStroke();
    var sx = map(this.x / this.z, 0, 1, 0, width);
    var sy = map(this.y / this.z, 0, 1, 0, height);
    var r = map(this.z, 0, width, this.s, 0);

    ellipse(sx, sy, r, r);

    var ax = this.px;
    var ay = this.py;
    for(var i=0;i<5;i++) {
      var c = map(i,0,4,8,96);
      var bx = map(i,0,4,this.px,this.sx);
      var by = map(i,0,4,this.py,this.sy);
      stroke(c);
      line(ax, ay, bx, by);
      ax=bx;
      ay=by;
    }
  }
}
