#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD) # GPIO mode
GPIO.setwarnings(False) 


'''
define pins for lcd
'''
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
delay = 1
buzzer=37
GPIO.setup(buzzer, GPIO.OUT)  

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 11 #enable
LCD_D4 = 12
LCD_D5 = 13
LCD_D6 = 15
LCD_D7 = 16
IR_Sensor = 18

# we have to set input, output mode for each pins
GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT) # RS
GPIO.setup(LCD_D4, GPIO.OUT) # DB4
GPIO.setup(LCD_D5, GPIO.OUT) # DB5
GPIO.setup(LCD_D6, GPIO.OUT) # DB6
GPIO.setup(LCD_D7, GPIO.OUT) # DB7
GPIO.setup(IR_Sensor, GPIO.IN) # DB7

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line


# this function is used to initialise lcd by sending the different commands

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)


#the main purpose of this function to convert the byte data into bit and send to lcd port

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # Fisrt set RS mode to character or command 
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()

  
#used to toggle Enable pin, simulate the sensor

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

  
#print the data on lcd 

def lcd_string(message,line):
  # Send string to display
  message = message.ljust(LCD_WIDTH," ") # Ensure the message is padded to lcd_WIDTH characters(using ljust method)
 
  lcd_byte(line, LCD_CMD) # set the LCD cursor to the specified line, lcd ready to receive msg

   # iterate over each char of message and send it to lcd using lcd_byte function in LCD_CHR mode
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR) #ord function converts each char into its ASCII value

    
lcd_init()
lcd_string("welcome ",LCD_LINE_1) 
time.sleep(2)
# Define delay between readings
delay = 5

# an infinite loop until the program is running
while 1:
  # Print out results
  if GPIO.input(IR_Sensor):
   lcd_string("Obstacle Detected  ",LCD_LINE_1)
   time.sleep(1)
  else:
    lcd_string("Obstacle Removed  ",LCD_LINE_1)
    time.sleep(1)
