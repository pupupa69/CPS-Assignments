/* ADVANCED CONTROLLER GROUP CODE */
/*         DMYTRO LUTSKIV         */
/*        ALEXANDRE RAMOND        */
/*          FIONA  MATHE          */
/*          PEIZHE  YING          */


//==============================LIBRARIES=======================================

#include <PL_ADXL355.h>
#include <Joystick.h>

//==============================================================================

// Create an instance of ADXL355
// ADXL355 MOSI, MISO and SCLK pins should be connected to the correspondent
// Arduino pins and ADXL355 CS pin should be connected to pin 2
PL::ADXL355 adxl355(2);

// ADXL355 range: +/- 2 g
auto range = PL::ADXL355_Range::range2g;

//==============================DEFINITIONS=====================================

#define YAW_PIN     9
#define ASSIST_PIN  10
#define MAX_ERROR   0.2

Joystick_ Joystick(JOYSTICK_DEFAULT_REPORT_ID,JOYSTICK_TYPE_GAMEPAD,
  1, 0,                  // Button Count, Hat Switch Count
  true, true, true,     // X and Y, and Z Axis
  true, false, false,   // No Rx, Ry, or Rz
  false, true,          // No rudder yes throttle
  false, false, false);  // No accelerator, brake, or steering

float x,y;
int degreesX = 0;
int degreesY = 0;
int pot = 4;

// Setup for averaging

const int numReadings = 10;

float Xreadings[numReadings];  // the readings from the input
int XreadIndex = 0;          // the index of the current reading
float Xtotal = 0;              // the running total
float Xaverage = 0;            // the average

float Yreadings[numReadings];  // the readings from the input
int YreadIndex = 0;          // the index of the current reading
float Ytotal = 0;              // the running total
float Yaverage = 0;            // the average

//==============================FUNCTIONS=======================================

float remove_error(float axis)
{
  if(abs(axis) < MAX_ERROR)
  {
    return 0;
  }
  else if(axis > 0)
  {
    return (axis - MAX_ERROR);
  }
  else if(axis < 0)
  {
    return (axis + MAX_ERROR);
  }
}

//==============================================================================

void setup() {

  // Setup Joystick
  Joystick.begin(true);
  Joystick.setXAxisRange(-100,100);
  Joystick.setYAxisRange(-100,100);
  Joystick.setZAxisRange(-100,100);
  Joystick.setThrottleRange(0,1023);

  // Initialise all readings to zero
  for (int thisReading = 0; thisReading < numReadings; thisReading++)
  {
    Xreadings[thisReading] = 0;
    Yreadings[thisReading] = 0;
  }

  // Initialise Yaw and Assist mode pins as inputs
  pinMode(ASSIST_PIN, INPUT);
  pinMode(YAW_PIN, INPUT);

  // Initialize ADXL355
  adxl355.begin();
  // Set ADXL355 range
  adxl355.setRange(range);
  // Enable ADXL355 measurement
  adxl355.enableMeasurement();
  
  // Initialize Serial at 115200 kbps
  Serial.begin(115200);
  // Wait for Serial ready state
  while(!Serial);
}

//==============================================================================

void loop() {
  // Read and print the accelerations
  auto accelerations = adxl355.getAccelerations();
  x = accelerations.x;
  y = accelerations.y;
  int assist_button = digitalRead(ASSIST_PIN);
  int yaw_button = digitalRead(YAW_PIN);

  Serial.print("Accelerations: X: ");
  Serial.print(accelerations.x);
  Serial.print(" g, Y: ");
  Serial.print(accelerations.y);
  Serial.println(" g");

  // This bit of code removes an error from X and Y axis
  // The effect of this is that if you tilt the controller
  // just slightly in any direction, it will still read 0
  // This way you add some stability to holding the drone 
  // straight up.
  x = remove_error(x);
  y = remove_error(y);

  // This section computes the average readings of the 
  // 10 readings
  // The effect of this is reduction in jitter, and 
  // since the readings are fast (3ms), no lag is 
  // observed either.
  Xtotal = Xtotal - Xreadings[XreadIndex];
  Xreadings[XreadIndex] = x;
  Xtotal = Xtotal + Xreadings[XreadIndex];
  XreadIndex = XreadIndex + 1;
  if (XreadIndex >= numReadings) {
    XreadIndex = 0;
  }
  Xaverage = Xtotal / numReadings;

  Ytotal = Ytotal - Yreadings[YreadIndex];
  Yreadings[YreadIndex] = y;
  Ytotal = Ytotal + Yreadings[YreadIndex];
  YreadIndex = YreadIndex + 1;
  if (YreadIndex >= numReadings) {
    YreadIndex = 0;
  }
  Yaverage = Ytotal / numReadings;

  Serial.println(Xaverage);
  Serial.println(Yaverage);

  Serial.print("Assist button: ");
  Serial.println(assist_button);

  Serial.print("Yaw button: ");
  Serial.println(yaw_button);

  // Some sensitivity calibration
  // Tilting it forward is easier,
  // but tilting backward is difficult.
  // We compensate for both, since both are
  // still more difficult to do compared
  // to left-right
  if(Xaverage < 0 ){
    Xaverage = Xaverage*2;
  }
  if(Xaverage > 0 ){
    Xaverage = Xaverage*1.2;
  }

  Serial.println("");
  delay(3);

  // This bit of code implements the Yaw button
  // When the button is not pressed, operate as
  // usual.
  // When it is pressed, use right-left tilt to
  // yaw instead.
  if(!yaw_button)
  {
  Joystick.setXAxis(Xaverage*100); 
  Joystick.setYAxis(Yaverage*100);
  Joystick.setZAxis(0);
  }
  if(yaw_button)
  {
  Joystick.setXAxis(0); 
  Joystick.setYAxis(0);
  Joystick.setZAxis(Yaverage*100);
  }

  // Set potentiometer value to throttle
  // And assist SWITCH value to assist mode
  // Assist mode = Height hold
  Joystick.setThrottle(analogRead(pot));
  Joystick.setButton(0, assist_button);
}
