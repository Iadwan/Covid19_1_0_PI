import smbus
import time
import json
from urllib.request import Request, urlopen

# Define some device parameters
I2C_ADDR  = 0x3f # I2C device address
LCD_WIDTH = 16   # Maximum characters per line
# for Rasraspberrypi display config I used http://www.raspberrypi-spy.co.uk/ by Matt Hawkins
# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def main():
  # Main program block

  # Initialise display
  lcd_init()



  

  while True:

	## We Read from this Public API 

	complete_url = "https://api.thevirustracker.com/free-api?countryTotal=JO"

	#Request the URL and decode
	
	req = Request(complete_url, headers={'User-Agent': 'Mozilla/5.0'})
	
	#json method of response object  

	webpage = urlopen(req).read().decode()
	# convert json data into python data 
	jsonget = json.loads(webpage)
	
	if jsonget["stat"] != "bad": 
	  
      	    # Get the value of "countrydata" 

	    country_data = jsonget["countrydata"] 

 
	    total_cases = country_data[0]["total_cases"]
	 
	    total_recovered = country_data[0]["total_recovered"] 
  
	    total_deaths = country_data[0]["total_deaths"] 


	    date_time = datetime.datetime.now()
	
	
	    lcd_string("COVID19 Infects:",LCD_LINE_1)
	    lcd_string("By Ibrahim.....",LCD_LINE_2)
	
	    time.sleep(3)
	
	    lcd_string("Date : ",LCD_LINE_1)
	    lcd_string(date_time,LCD_LINE_2)
	
	    time.sleep(3)
		
		
	    lcd_string("Jordan-Confirmed",LCD_LINE_1)
	    lcd_string(total_cases,LCD_LINE_2)
	
	    time.sleep(3)


	    lcd_string("Jordan-Recovered",LCD_LINE_1)
	    lcd_string(total_recovered,LCD_LINE_2)
		
	    time.sleep(3)
  
	    lcd_string("Jordan-Death:",LCD_LINE_1)
	    lcd_string(total_deaths,LCD_LINE_2)

	    time.sleep(3)

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)

ra