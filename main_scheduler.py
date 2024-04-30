import schedule
import time
#for threading
import threading

# for BME280 Sensors:
import smbus2
import bme280
import os
import pytz

# BME280 sensor address (default address)
address = 0x76
address2 = 0x77
# Initialize I2C bus
bus = smbus2.SMBus(1)
# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address) 
calibration_params2 = bme280.load_calibration_params(bus, address2)

# for relay control
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
RELAIS_1_GPIO = 4
RELAIS_2_GPIO = 17
RELAIS_3_GPIO = 27
RELAIS_4_GPIO = 22

# define functions

# read sensor values and return 
def getSensors():
	#print("Reading Sensor Values...")
	
	# Read sensor data 
	data = bme280.sample(bus, address, calibration_params) 
	data2 = bme280.sample(bus, address2, calibration_params2)
	# Extract temperature, pressure, humidity, and corresponding timestamp
	timestamp = data.timestamp
	temperature_celsius = data.temperature
	humidity = data.humidity
	pressure = data.pressure
	
	timestamp2 = data2.timestamp
	temperature_celsius2 = data2.temperature
	humidity2 = data2.humidity
	pressure2 = data2.pressure
	timestamp2 = data2.timestamp
	
	# Adjust timezone
	# Define the timezone you want to use (list of timezones: https://gist.github.com/mjrulesamrat/0c1f7de951d3c508fb3a20b4b0b33a98)
	desired_timezone = pytz.timezone('Europe/Berlin')  # Replace with your desired timezone
	# Convert the datetime to the desired timezone
	timestamp_tz = timestamp.replace(tzinfo=pytz.utc).astimezone(desired_timezone)
	timestamp_out = timestamp_tz.strftime('%H:%M:%S %d/%m/%Y')
	#timestamp_out = timestamp_tz.strftime('%H:%M:%d %S/%m/%Y')
	#%H:%M:%d %S/%m/%Y
	# Convert temperature to Fahrenheit
	#temperature_fahrenheit = (temperature_celsius * 9/5) + 32
	#temperature_fahrenheit2 = (temperature_celsius2 * 9/5) + 32
	# Print the readings
	#print(timestamp_tz.strftime('%H:%M:%S %d/%m/%Y'))
	#print("Temp1={0:0.1f}ºC, Temp1={1:0.1f}ºF, Humidity1={2:0.1f}%, Pressure1={3:0.2f}hPa".format(temperature_celsius, temperature_fahrenheit, humidity, pressure))
	#print("Temp2={0:0.1f}ºC, Temp2={1:0.1f}ºF, Humidity2={2:0.1f}%, Pressure2={3:0.2f}hPa".format(temperature_celsius2, temperature_fahrenheit2, humidity2, pressure2))
	valueList = [timestamp_out, temperature_celsius, temperature_celsius2, humidity, humidity2, pressure, pressure2]
	return valueList

def logdata():
	import os
	import pytz
	# Check if the file exists before opening it in 'a' mode (append mode)
	file_exists = os.path.isfile('sensor_readings_bme280.csv')
	file = open('sensor_readings_bme280.csv', 'a')
	
	# Write the header to the file if the file does not exist
	if not file_exists:
		file.write('Date,Temp1,Temp2,humidity1,humidity2,pressure1,pressure2\n')
	# Read data
	data = getSensors()
	# Save data in *.csv file
	file.write(data[0] + "," + str(round(data[1],2))+ "," + str(round(data[2],2))+ "," + str(round(data[3],2))+ "," + str(round(data[4],2))+ "," + str(round(data[5],2))+ "," + str(round(data[6],2))+"\n")
	file.close()

def logdatalong():
	import os
	import pytz
	# Check if the file exists before opening it in 'a' mode (append mode)
	file_exists = os.path.isfile('sensor_readings_bme280_long.csv')
	# Write the header to the file if the file does not exist
	if not file_exists:
		with open('sensor_readings_bme280_long.csv', 'a') as file:
			file.write('date,value,type\n')
	
	# Read data
	data = getSensors()
	# Save data in *.csv file
	#file = open('sensor_readings_bme280_long.csv', 'a')
	#file.write(data[0] + "," + str(round(data[1],2))+ ", Temp1\n" + data[0] + "," + str(round(data[2],2))+ ", Temp2\n" + data[0] + "," + str(round(data[3],2))+ ", Humid1\n" +  data[0] + "," + str(round(data[4],2))+ ", Humid2\n" + data[0] + "," + str(round(data[5],2))+ ", Press1\n" + data[0] + "," + str(round(data[6],2))+ ", Press2\n") 
	#file.close()
	with open('sensor_readings_bme280_long.csv', 'a') as file:
	    file.write(data[0] + "," + str(round(data[1],2))+ ",Temp1\n" + data[0] + "," + str(round(data[2],2))+ ",Temp2\n" + data[0] + "," + str(round(data[3],2))+ ",Humid1\n" +  data[0] + "," + str(round(data[4],2))+ ",Humid2\n" + data[0] + "," + str(round(data[5],2))+ ",Press1\n" + data[0] + "," + str(round(data[6],2))+ ",Press2\n")
			
# Turn on / off Relais 1
def R1on():
	GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
	print("R1 on")
	GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on
#	GPIO.cleanup()  

def R1off():
	GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
	print("R1 off")
	GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # off

# Turn on / off Relais 2
def R2on():
	GPIO.setup(RELAIS_2_GPIO, GPIO.OUT) # GPIO Assign mode
	print("R2 on")
	GPIO.output(RELAIS_2_GPIO, GPIO.HIGH) # on

def R2off():
	GPIO.setup(RELAIS_2_GPIO, GPIO.OUT) # GPIO Assign mode
	print("R2 off")
	GPIO.output(RELAIS_2_GPIO, GPIO.LOW) # off

# Turn on / off Relais 3
def R3on():
	GPIO.setup(RELAIS_3_GPIO, GPIO.OUT) # GPIO Assign mode
	print("R3 on")
	GPIO.output(RELAIS_3_GPIO, GPIO.HIGH) # on

def R3off():
	GPIO.setup(RELAIS_3_GPIO, GPIO.OUT) # GPIO Assign mode
	print("R3 off")
	GPIO.output(RELAIS_3_GPIO, GPIO.LOW) # off

# Turn on / off Relais 4
def R4on():
	GPIO.setup(RELAIS_4_GPIO, GPIO.OUT) # GPIO Assign mode
	print("R4 on")
	GPIO.output(RELAIS_4_GPIO, GPIO.HIGH) # on

def R4off():
	GPIO.setup(RELAIS_4_GPIO, GPIO.OUT) # GPIO Assign mode
	print("R4 off")
	GPIO.output(RELAIS_4_GPIO, GPIO.LOW) # off

def relaistest():
	R1on()
	R2on()
	R3on()
	R4on()
	time.sleep(5)
	R1off()
	R2off()
	R3off()
	R4off()
	

# get and print Sensorvalues to console
def printSensor():
	values = getSensors()
	# Print the readings
	print("Zeit:", values[0])
	#print("Sensor 1: Temp: ", values[1],"Humid: ",values[3], "Pressure: ",values[5] )
	#print("Sensor 2: Temp: ", values[2],"Humid: ",values[4], "Pressure: ",values[6] )
	#print(values[0])
	
	print("Sensor 1: Temperatur = {0:0.1f}ºC ".format(values[1]) + "Humidity = {0:0.1f}% ".format(values[3]) + "Pressure = {0:0.2f}hPa".format(values[5]))
	print("Sensor 2: Temperatur = {0:0.1f}ºC ".format(values[2]) + "Humidity = {0:0.1f}% ".format(values[4]) + "Pressure = {0:0.2f}hPa".format(values[6]))
	
# Check if Humidity is to low / high
def checker():
	values = getSensors()
	print("Checking Values...")
	#print(values[1])
	
	if values[3]>50:
		print("Humidity over 50 %")
	if values[3]<30:
		print("Humidity under 30 %")
		#R1off()
		
		
def humidon(duration=30):
	print("Humindifier on for "+ str(duration) +" seconds")
	R2on()
	time.sleep(3)
	R3on()
	time.sleep(1)
	R3off()
	time.sleep(duration)
	R2off()
	print("Humindifier off")
	
def windon(duration = 30):
	print("Wind on for " + str(duration)+ " seconds")
	R1on()
	time.sleep(duration)
	R1off()

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(10).seconds.do(run_threaded, printSensor)
schedule.every(20).seconds.do(run_threaded, logdatalong)
#schedule.every(60).seconds.do(run_threaded, humidon)
#schedule.every(60).seconds.do(run_threaded, windon)

#schedule.every(1).seconds.do(getSensors)
#schedule.every(10).seconds.do(printSensor)
#schedule.every(10).seconds.do(logdatalong)
#schedule.every(3).seconds.do(logdata)
#schedule.every(10).seconds.do(checker)
#schedule.every(60).seconds.do(humidon, duration=30)
#schedule.every(6).seconds.do(R1off)


while True:
		schedule.run_pending()
