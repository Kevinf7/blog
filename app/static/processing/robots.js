var rbod = [];
var rhead = [];
var rarms = [];

function setup() {
  createCanvas(windowWidth,windowHeight);
  
  counter=0;
  for(let i=0;i<12;i++) {
    for(let j=0;j<6;j++) {
      rbod[counter] = new robotBody((i*width/12)+66, (j*height/6)+random(-10,10), 40, 10, round(6+random(-4,4)));
      rhead[counter] = new robotHead(rbod[counter]);
      rarms[counter] = new robotArms(rbod[counter]);
      counter++;
    }
  }
}

function draw() {
  background(255);
  counter=0;
  for(i=0;i<12;i++) {
    for(let j=0;j<6;j++) {
      rbod[counter].display();
      rhead[counter].display();
      rarms[counter].display();
      counter++;
    }
  }
}

function mouseClicked() {
   counter=0;
   for(let i=0;i<12;i++) {
    for(let j=0;j<6;j++) {
      rbod[counter] = new robotBody((i*width/12)+66, (j*height/6)+random(-10,10), 40, 10, round(6+random(-4,4)));
      rhead[counter] = new robotHead(rbod[counter]);
      rarms[counter] = new robotArms(rbod[counter]);
      counter++;
    }
  }
}


class robotBody {
  
  constructor(x_,y_,w_,h_,num_seg_) {
    
    this.num_seg = num_seg_;
    this.rotate = [];
    this.x = [];
    this.y = [];
    this.w = [];
    this.h = [];
    
    for(let i=0;i<this.num_seg;i++) {
      this.rotate[i]=random(-6,6);
      this.w[i]=w_+random(w_/3*-1,w_/3);
      this.h[i]=h_+random(-4,4);
      this.x[i]=x_+random(-4,4);
      if (i==0) {
        this.y[i]=y_+random(-1,1)-2;
      } else {
        this.y[i]=this.y[i-1]+random(-1,1)+this.h[i-1]-2;        
      }
    }
    this.w = sort(this.w);
    this.w = reverse(this.w);
    fill(202,205,175);
    stroke(0);
    rectMode(CENTER);
  }
  
  display() { 
    for(let i=0;i<this.num_seg;i++) {
      push();
      translate(this.x[i],this.y[i]);
      rotate(radians(this.rotate[i]));
      rect(0,0,this.w[i],this.h[i],16);
      pop(); 
    }
  }
  
  get_x(seg) {
    if (seg<1||seg>this.num_seg) {
      return this.x[0];
    } else {
      return this.x[seg-1];
    }
  }
  
  get_y(seg) {
    if (seg<1||seg>this.num_seg) {
      return this.y[0];
    } else {
      return this.y[seg-1];
    }
  }
  
  get_h(seg) {
    if (seg<1||seg>this.num_seg) {
      return this.h[0];
    } else {
      return this.h[seg-1];
    }
  }
  
  get_w(seg) {
    if (seg<1||seg>this.num_seg) {
      return this.w[0];
    } else {
      return this.w[seg-1];
    }
  }
  
  get_num_seg() {
    return this.num_seg;
  }
}

class robotHead {
  
  constructor(rbod) {
    this.x=rbod.get_x(0);
    this.y=rbod.get_y(0)-rbod.get_h(0);    
    this.w=rbod.get_w(0)*0.7;
    this.h=rbod.get_h(0);
    this.rotate=random(-6,6);
    
    fill(202,205,175);
    stroke(0);
    rectMode(CENTER);
  }
  
  display() {
    push();
    translate(this.x,this.y);
    rotate(radians(this.rotate));
    rect(0,0,this.w,this.h,16);
    fill(0);
    ellipse(-this.w/4,-this.h/4,3,3);
    ellipse(this.w/4,-this.h/4,3,3);
    line(0,-this.h/2,-this.w/6,-this.h);
    line(0,-this.h/2,this.w/6,-this.h); 
    fill(202,205,175);
    pop();
  }
}

class robotArms {
  
  constructor(rbod) {
    this.w = rbod.get_w(0);
    this.left_x=rbod.get_x(0)-this.w/2;
    this.right_x=rbod.get_x(0)+this.w/2;
    this.left_y=rbod.get_y(0);
    this.right_y=rbod.get_y(0);
    
    this.jleft_x = this.left_x - 20 + random(-4,4);
    this.jleft_y = this.left_y + 30 + random(-6,6);
    this.jright_x = this.right_x + 20 + random(-4,4);
    this.jright_y = this.right_y + 30 + random(-6,6);
    
    this.fleft_x = this.jleft_x - 6 + random(-2,2);
    this.fleft_y = (this.jleft_y + 40 + random(-4,4));
    this.fright_x = this.jright_x + 6 + random(-2,2);
    this.fright_y = (this.jright_y + 40 + random(-4,4)) ;
  }
  
  display() {
    line(this.left_x,this.left_y,this.jleft_x,this.jleft_y);
    line(this.jleft_x,this.jleft_y,this.fleft_x,this.fleft_y);
    
    line(this.right_x,this.right_y,this.jright_x,this.jright_y);
    line(this.jright_x,this.jright_y,this.fright_x,this.fright_y);
  }
}
