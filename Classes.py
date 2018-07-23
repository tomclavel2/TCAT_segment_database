class Stop:
    def __init__(self,stopId, messageId,stopTime,onboard,boards,alights):
        self.stopId=stopId
        self.stopTime=stopTime
        self.messageId=messageId
        self.onboard=onboard
        self.boards=boards
        self.alights=alights

class Segment:
    def __init__(self,iStopNumber,tStopNumber,numberBoardsIStop,numberAlightsTStop,timeIStop,timeTStop):
        self.segmentID=(iStopNumber,tStopNumber)
        self.iStopNumber=iStopNumber
        self.tStopNumber=tStopNumber
        #self.segmentDistance=segmentDistance
        self.numberBoardsInitialStop=numberBoardsIStop
        self.numberAlightsTerminalStop= numberAlightsTStop
        self.timeInitialStop=timeIStop
        self.timeTerminalStop=timeTStop

class Trip:
    def __init__(self, tripNumber, bus, stop, stopTime, messageId, onboard, boards, alights):
      self.tripNumber=tripNumber
      self.currentBus = bus
      self.lastStop = Stop(stop, messageId, stopTime, onboard, boards, alights)
      self.lastStopTime = stopTime
      self.numberOfStops = 1
      self.tripStartTime = stopTime
      self.tripEndTime = stopTime
      self.segments=[]
      self.buses=[]
      self.buses.append(bus)

    def getTripNumber(self):
        self.tripNumber

    def addSegment(self, stop):
        lastStop=self.lastStop
        newSegment=Segment(lastStop.stopId,stop.stopId,lastStop.boards,stop.alights,lastStop.stopTime,stop.stopTime)
        self.segments.append(newSegment)
        self.lastStop=stop
        self.numberOfStops+=1
        self.tripEndTime=stop.stopTime

    def getSegments(self):
        return self.segments

    def addBus(self, bus):
        self.buses.append(bus)
        self.currentBus=bus


    def getBuses(self):
        return self.buses

class Block:
    def __init__(self, blockNumber):
      self.blockNumber=blockNumber
      self.trips=[]
      self.numberOfTrips=0
      self.numberOfBuses=0

    def addTrip(self, trip):
        self.trips.append(trip)
        self.numberOfTrips+=1
        self.numberOfBuses+=1

    def getTrips(self):
        return self.trips

    def getTrip(self, tripNumber):
        for t in self.trips:
            if t.tripNumber==tripNumber:
                return t

    def getTripNumbers(self):
        list=[]
        for t in self.trips:
            list.append(t.tripNumber)
        return list

class Day:
    def __init__(self, date):
      self.date=date
      self.numberOfBlocks=0
      self.busesUsed=[]
      self.blocks=[]

    def addBlock(self, block):
        self.blocks.append(block)
        self.numberOfBlocks+=1

    def getBlock(self, blockNumber):
        for b in self.blocks:
            if blockNumber==b.blockNumber:
                return b


    def getBlocks(self):
        return self.blocks

    def getBlockNumbers(self):
        list=[]
        for block in self.blocks:
            list.append(block.blockNumber)
        return list

    def addBus(self,bus):
        if bus not in self.busesUsed:
            self.busesUsed.append(bus)
