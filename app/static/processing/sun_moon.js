let suns = [];
let num_suns = 6;
let moons = [];

function setup() {
  createCanvas(windowWidth,windowHeight);
  for (let i = 0; i < num_suns; i++) {
    suns.push(new Sun(random(0,width), random(0,height)));
  }
  noStroke();
  fill(0);
}

function draw() {
  background(175,215,255);
  for (let i = 0; i < suns.length; i++) {
    suns[i].display();
  }
  for(let i=0; i<moons.length; i++) {
    moons[i].display();
  }
}

function mouseClicked() {
  moons.push(new Moon(mouseX,mouseY));
}

class Sun {
  constructor(x, y) {
    this.x=x;
    this.y=y;
    //size of sun
    this.rad=random(8,50);
  }

  display() {
    fill(255,0,0,200);
    ellipse(this.x,this.y,this.rad*2,this.rad*2);
  }

  getx () {
    return this.x;
  }

  gety() {
    return this.y;
  }

  getrad() {
    return this.rad;
  }
}

class Moon {

  constructor(x,y) {
    this.x=x;
    this.y=y;
    this.rad=4;
    this.loccount=0; //for the lerp
    this.startspin=false;

    // calculate distance to each sun
    this.adj = [];
    this.opp = [];
    this.dist = [];
    for (let i=0; i<num_suns; i++) {
      this.adj[i]  = this.x-suns[i].getx();
      this.opp[i] = suns[i].gety()-this.y;
      this.dist[i] = sqrt(pow(this.adj[i],2)+pow(this.opp[i],2));
    }

    // for the closest sun, get the index and the distance
    this.closestsun_index = 0;
    this.closestsun_dist = 99999999;
    for (let i=0; i<num_suns; i++) {
      if (this.dist[i] < this.closestsun_dist) {
        this.closestsun_index = i;
        this.closestsun_dist = this.dist[i];
      }
    }

    // get theta
    this.theta = atan2(this.opp[this.closestsun_index],this.adj[this.closestsun_index])+PI/2;
    // get the sun object
    this.sun = suns[this.closestsun_index];
    // get sun radius
    this.radmotion = this.sun.getrad() + 8;
    // calculate distance to sun
    this.distspin = this.closestsun_dist - this.radmotion;
    // calculate spin speed
    this.spinspeed = random(-0.04,0.04);
  }

  display() {
    fill(0,80,80,200);
    if (!this.startspin) {
      this.locx = lerp(this.x, this.sun.getx(), this.loccount/this.closestsun_dist);
      this.locy = lerp(this.y, this.sun.gety(), this.loccount/this.closestsun_dist);
      ellipse(this.locx,this.locy,this.rad*2,this.rad*2);
      this.loccount+=1.6;
    } else {
      this.locx = this.sun.getx() + sin(this.theta)*this.radmotion;
      this.locy = this.sun.gety() + cos(this.theta)*this.radmotion;
      ellipse(this.locx,this.locy,this.rad*2,this.rad*2);
      this.theta += this.spinspeed;

    }
    if(this.loccount>=this.distspin){
      this.startspin=true;
    }
  }
}
