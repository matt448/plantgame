// Limit switch pins
int topLimitState = 0;
int bottomLimitState = 0;
const int topLimitPin = 11;
const int bottomLimitPin = 10;

// Stepper motor pins
const int enablePin = 5;
const int dirPin = 2;
const int stepPin = 3;
const int ms1Pin = 6;
const int ms2Pin = 4;
const int ledPin = 13;

// Motor constants
const int speed1 = 1;
const int speed2 = 500;
const int speed3 = 750;
const int speed4 = 1000;

// Calibration values
int stepsMin = 0;  // minimum recorded value
int stepsMax = 0;  // maximum recorded value
int curSteps = 0;
boolean calibrated = false;
boolean gameOver = false;

enum MicroSteps {
  FULL,
  HALF,
  QUARTER,
  EIGHTH
};

enum Direction {
  UP,
  DOWN
};

void setup()
{
  pinMode(topLimitPin, INPUT);  //up limit switch
  pinMode(bottomLimitPin, INPUT);  //down limit switch

  pinMode(dirPin, OUTPUT);
  pinMode(stepPin, OUTPUT);
  pinMode(enablePin, OUTPUT);
  pinMode(ms1Pin, OUTPUT);
  pinMode(ms2Pin, OUTPUT);
  pinMode(ledPin, OUTPUT);

  digitalWrite(ledPin, LOW); // Clear LED

  // Initialize the Serial port:
  Serial.begin(9600);

  // Reset stepper motor
  initStepper();
}

void loop()
{
  topLimitState = digitalRead(topLimitPin);
  bottomLimitState = digitalRead(bottomLimitPin);

  // Calibrate, then move to home
  calibrateStepper();

  // Start game
  int i;

  if (gameOver == false) {
    for (i = 0; i < random(stepsMax / 2, stepsMax); i++)
    {
      stepMotor(random(100, 200), UP, FULL);
    }
    for (i = 0; i < random(stepsMax / 4, stepsMax / 2); i++)
    {
      stepMotor(random(200, 300), DOWN, FULL);
    }
    for (i = 0; i < random(stepsMax / 8, stepsMax / 4); i++)
    {
      stepMotor(random(300, 400), UP, FULL);
    }
    gameOver = true;
    Serial.print("Final position: "); Serial.println(curSteps);
    float score = ((float)curSteps / (float)stepsMax) * 100.0;
    Serial.print("You made it "); Serial.print(score); Serial.println("% to target");
    Serial.println("Game Over!");
  }
}

void stepMotor(int speed)
{
  stepMotor(speed, UP, FULL);
}

void stepMotor(int speed, Direction direction, MicroSteps microStep)
{
  if (speed == 0) {
    return;
  }
  stepDirection(direction);
  stepRate(microStep);

  digitalWrite(enablePin, LOW);  // Enable motor
  digitalWrite(ledPin, HIGH);
  digitalWrite(stepPin, LOW);  // This LOW to HIGH change is what creates the
  delay(1);
  digitalWrite(stepPin, HIGH); // "Rising Edge" so the driver knows to when to step.
  delay(1);
  digitalWrite(ledPin, LOW);
  digitalWrite(enablePin, HIGH);  // Disable motor
  delayMicroseconds(speed);

  if (direction == UP) {
    curSteps++;
  } else {
    curSteps--;
  }
}

void initStepper() {
  digitalWrite(enablePin, HIGH);  // Disable motor
  stepDirection(UP); // Default to upward direction
  stepRate(FULL);  // Stepper start at full step
}

void calibrateStepper() {
  if (calibrated == true) {
    return;
  }
  // Reset to bottom position
  while (digitalRead(bottomLimitPin) == LOW) {
    stepMotor(speed1, DOWN, FULL);
  }
  curSteps = 0;
  while (digitalRead(topLimitPin) == LOW) {
    stepMotor(speed1, UP, FULL);
    if (curSteps > stepsMax) {
      stepsMax = curSteps;
    }
  }
  Serial.print("Total steps: "); Serial.println(stepsMax);
  calibrated = true;
  // Reset to bottom position
  while (digitalRead(bottomLimitPin) == LOW) {
    stepMotor(speed1, DOWN, FULL);
  }
  Serial.println("Game Ready!");
  delay(1500);
}

void stepDirection(Direction direction) {
  switch (direction) {
    case UP:
      digitalWrite(dirPin, HIGH);
      break;
    case DOWN:
      digitalWrite(dirPin, LOW);
      break;
    default:
      digitalWrite(dirPin, HIGH);
      break;
  }
}

void stepRate(MicroSteps microStep) {
  switch (microStep) {
    case FULL:
      // Full step
      digitalWrite(ms1Pin, LOW);
      digitalWrite(ms2Pin, LOW);
      break;
    case HALF:
      // Half step
      digitalWrite(ms1Pin, HIGH);
      digitalWrite(ms2Pin, LOW);
      break;
    case QUARTER:
      // Quarter step
      digitalWrite(ms1Pin, LOW);
      digitalWrite(ms2Pin, HIGH);
      break;
    case EIGHTH:
      // Eighth step
      digitalWrite(ms1Pin, HIGH);
      digitalWrite(ms2Pin, HIGH);
      break;
    default:
      // Full step
      digitalWrite(ms1Pin, LOW);
      digitalWrite(ms2Pin, LOW);
      break;
  }
}
