from Kiwrious import KiwriousService, KiwriousSensor, SensorData, SensorUnits
import time

class ExampleSubclass(KiwriousService):
    ''' A demo class that shows how methods can be over written, 
    all three methods are called in the producer process, 
    it will be executed on every row of data read. '''
    
    def on_sensor_data(self, user_sensor, user_data):
        print("on sensor data defined")

    def on_sensor_connection(self, user_sensor, user_connection):
        print(str(user_sensor) + " connection defined")

    def on_sensor_data_increase(self, kiwrioussensor):
        if (kiwrioussensor == KiwriousSensor.LIGHT):
            print("DANGER! Overexposure to UV light!")
        else:
            super().on_sensor_data_increase(kiwrioussensor)
            print("Major change in ", str(kiwrioussensor), " sensor!")

if __name__ == '__main__':

    service = KiwriousService()
    #service = ExampleSubclass()

    # plug in the heart rate sensor
    service.start_service()

    for i in range(10):
        print(service.get_sensor_reading(KiwriousSensor.HEARTBEAT))
        time.sleep(2) # sleep for slower print, can be removed
    
    service.stop_service()

    print("-----switch to subclass-----")
    service.start_service()
    
    print("activate heart listener")
    service.activate_listener(KiwriousSensor.HEARTBEAT)
    service.set_threshold(KiwriousSensor.HEARTBEAT, 1) # execute on_sensor_data_increase if heartbeat rise by 1
    time.sleep(15) # sleep to view print statements from on_sensor_data_increase

    service.stop_service()