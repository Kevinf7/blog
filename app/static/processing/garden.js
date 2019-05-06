let flowers = []; 

function setup() {
  createCanvas(windowWidth,windowHeight);
}


function draw() {
  background(175,203,222);
  noStroke();
  fill(175,222,183);
  rect(0,height/4*3,width,height/4*3);
  for(let i=0;i<flowers.length;i++) {
    flowers[i].display();
  }
}

function mouseClicked() {
  if (mouseY > height/4*3) {
    flowers.push(new Flower(mouseX, mouseY));
  }
}


class Flower {
  constructor(x,y) {
    //stem
    this.steps = 100;
    this.count = 0;
    
    //flower
    this.growStem = true;
    this.petals = 8;
    this.stepAngle=TWO_PI/this.petals;
    this.motion=0;
    this.accel=random(-0.004, 0.004);
    this.cr=random(0,255);
    this.cg=random(0,255);
    this.cb=random(0,255);
    this.fradius=random(5,50);
    this.fshape=random(15,80);
    
    this.startX = x;
    this.startY = y;
    this.prevX = [];
    this.prevY = [];
    this.prevX[0] = x;
    this.prevY[0] = y;
    this.endX = x;
    this.endY = random(20,height/2);
    this.cx1 = random(x-1000,x+1000);
    this.cy1 = random(y+100,y+1000);
    this.cx2 = random(this.endX-1000,this.endX+1000);
    this.cy2 = random(this.endY-100, this.endY-1000);
  }
  
  display() {
    if (this.growStem) {
      //grow the stem
      this.t = this.count / this.steps;
      this.x = curvePoint(this.cx1, this.startX, this.endX, this.cx2, this.t);
      this.y = curvePoint(this.cy1, this.startY, this.endY, this.cy2, this.t);
      
      stroke("#5D3300");
      noFill();
      for(let i=0;i<this.count;i++) {
        //draw all previous except for current line
        line(this.prevX[i], this.prevY[i], this.prevX[i+1], this.prevY[i+1]); 
      }
      //draw current line
      line(this.prevX[this.count],this.prevY[this.count],this.x,this.y); 
      
      this.count++;
      if (this.count>this.steps-1) {
        this.growStem = false;
      } else {
        this.prevX[this.count] = this.x;
        this.prevY[this.count] = this.y;
      }
    } else { 
      //draw the flower
      stroke("#5D3300");
      noFill();
      curve(this.cx1, this.cy1, this.startX, this.startY, this.endX, this.endY, this.cx2, this.cy2);
      
      push();
      translate(this.endX,this.endY);
      noStroke();
      fill(this.cr,this.cg,this.cb);
      
      beginShape();
      for(let i=0;i<=this.petals;i++) {
        this.x = cos(this.stepAngle*i+this.motion)*this.fradius;
        this.y = sin(this.stepAngle*i+this.motion)*this.fradius;
        this.cx = cos((this.stepAngle*i)-(this.stepAngle/2)+this.motion)*this.fshape;
        this.cy = sin((this.stepAngle*i)-(this.stepAngle/2)+this.motion)*this.fshape;  
        
        if(i==0) {
          vertex(this.x,this.y);
        } else {
          bezierVertex(this.cx,this.cy,this.cx,this.cy,this.x,this.y);
        }
      }
      endShape(CLOSE);
      this.motion+=this.accel;
      pop();
    }
  }
}
