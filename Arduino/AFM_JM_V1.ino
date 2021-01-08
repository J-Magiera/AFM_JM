
void (*CLI[])(void) = {&measure, &calibrate, &setParameters};

const int dirPin_x = 6;
const int stepPin_x = 7;

const int dirPin_y = 4;
const int stepPin_y = 5;

const int dirPin_z = 9;
const int stepPin_z = 8;

const int x2_end = 40;
const int x1_end = 38;
const int y2_end = 36;
const int y1_end = 34;

int xPos = 0;
int yPos = 0;
int xSize = 0;
int ySize = 0;

int data[4] = {};


const char packageLeft = '<';
const char packageRight = '>';


 

const int opto[12] = {A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11};

void setup() {
  Serial.begin(115200);
 
  pinMode(dirPin_x, OUTPUT);
  pinMode(stepPin_x, OUTPUT);
  pinMode(dirPin_z, OUTPUT);
  pinMode(stepPin_z, OUTPUT);
  pinMode(dirPin_y, OUTPUT);
  pinMode(stepPin_y, OUTPUT);

  pinMode(x1_end, INPUT);
  pinMode(x2_end, INPUT);
  pinMode(y1_end, INPUT);
  pinMode(y2_end, INPUT);


}

void loop() 
{

 if(Serial.available() > 0)
 {
  int command = Serial.read() - 48;
  CLI[command]();
 }
 
}
void d2()
{
  gotoXY(0,0);
}
void setParameters()
{
  int d = 0;

  for(int i = 0; i < 4; i++){
  while(!Serial.available());
  while(Serial.available())
  {
    d = processData();
  }
  data[i] = d;
  }

  gotoXY(data[0], data[1]);
  setField(data[2], data[3]);
  
}

int processData()
{
  static int receivedNumber = 0;
  byte  c = Serial.read();
    
  switch(c)
  {
    case '>':
      break;

    case '<':
      receivedNumber = 0;
      break;
     
    case '0' ... '9': 
      receivedNumber *= 10;
      receivedNumber += c - '0';
      break;

  }

  return receivedNumber;
}

void setField(int x, int y)
{
  int x1 = xPos + x;
  if(xSize >= x1) xSize = x1;
  int y1 = yPos + y;
  if(ySize >= y1) ySize = y1;

}

void gotoXY(int x, int y)
{
  if(x >= xPos)
  {
    for(; xPos < x; xPos++)
    {
      stepX(0);
    }
  }
  else
  {
    for(; xPos > x; xPos--)
    {
      stepX(1);
    }
  }

  if(y >= yPos)
  {
    for(; yPos < y; yPos++)
    {
      stepY(1);
    }
  }
  else
  {
    for(; yPos > y; yPos--)
    {
      stepY(0); 
    }
  }
}
 
void rotateHalfZ()
{
  rotate(stepPin_z, dirPin_z, 4, 1);
}

void stepX(bool dir)
{
  rotate(stepPin_x, dirPin_x, 2, dir);
}

void stepY(bool dir)
{
  rotate(stepPin_y, dirPin_y, 2, dir);
}

void rotate(int stepPin, int dirPin,int value, bool dir)
{
  digitalWrite(dirPin, dir);

  for(int j = 0; j < value*400; j++)
  {
    digitalWrite(stepPin, HIGH); 
    delayMicroseconds(50); 
    digitalWrite(stepPin, LOW); 
    delayMicroseconds(50); 
  }
  
}

void Read(int x, int y)
{
  int z = 0;
  rotateHalfZ();
 
  delay(80); 
  
  for(int i=1;i<13;i++)
    {  
      if(analogRead(opto[i-1]) > 700)
      {
        z = i--;
        break;    
      }      
    }
  
    Serial.print(' ');
    Serial.print(x);
    Serial.print(' ');
    Serial.print(y);
    Serial.print(' ');
    Serial.print(z);
    Serial.print(' ');
    Serial.print("\n");
 
    rotateHalfZ();
}

void measure()
{
  bool d = 0;
  for(; xPos < xSize; xPos++)
  {
    d = !d;
    if(0 == d)
    {
      for(; yPos >= 0; yPos--)
      {
        
        Read(xPos, yPos);
        stepY(d);    
        while(!(Serial.read() == '6')); 
      }
      yPos++;
    }
    else if (1 == d)
    {
      
      for(; yPos < ySize; yPos++)
      {
        Read(xPos,  yPos);
        stepY(d);
        while(!(Serial.read() == '6'));
      }
      yPos--;
    }
    stepX(0);
  }
  Serial.print('k');  
}

void calibrate()
{
  calibrate_x();
  calibrate_y();
}

void calibrate_x()
{
  xSize = 0;
  while(!digitalRead(x1_end))
  {
   stepX(0); 
  }
  while(!digitalRead(x2_end))
  {
    xSize++;
    stepX(1);
  }
}

void calibrate_y()
{
  ySize = 0;
  while(!digitalRead(y2_end))
  {
   stepY(1); 
  }
  while(!digitalRead(y1_end))
  {
    ySize++;
    stepY(0);
  }
}
