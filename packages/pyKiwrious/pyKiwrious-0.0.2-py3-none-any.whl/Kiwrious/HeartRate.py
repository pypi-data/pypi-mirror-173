from array import array
from contextlib import nullcontext
from enum import Enum
import math
import re
import numpy as np
from numpy.fft import fft, ifft

# input lower than MIN_INPUT_VALUE are considered not heart rate signal (when hand is not on sensor)
MIN_INPUT_VALUE = 300000
# input higher than MAX_INPUT_VALUE are considered not heart rate signal (when sensor moved rapidly)
MAX_INPUT_VALUE = 900000
SAMPLE_RATE = 200

INPUT_ARRAY_SIZE = 2048
RESULT_ARRAY_SIZE = 100

NULL = 0

# initialise SOS to filter signals
SOS = [
    [ [1.0000, 0, -1.0000], [1.0000, -1.9794, 0.9847]],
    [ [1.0000, 0, -1.0000], [1.0000, -1.9948, 0.9953]],
    [ [1.0000, 0, -1.0000], [1.0000, -1.9537, 0.9583]],
    [ [1.0000, 0, -1.0000], [1.0000, -1.9849, 0.9855]],
    [ [1.0000, 0, -1.0000], [1.0000, -1.9730, 0.9737]],
    [ [1.0000, 0, -1.0000], [1.0000, -1.9392, 0.9426]],
    [ [1.0000, 0, -1.0000], [1.0000, -1.9571, 0.9583]],
    [ [1.0000, 0, -1.0000], [1.0000, -1.9410, 0.9432]]
]

GAIN =  [0.0256,     0.0256,     0.0254,     0.0254,     0.0252,     0.0252,     0.0251,     0.0251,     1.0000]


class HEART_RATE_RESULT_STATUS(Enum):
    ''' heart rate results, heart rate is calculated when status is 'READY' '''
    TOO_LOW = 'TOO_LOW'
    TOO_HIGH = 'TOO_HIGH'
    PROCESSING = 'PROCESSING'
    READY = 'READY'

class FixedArray:
    ''' array with bounded size '''
    def __init__(self, size):
        self._size = size
        self._array = []
        self._sum = 0

    def _log(self, msg):
        print('|FixedArray|' + msg)

    def isAverageReady(self):
        ''' check if there is enough data to find heart rate '''
        return len(self._array) >= self._size
    
    def average(self):
        return self.calcAverage(self._sum, len(self._array))

    def array(self):
        return self._array

    def _cleanup(self):
        while(len(self._array) > self._size):
            removed = self._array.pop(0)
            if removed:
                self._sum = self._sum - removed

    def _add(self, item):
        self._array.append(item)
        self._sum = self._sum + item

    def add(self, item):
        self._add(item)
        self._cleanup()

    def addItems(self, items):
        for item in items:
            self.add(item)

    def calcSum(self, arr):
        return sum(arr)

    def calcAverage(self, _sum,length):
        if length == 0:
            return 0
        return _sum/length

    def createSteppedArray(startValue, stopValue, cardinality):
        arr = []
        step = (stopValue - startValue) / (cardinality - 1)
        for i in range(cardinality):
            arr.append(startValue + step * i)
        return arr

class Biquad:
    ''' A representation of a biquadratic filter '''
    def __init__(self,b, a, g1, g2):
        self.b = b
        self.a = a
        self.g1 = g1
        self.g2 = g2
        self.w = [1, 1, 1]
    
    def _log(self, msg):
        print("Biquad"+msg)
    
    def updateFilter(self, x):
        xGained = x * self.g1
        self.w[2] = self.w[1]
        self.w[1] = self.w[0]
        self.w[0] = xGained - self.a[1] * self.w[1] - self.a[2] * self.w[2]

        y = self.b[0] * self.w[0] + self.b[1] * self.w[1] + self.b[2] * self.w[2]
        yGained = y * self.g2

        return yGained

class HeartRateProcessor:
    ''' Processor that stores some previous rows of data and generate heart rate '''
    def __init__(self):
        self._filters = []
        self._xf = NULL
        self._log('ctor')
        self._initFilters()
        halfSampleRate = math.floor(SAMPLE_RATE/2)
        self._resultArray = FixedArray(RESULT_ARRAY_SIZE)
        self._inputArray = FixedArray(INPUT_ARRAY_SIZE)

        L = INPUT_ARRAY_SIZE
        halfL = math.floor(L / 2)
        self._xf = FixedArray.createSteppedArray(0, halfSampleRate, halfL)
    
    def _log(self, msg):
        print('HeartRateProcessor'+msg)
    
    def _initFilters(self):
        filters = []
        for i in range(len(SOS)):
            filters.append(Biquad(SOS[i][0], SOS[i][1], GAIN[i], 1))
        self._filters = filters
    
    def getStatusForInput(self, input):
        if (input < MIN_INPUT_VALUE):
            return HEART_RATE_RESULT_STATUS.TOO_LOW
        elif (input > MAX_INPUT_VALUE):
            return HEART_RATE_RESULT_STATUS.TOO_HIGH
        return HEART_RATE_RESULT_STATUS.PROCESSING
    
    def processSingleInput(self, input):
        status = self.getStatusForInput(input)
        if (status != HEART_RATE_RESULT_STATUS.PROCESSING):
            return [status]
        self._inputArray.add(input)
        output = self.process()

        if not output:
            return [HEART_RATE_RESULT_STATUS.PROCESSING]
        
        return [HEART_RATE_RESULT_STATUS.READY, output]
    
    def processMultiInput(self, input_arr):
        for input_number in input_arr:
            status = self.getStatusForInput(input_number)
            if (status != HEART_RATE_RESULT_STATUS.PROCESSING):
                return [status]
            
        self._inputArray.addItems(input_arr)
        output = self.process()

        if not output:
            return [HEART_RATE_RESULT_STATUS.PROCESSING]
        
        return [HEART_RATE_RESULT_STATUS.READY, output]
    
    def process(self):
        if not self._inputArray.isAverageReady():
            return NULL
        
        heartRate = self._process(self._inputArray)
        if not heartRate:
            return NULL
        
        self._resultArray.add(heartRate)
        if not self._resultArray.isAverageReady():
            #self._log('waiting for enough results', len(self._resultArray.array));
            return NULL
        
        return self._resultArray.average()
    
    def _process(self, input_array: FixedArray):
        if not input_array.isAverageReady():
            return NULL
        
        filtered = []
        for input_number in input_array.array():
            adjustedV = input_number - input_array.average()
            filtered.append(self._updateAllFilters(adjustedV))

        dataFFT = fft(filtered)
        mag = np.abs(dataFFT)

        minVal = 0
        minIndex = 0

        for i in range(len(mag)//2):
            element = mag[i]
            if (element > minVal):
                minVal = element
                minIndex = i

        heartRate = self._xf[minIndex] * 60
        return heartRate

    def _updateAllFilters(self, input_number):
        current = input_number
        for filter in self._filters:
            output = filter.updateFilter(current)
            current = output
        return output
