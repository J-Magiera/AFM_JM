
void (*CLI[])(void) = {&measure, &calibrate, &singleMeasure};

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

int xSteps = 42;
int ySteps = 42;
int xPos = 0;
int yPos = 0;
int j = 10;


 

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
  for(int x = 0; x < 50; x++)
  {
    d = !d;
    for(int y = 0; y < yPos; y++)
    {
      if(d)
      {
        Read(x, y);
      }
      else
      {
        Read(x, yPos - 1 - y);
      }
      delay(40);
      while(!(Serial.read() == '6'));
      stepY(d);
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
  xPos = 0;
  while(!digitalRead(x1_end))
  {
   stepX(0); 
  }
  while(!digitalRead(x2_end))
  {
    xPos++;
    stepX(1);
  }
}

void calibrate_y()
{
  yPos = 0;
  while(!digitalRead(y2_end))
  {
   stepY(1); 
  }
  while(!digitalRead(y1_end))
  {
    yPos++;
    stepY(0);
  }
}

void singleMeasure()
{
  j++;
  Read(j, j+1);
}
