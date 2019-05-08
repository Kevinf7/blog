var snake;
var food;
var NUM_POI;
var MIN_RATE;
var MAX_RATE;
var SCL;
var poison = [];
var keywidth;
var keyheight;
var rate;
var err;
var wait;
var start;

function setup() {
  createCanvas(windowWidth,windowHeight);
  NUM_POI = 5;
  MIN_RATE = 5;
  MAX_RATE = 20;
  SCL = 20;  
  wait=0;
  rate=5;
  start=true;
  frameRate(rate);   
  snake = new Snake();
  food = new Food();
  for (var i=0; i<NUM_POI; i++) {
    poison[i] = new Poison();
  }
  keywidth=width/3;
  keyheight=height/3;
}

function init() {
  wait=0;
  rate=5;
  start=true;
  frameRate(rate);
}

function draw() { 
  if (snake.alive) {
    background(0);
    stroke(96);
    
    line(keywidth, 0, keywidth, height);
    line(width-keywidth, 0, width-keywidth, height);
    line(0, keyheight, width, keyheight);
    line(0, height-keyheight, width, height-keyheight);

    noStroke();
    textSize(32); 
    fill(255);
    textAlign(RIGHT); 
    text(snake.points, width-50,height-50);
    
    snake.update();
    snake.show();
    for (var i=0; i<NUM_POI; i++) {
      poison[i].show();
    }
    food.show();
    
    if (snake.isEat(food)) {
      if (food.yum) {
        snake.ate(0);
      } else {
        snake.ate(1);
      }
      
      food.init();
      var inc = snake.eaten % 2;
      if (inc == 0 && !start) {
        if (rate<=MAX_RATE) {
          rate=rate+0.3;
          frameRate(rate);
          snake.incLen(snake.SNK_LEN);
        }
      } else {
        start=false;
      }
    }
    
    for (let i=0; i<NUM_POI; i++) {
      if (snake.isEat(poison[i])) {
        snake.ate(2);
        poison[i].init();
      }
    }
    
    var r = snake.chkAlive();
    if (r==1) {
      err="You ate your tail. You died!";
      setWait();
    } else if (r==2) {
      err="You hit the wall. You died!";
      setWait();
    }
    
    
  } else {
    background(255,0,100);
    textSize(64); 
    fill(255);
    textAlign(CENTER); 
    text("Snake Game", width/2, height/2 - 100);
    textSize(32);
    text(err, width/2, height/2);
    text("Final Score: " + snake.points, width/2, height/2 + 50);
    text("Game by Kevin Foong", width/2, height/2 + 100);
    if (!chkWait()) {
       fill(64);
       text("Touch screen to start", width/2, height/2 + 150);
    }
  }
}

function mouseClicked() {
  if (snake.alive) {
    /*
    if (mouseX < keywidth && mouseY > keyheight && mouseY < height - keyheight ) {
      snake.setDir(2);
    } else if (mouseX < width && mouseX > width-keywidth && mouseY > keyheight && mouseY < height - keyheight ) {
      snake.setDir(3);
    } else if (mouseX > keywidth && mouseX < width-keywidth && mouseY < keyheight) {
      snake.setDir(0);
    } else if (mouseX > keywidth && mouseX < width-keywidth && mouseY < height && mouseY > height-keyheight) {
      snake.setDir(1);
    }*/
    if (mouseX < keywidth && (snake.direction == 0 || snake.direction == 1 )) {
      snake.setDir(2);
    } else if (mouseX > width-keywidth &&  (snake.direction == 0 || snake.direction == 1 )) {
      snake.setDir(3);
    } else if (mouseY > height - keyheight && (snake.direction == 2 || snake.direction == 3 )) {
      snake.setDir(1);
    } else if (mouseY < keyheight && (snake.direction == 2 || snake.direction == 3 )) {
      snake.setDir(0);
    }
  } else {
      if (!chkWait()) {
        init();
        snake = new Snake();
        for (var i=0; i<NUM_POI; i++) {
          poison[i] = new Poison();
        }
        food = new Food();
      }
  }
}
  
function setWait() {
  wait=millis()/1000;
}

function chkWait() {
  if (wait==0) {
    return false;
  }
  var now = millis()/1000;
  if (now-wait > 2) {
    return false;
  } else {
    return true;
  }
}

//Snake
class Snake {
  constructor() {
    this.MAX_LEN=60;
    this.SNK_LEN=3;
    this.eaten=0;    
    this.points=0;
    this.alive=true;
    this.ploc = createVector(this.SNK_LEN-2*SCL,0);
    this.body = [];
    var v = createVector((this.SNK_LEN-1)*SCL,0);
    this.body.push(v);
    this.setDir(3);
    this.incLen(this.SNK_LEN-1);
  }

  update() { 
    if (this.body.length>1) {
      for (var i=this.body.length-1; i>0; i--) {
        this.body[i].x = this.body[i-1].x;
        this.body[i].y = this.body[i-1].y;
      }    
    }
    this.ploc.x = this.body[0].x;
    this.ploc.y = this.body[0].y;
      
    this.body[0].x=this.body[0].x+this.xspeed*SCL;
    this.body[0].y=this.body[0].y+this.yspeed*SCL;
  }
      
  show() {
    fill(255,255,100);
    for (var i=0; i<this.body.length; i++) {
      rect(this.body[i].x, this.body[i].y, SCL, SCL);
    }
  }
  
  incLen(t) {
    if (this.body.length < this.MAX_LEN) {
      for (var i=0; i<t; i++) {         
        this.body.push(createVector(this.ploc.x,this.ploc.y));
      }
    }
  }

  isEat(et) {
    if (dist(this.body[0].x, this.body[0].y, et.getX(), et.getY()) <2) {
      return true;
    } else {
      return false;
    }
  }

  chkAlive() {
    for (var i=1; i<this.body.length; i++) {
      if (dist(this.body[0].x, this.body[0].y, this.body[i].x, this.body[i].y) <1) { 
        this.alive=false;
        return 1;
      }
    }
    if (this.body[0].x<0 || this.body[0].x>width-SCL || this.body[0].y<0 || this.body[0].y>height-SCL){
      this.alive=false;
      return 2;
    }
    return 0;
  }
  
  ate(a) {
    if (a==0) { //yum
      this.eaten++;
      this.points=this.points+2;
    } else if (a==1) { // normal food
      this.eaten++;
      this.points=this.points+1;
    } else if (a==2) { //poison
      this.points=this.points-3;
    }
  }
  
  setDir(d) {
    if (d==0) {
      this.xspeed = 0;
      this.yspeed = -1;
      this.direction=0;
    } else if (d==1) {
      this.xspeed = 0;
      this.yspeed = 1;
      this.direction=1;
    } else if (d==2) {
      this.xspeed = -1;
      this.yspeed = 0;
      this.direction=2;
    } else if (d==3) {
      this.xspeed = 1;
      this.yspeed = 0;
      this.direction=3;
    } 
  }
}

//Poison
class Poison {
  constructor() {
    var rows = floor(width/SCL);
    var cols = floor(height/SCL);
    this.x = floor(random(rows));
    this.y = floor(random(cols));
    this.x=this.x*SCL;
    this.y=this.y*SCL; 
    this.start=millis()/1000;
  }

  init() {
    var rows = floor(width/SCL);
    var cols = floor(height/SCL);
    this.x = floor(random(rows));
    this.y = floor(random(cols));
    this.x=this.x*SCL;
    this.y=this.y*SCL; 
    this.start=millis()/1000; 
  }

  show() {
    var now=millis()/1000;
    if (now-this.start > 20) {
      this.init();
    }
    fill(100,0,255);
    rect(this.x,this.y,SCL,SCL);
  }
  
  getX() {
    return this.x;
  }
  
  getY() {
    return this.y;
  }
}

//Food
class Food {
  constructor() {
    var rows = floor(width/SCL);
    var cols = floor(height/SCL);
    this.x = floor(random(rows));
    this.y = floor(random(cols));
    this.x=this.x*SCL;
    this.y=this.y*SCL;
    this.yum=true;
    this.start=millis()/1000;
  }

  init() {
    var rows = floor(width/SCL);
    var cols = floor(height/SCL);
    this.x = floor(random(rows));
    this.y = floor(random(cols));
    this.x=this.x*SCL;
    this.y=this.y*SCL;
    this.yum=true;
    this.start=millis()/1000;       
  }
    
  show() {
    var irate = map(rate,MIN_RATE,MAX_RATE,11,7);
    var yrate = map(rate,MIN_RATE,MAX_RATE,4,3);
    var now=millis()/1000;
    if (now-this.start > irate) {
      this.init();
    }
    if (this.yum) {
      if (now-this.start > yrate) {
        this.yum=false;
      }
      fill(100,255,0);
    } else {
      fill(255,0,100);
    }
    rect(this.x,this.y,SCL,SCL);
  }
    
  getX() {
    return this.x;
  }
  
  getY() {
    return this.y;
  }
}
