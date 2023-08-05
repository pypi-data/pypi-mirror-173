import serial
import struct
import queue
from enum import Enum
from serial.tools import list_ports
import time, os
import HeartRate
from HeartRate import HEART_RATE_RESULT_STATUS
import threading
from threading import Lock, Thread


# Kiwrious sensors and its type code
class KiwriousSensor(Enum):

    CONDUCTIVITY = "04"
    AIR = "06"
    HUMIDITY = "07"
    TEMPERATURE = "09"
    LIGHT = "0b"
    HEARTBEAT = "05"

# Kiwrious sensors and its units, each sensors has two units
class SensorUnits(Enum):

    RESISTANCE = 'Ω'
    CONDUCTIVITY = 'μS/cm'
    TEMPERATURE = '°C'
    HUMIDITY = '%'
    VOC = 'tVOC'
    CO2 = 'ppb'
    LUX = 'lux'
    UV_INDEX = 'uv index'
    IR_Temperature = 'IR Temperature'
    Ambient_temperature = 'Ambient temperature'
    BPM = 'bpm'

# A class that represents a piece of sensor data
class SensorData:

    def __init__(self,sensor_type,data_value,data_unit):
        self.sensor_type = sensor_type
        self.data_value = data_value
        self.data_unit = data_unit
    
    def __repr__(self):
        return 'SensorData{sensor_type = ' + str(self.sensor_type) + ', data_value = ' + str(self.data_value) + '; data_unit = ' + str(self.data_unit) + '}'

class NotKiwriousException(Exception):
    """ Raised when queried sensor is not connected """
    pass

# ______________________________________________________________________________
class KiwriousService:
    ''' A service that connects to the sensors and mainipulate sensor datas. '''

    def __init__(self):
        # State to control servive's child threads
        self.__alive = False
        # Record current connecting sensers
        self.__connected_sensors_list = []         #[sensor_type,...]

        self.__data_collector_index = [KiwriousSensor.CONDUCTIVITY,KiwriousSensor.AIR,KiwriousSensor.HUMIDITY,KiwriousSensor.TEMPERATURE,KiwriousSensor.LIGHT,KiwriousSensor.HEARTBEAT]
        self.__data_collector_raw = [None,None,None,None,None,None,None]
        self.__data_collector = [None,None,None,None,None,None,None]
        # Record opition to record the raw data from sensor, defaut is False
        self.__record = False
        self.__data_repo = [[],[],[],[],[],[]]

        # The container of passing data from user_consemer to user
        self.__connected_ports = []
        self.__connecting = False
        self.__timeout = 15

        # There is one listener for each sensor, they monitor major change in sensors
        self.__listeners = dict()
        for sensor in KiwriousSensor:
            # Each listener stores [is_activated_boolean, previous_row_of_data, current_row_of_data]
            self.__listeners[sensor] = [False, None, None]
        # Define a 'major change' for each sensor measurements
        #TODO: change threshold for each sensor
        self.__thresholds = dict()
        for sensor in KiwriousSensor:
            # Each listener stores [is_activated_boolean, previous_row_of_data, current_row_of_data]
            self.__thresholds[sensor] = [0, 0]
        self.__thresholds[KiwriousSensor.HEARTBEAT] = [0]
    
    def __validate(self, sensor):
        ''' Return the next row of validated raw data in the sensor,
        skip and continues if it read incorrect format. '''

        byteRow = ''
        buffer = []
        count = 0
        while True:
            data = sensor.read()
            if data == b'':
                # hardware is disconnected
                break
            if count == 0:
                if data == bytes.fromhex('0a'):
                    count += 1
                    buffer.append(data)
                else:
                    pass
            elif count == 1:
                if data == bytes.fromhex('0a'):
                    count += 1
                    buffer.append(data)
                else:
                    count = 0
                    buffer = []
            elif count == 2:
                if data in [b'\x05', b'\x04', b'\x06', b'\x07', b'\t', b'\x0b']:
                    count += 1
                    buffer.append(data)
                else:
                    count = 0
                    buffer = []
            elif 2 < count < 24:
                count += 1
                buffer.append(data)
            elif count >= 24:
                if data == bytes.fromhex('0b'):
                    count += 1
                    buffer.append(data)
                    if count == 26:
                        byteRow = buffer
                        count = 0
                        buffer = []
                        break
                elif data == bytes.fromhex('0a'):
                    count = 1
                    buffer = [bytes.fromhex('0a')]
                else:
                    # this byte might be the body, go back to check we didn't miss a header
                    if bytes.fromhex('0a') in buffer[2:]:
                        buffer = buffer[2:]
                        index = buffer.index(bytes.fromhex('0a'))
                        if bytes.fromhex('0a') == buffer[index+1] and buffer[index+2] in [b'\x05', b'\x04', b'\x06', b'\x07', b'\t', b'\x0b']:
                            count = len(buffer) - index
                            buffer = buffer[index:]
                        else:
                            count = 0
                            buffer = []
                    else:
                        count = 0
                        buffer = []
        return byteRow

    def get_type(self, data):
        ''' Return sensor type of a row of data '''
        for sensor_type in KiwriousSensor:
            if data[2].hex() == sensor_type.value:
                return sensor_type
        return False
    
    def decode(self, data, kiwrioussensor):
        ''' Return decoded data according to given sensor type '''
        data = [x.hex() for x in data]
        if kiwrioussensor == KiwriousSensor.CONDUCTIVITY:
            return self.__getConductivity(data)
        elif kiwrioussensor == KiwriousSensor.AIR:
            return self.__getAirQuality(data)
        elif kiwrioussensor == KiwriousSensor.HUMIDITY:
            return self.__getHumidity(data)
        elif kiwrioussensor == KiwriousSensor.TEMPERATURE:
            return self.__getTemperature(data)
        elif kiwrioussensor == KiwriousSensor.LIGHT:
            return self.__getLightValue(data)
        elif kiwrioussensor == KiwriousSensor.HEARTBEAT:
            return self.__getHeartBeat(data)
        else:
            raise NotKiwriousException(kiwrioussensor, "is not a Kiwrious sensor")
    
    def get_unit(self, kiwrioussensor):
        ''' Return measurement units according to given sensor type '''
        if kiwrioussensor == KiwriousSensor.CONDUCTIVITY:
            return (SensorUnits.RESISTANCE,SensorUnits.CONDUCTIVITY)
        elif kiwrioussensor == KiwriousSensor.AIR:
            return (SensorUnits.VOC,SensorUnits.CO2)
        elif kiwrioussensor == KiwriousSensor.HUMIDITY:
            return (SensorUnits.HUMIDITY,SensorUnits.TEMPERATURE)
        elif kiwrioussensor == KiwriousSensor.TEMPERATURE:
            return (SensorUnits.IR_Temperature,SensorUnits.Ambient_temperature)
        elif kiwrioussensor == KiwriousSensor.LIGHT:
            return (SensorUnits.LUX,SensorUnits.UV_INDEX)
        elif kiwrioussensor == KiwriousSensor.HEARTBEAT:
            #No formula for heartbeat sensor given, so using conductivity's unit for now
            return SensorUnits.BPM
        else:
            raise NotKiwriousException(kiwrioussensor, "is not a Kiwrious sensor")
        
    def __getLightValue(self, data):
        ''' Return decoded light sensor data '''
        LUX = struct.unpack("<f",bytes.fromhex(''.join(data[6:10])))[0]
        UV = struct.unpack("<f",bytes.fromhex(''.join(data[10:14])))[0]
        return (LUX, UV)

    def __getConductivity(self, data):
        ''' Return decoded conductivity sensor data '''
        Resistance = struct.unpack("<h",bytes.fromhex(''.join(data[8:10])))[0]*struct.unpack("<h",bytes.fromhex(''.join(data[6:8])))[0]
        if Resistance == 0:
            return (0,0)
        Conductance = (1/Resistance)*1000000
        return (Resistance,Conductance)
    
    def __getAirQuality(self,  data):
        ''' Return decoded air sensor data '''
        VOC = struct.unpack("<h",bytes.fromhex(''.join(data[6:8])))[0]
        CO2 = struct.unpack("<h",bytes.fromhex(''.join(data[8:10])))[0]
        return (VOC,CO2)
    
    def __getHumidity(self, data):
        ''' Return decoded humidity sensor data '''
        Temperature = struct.unpack("<h",bytes.fromhex(''.join(data[6:8])))[0]/100
        Humidity = struct.unpack("<h",bytes.fromhex(''.join(data[8:10])))[0]/100
        return (Temperature,Humidity)
    
    def __getTemperature(self, data):
        ''' Return decoded temperature sensor data '''
        X = int((''.join(reversed(data[8:10]))), base=16)
        
        binarya = bytes.fromhex(''.join(data[10:14]))
        FLOAT = 'f'
        fmt = '<' + FLOAT * (len(binarya) // struct.calcsize(FLOAT))
        a = struct.unpack(fmt, binarya)[0]
        
        binaryb = bytes.fromhex(''.join(data[14:18]))
        FLOAT = 'f'
        fmt = '<' + FLOAT * (len(binaryb) // struct.calcsize(FLOAT))
        b = struct.unpack(fmt, binaryb)[0]
        
        binaryc = bytes.fromhex(''.join(data[18:22]))
        FLOAT = 'f'
        fmt = '<' + FLOAT * (len(binaryc) // struct.calcsize(FLOAT))
        c = struct.unpack(fmt, binaryc)[0]
        
        IRTemp = (a * pow(X, 2)) / pow(10, 5) + (b * X) + c
        IRTemp = float("{:.2f}".format(IRTemp))
        AmbientTemp = int(''.join(reversed(data[6:8])), base=16) / 100
        return (IRTemp, AmbientTemp)
    
    def __getHeartBeat(self, data):
        ''' Return decoded heartrate sensor data '''
        binary1i = bytes.fromhex(''.join(data[6:10]))
        UNSIGNED_INT = 'I'
        fmt = '<' + UNSIGNED_INT * (len(binary1i) // struct.calcsize(UNSIGNED_INT))
        ch_1i = struct.unpack(fmt, binary1i)[0]
        
        binary2i = bytes.fromhex(''.join(data[10:14]))
        UNSIGNED_INT = 'I'
        fmt = '<' + UNSIGNED_INT * (len(binary2i) // struct.calcsize(UNSIGNED_INT))
        ch_2i = struct.unpack(fmt, binary1i)[0]
        
        binary1ip1 = bytes.fromhex(''.join(data[14:18]))
        UNSIGNED_INT = 'I'
        fmt = '<' + UNSIGNED_INT * (len(binary1ip1) // struct.calcsize(UNSIGNED_INT))
        ch_1ip1 = struct.unpack(fmt, binary1ip1)[0]

        binary2ip1 = bytes.fromhex(''.join(data[18:22]))
        UNSIGNED_INT = 'I'
        fmt = '<' + UNSIGNED_INT * (len(binary2ip1) // struct.calcsize(UNSIGNED_INT))
        ch_2ip1 = struct.unpack(fmt, binary2ip1)[0]

        return [ch_1i,ch_2i,ch_1ip1,ch_2ip1]

    def on_sensor_data_increase(self, kiwrioussensor):
        ''' This method is deactivated by default,
        use deactivate_listener(sensorname) to block this method
        and activate_listener(sensorname) to unblock '''
        pass

    def set_threshold(self, kiwrioussensor, threshold1 = None, threshold2 = None):
        ''' set the threshold to define an increase in a sensor,
        change only one or both of the thresholds '''
        if kiwrioussensor not in self.__listeners:
            raise NotKiwriousException(kiwrioussensor, "is not a Kiwrious sensor")
        # set first threshold
        if threshold1 != None:
            if not isinstance(threshold1, float) and not isinstance(threshold1, int):
                raise NotKiwriousException("Value of threshold must be an integer or float")
            else:
                if kiwrioussensor == KiwriousSensor.HEARTBEAT:
                    self.__thresholds[kiwrioussensor] = [threshold1]
                else:
                    self.__thresholds[kiwrioussensor] = [threshold1, self.__thresholds[kiwrioussensor][1]]
        # set second threshold
        if threshold2 != None:
            if not isinstance(threshold2, float) and not isinstance(threshold2, int):
                raise NotKiwriousException("Value of threshold must be an integer or float")
            else:
                if kiwrioussensor == KiwriousSensor.HEARTBEAT:
                    raise NotKiwriousException("HEARTBEAT listener only has one threshold")
                self.__thresholds[kiwrioussensor] = [self.__thresholds[kiwrioussensor][0], threshold2]
    
    def __check_data_difference(self, kiwrioussensor):
        ''' Detect if difference between previous and current row exceeded the threshold '''
        if kiwrioussensor == KiwriousSensor.HEARTBEAT:
            if isinstance(self.__listeners[kiwrioussensor][1], int) and isinstance(self.__listeners[kiwrioussensor][2], int):
                if (self.__listeners[kiwrioussensor][1] - self.__listeners[kiwrioussensor][2] >= self.__thresholds[kiwrioussensor][0]):
                    self.on_sensor_data_increase(kiwrioussensor)
        else:
            if (self.__listeners[kiwrioussensor][1][0] - self.__listeners[kiwrioussensor][2][0] >= self.__thresholds[kiwrioussensor][0]):
                self.on_sensor_data_increase(kiwrioussensor)
            elif (self.__listeners[kiwrioussensor][1][1] - self.__listeners[kiwrioussensor][2][1] >= self.__thresholds[kiwrioussensor][1]):
                self.on_sensor_data_increase(kiwrioussensor)
    
    def disconnect_sensor(self, kiwrioussensor):
        ''' Stop reading from a sensor but the comport is open untill user detach the hardware '''
        if (kiwrioussensor in self.__connected_sensors_list):
            print(kiwrioussensor + " sensor disconnected")
            self.__connected_sensors_list.remove(kiwrioussensor)
    
    def connect_sensor(self, kiwrioussensor):
        ''' Attempt to start reading from a sensor that was disconnected before '''
        self.__connecting = True
        if (kiwrioussensor not in self.__connected_sensors_list):
            print("Attempt to connect", kiwrioussensor, "sensor to", self.__connected_sensors_list)
            self.__connected_sensors_list.append(kiwrioussensor)
        self.__connecting = False

    def activate_listener(self, kiwrioussensor):
        ''' Turn on listener, detect any major increase in sensor value.
        A major increase is defined by the thresholds list (zero by default),
        use set_threshold(sensorname, threshold1, threshold2) to define major increase  '''
        if (kiwrioussensor in self.__listeners):
            self.__listeners[kiwrioussensor] = [True, None, None]
    
    def deactivate_listener(self, kiwrioussensor):
        ''' Turn off listener '''
        if (kiwrioussensor in self.__listeners):
            self.__listeners[kiwrioussensor] = [False, None, None]

    def producer(self, current_port):
        self.__producer(current_port)
        
    def __producer(self, current_port):
        ''' An input stream from a sensor, continues until sensor disconnects '''
        try:
            sensor = serial.Serial(port=current_port.device, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
            self.__connected_ports.append(current_port.location)
        except Exception as e:
            print(e)
            print("connect fail")
            try:
                sensor.close()
            except Exception as e:
                exit(0)
            exit(0)
        try:
            
            byte_data = self.__validate(sensor)

            sensor_type = self.get_type(byte_data)

            index = self.__data_collector_index.index(sensor_type)

            if sensor_type == KiwriousSensor.HEARTBEAT:
                processor = HeartRate.HeartRateProcessor()

            if sensor_type == KiwriousSensor.HEARTBEAT:
                output = processor.processMultiInput(self.decode(byte_data,sensor_type))
                if len(output)>1:
                    decoded_data = int(output[1])
                else:
                    decoded_data = output[0]
            else:
                decoded_data = self.decode(byte_data,sensor_type)
            
            self.__data_collector_raw[index] = byte_data
            self.__data_collector[index] = decoded_data
            if self.__record:
                self.__data_repo[index].append(decoded_data)
            
            self.__connected_sensors_list.append(sensor_type)
            print(str(sensor_type) + " sensor connected")
            self.on_sensor_connection(self.get_connected_sensors()[-1], self.__alive) #call user defined method when there is a successful connection
            
            while self.__alive:
                # whil service is alive
                if sensor_type in self.__connected_sensors_list:
                    byte_data = self.__validate(sensor)
                    
                    if sensor_type == KiwriousSensor.HEARTBEAT:
                        output = processor.processMultiInput(self.decode(byte_data,sensor_type))
                        if len(output)>1:
                            decoded_data = int(output[1])
                        else:
                            decoded_data = output[0]
                    else:
                        decoded_data = self.decode(byte_data,sensor_type)
                    
                    self.__data_collector_raw[index] = byte_data
                    self.__data_collector[index] = decoded_data
                    if self.__record:
                        self.__data_repo[index].append(decoded_data)
                    
                    self.on_sensor_data(sensor_type, decoded_data) #call user defined method when there is a pack of new data received
                    
                    current = decoded_data
                    if (self.__listeners[sensor_type][0] == True): # update previous_row and current_row for listener
                        self.__listeners[sensor_type] = [True, self.__listeners[sensor_type][2], current]
                        if (self.__listeners[sensor_type][1] != None and self.__listeners[sensor_type][2] != None):
                            self.__check_data_difference(sensor_type)
            
            self.__connected_ports.remove(current_port.location)
            if (sensor_type in self.__connected_sensors_list):
                self.__connected_sensors_list.remove(sensor_type)
                self.__data_collector[index] = None
                self.__data_collector_raw[index] = None
            sensor.close()
            print(str(sensor_type) + " sensor detached from device")
        except Exception as e:
            #print(e)
            try:
                # kill process for this sensor if hardware detached
                self.__connected_ports.remove(current_port.location)
                self.__connected_sensors_list.remove(sensor_type)
                self.__data_collector[index] = None
                self.__data_collector_raw[index] = None
                sensor.close()
                print(str(sensor_type) + " sensor detached from device")
                self.on_sensor_connection(sensor_type, self.__alive) #call user defined method when there is a connection ended
                print("current connected sensor => " + str(self.__connected_sensors_list))
            except:
                self.__alive = False
                os._exit(1)

    def verify_and_create_Sensors(self):
        self.__verify_and_create_Sensors()

    def __verify_and_create_Sensors(self):
        while self.__alive:
            sleep_time = 0
            self.__connecting = True
            for port in serial.tools.list_ports.comports():
                if port.vid != None and port.pid != None:
                    if port.vid == int(0x04d8) and port.pid == int(0xec19) and port.location not in self.__connected_ports: #check it is a kiwrious sensor and not a sensor already connected
                        p1 = threading.Thread(target=self.producer, args=(port,),daemon=True)
                        #p1.daemon = True
                        p1.start()
                        sleep_time += 0.5
            time.sleep(sleep_time)
            self.__connecting = False
            time.sleep(0.1)
                        
 
    def start_service(self):
        ''' Start building connection with the sensor '''
        self.__alive = True
        verify_and_create_Sensors = threading.Thread(target=self.verify_and_create_Sensors, daemon=True)
        #user_consumer = threading.Thread(target=self.user_consumer)
        verify_and_create_Sensors.start()
        #user_consumer.start()
        return

    def stop_service(self):
        ''' End connection with the sensor '''
        self.__alive = False
        time.sleep(1)
        self.__connected_sensors_list = []
        self.__data_collector_raw = [None,None,None,None,None,None,None]
        self.__data_collector = [None,None,None,None,None,None,None]
        self.__connecting = False
        self.__record = False
        self.__connected_ports = []
        return
    
    def start_record(self):
        self.__record = True
        return
    
    def stop_record(self):
        self.__record = False
        return
    
    def set_timeout(self, time):
        self.__timeout = time
        return
    
    def get_recorded_data(self, kiwrioussensor):
        index = self.__data_collector_index.index(kiwrioussensor)
        return self.__data_repo[index]

    def get_connected_sensors(self):
        ''' Return a list of all connected sensors '''
        if not self.__alive:
            return []
        
        TTL = self.__timeout
        while self.__connecting == True:     #openning new port
            time.sleep(0.1)
            TTL -= 1
            if TTL == 0:
                break
        return self.__connected_sensors_list

    def get_raw_data(self, kiwrioussensor):
        ''' Return the most recent row of raw data for a given sensor
        >>> get_raw_data('HUMIDITY')
        ['0a', '0a', '07', '01', '02', '00', '6b', '09', '7f', '18', 'b4', '44', '44', '7d', '48', '70', 'ed', '79', '39', '64', 'a9', '44', '79', '16', '0b', '0b']
        '''
        if not self.__alive:
            return None
        
        TTL = self.__timeout
        while kiwrioussensor not in self.__connected_sensors_list:     #read sensor haven't started
            time.sleep(0.1)
            TTL -= 1
            if TTL == 0:
                print(str(kiwrioussensor) + " is not connected")
                return None
                #raise NotKiwriousException(kiwrioussensor, "is not connected")
        
        
        index = self.__data_collector_index.index(kiwrioussensor)
        while self.__data_collector_raw[index] == -1:
            time.sleep(0.1)
        data = self.__data_collector_raw[index]
        if data:
            self.__data_collector_raw[index] = -1
            self.__data_collector[index] = -1
            return data
        
        print(str(kiwrioussensor) + " is not connected")
        return None
        #raise NotKiwriousException(kiwrioussensor, "is not connected")
    
    
    def get_decoded_data(self, kiwrioussensor):
        ''' Return the most recent row of decoded data for a given sensor
        >>> get_decoded_data('AIR')
        (0, 415)
        '''
        if not self.__alive:
            return None
        
        TTL = self.__timeout
        while kiwrioussensor not in self.__connected_sensors_list:     #read sensor haven't started
            time.sleep(0.1)
            TTL -= 1
            if TTL == 0:
                print(str(kiwrioussensor) + " is not connected")
                return None
                #raise NotKiwriousException(kiwrioussensor, "is not connected")
        
        
        index = self.__data_collector_index.index(kiwrioussensor)
        while self.__data_collector[index] == -1:
            time.sleep(0.1)
        decoded_data = self.__data_collector[index]
        
        if decoded_data:
            self.__data_collector_raw[index] = -1
            self.__data_collector[index] = -1
            return decoded_data
        
        print(str(kiwrioussensor) + " is not connected")
        return None
        #raise NotKiwriousException(kiwrioussensor, "is not connected")

    def get_sensor_reading(self, kiwrioussensor):
        ''' Return the most recent row of formatted data for a given sensor
        >>> get_sensor_reading('LIGHT')
        [SensorData{sensor_type = KiwriousSensor.LIGHT, data_value = 93.95458984375; data_unit = SensorUnits.LUX}, SensorData{sensor_type = KiwriousSensor.LIGHT, data_value = 0.435791015625; data_unit = SensorUnits.UV_INDEX}]
        '''
        if not self.__alive:
            return None
        
        TTL = self.__timeout
        while kiwrioussensor not in self.__connected_sensors_list:     #read sensor haven't started
            time.sleep(0.1)
            TTL -= 1
            if TTL == 0:
                print(str(kiwrioussensor) + " is not connected")
                return None
                #raise NotKiwriousException(kiwrioussensor, "is not connected")
        
        Units = self.get_unit(kiwrioussensor)
        index = self.__data_collector_index.index(kiwrioussensor)
        
        while self.__data_collector[index] == -1:
            time.sleep(0.1)
        decoded_data = self.__data_collector[index]
        
        if decoded_data:
            self.__data_collector_raw[index] = -1
            self.__data_collector[index] = -1
            if kiwrioussensor == KiwriousSensor.HEARTBEAT:
                return SensorData(kiwrioussensor,decoded_data,Units)
            else:
                frame = [SensorData(kiwrioussensor,decoded_data[0],Units[0]),SensorData(kiwrioussensor,decoded_data[1],Units[1])]
                return [frame[0],frame[1]]
        print(str(kiwrioussensor) + " is not connected")
        return None
        #raise NotKiwriousException(kiwrioussensor, "is not connected")

    def on_sensor_data(self, kiwrioussensor, decoded_data):
        ''' Custom action on a piece of data on read in '''
        pass

    def on_sensor_connection(self, kiwrioussensor, is_connected):
        ''' Custom action on a sensor connection '''
        pass


# run the UserImplementation.py class
