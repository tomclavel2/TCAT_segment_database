class Stop:
    def __init__(self,stopId, messageId,stopTime,onboard,boards,alights):
        self.stopId=stopId
        self.stopTime=stopTime
        self.messageId=messageId
        self.onboard=onboard
        self.boards=boards
        self.alights=alights

class Segment:
    def __init__(self,iStopNumber,tStopNumber,numberBoardsIStop,numberAlightsTStop,timeIStop,timeTStop,bus):
        self.segmentID=(iStopNumber,tStopNumber)
        self.iStopNumber=iStopNumber
        self.tStopNumber=tStopNumber
        self.numberBoardsInitialStop=numberBoardsIStop
        self.numberAlightsTerminalStop= numberAlightsTStop
        self.timeInitialStop=timeIStop
        self.timeTerminalStop=timeTStop
        self.miles=0
        self.bus=bus

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
      self.buses=[bus]
      self.buses.append(bus)
     # self.stops=[self.lastStop]
      self.scheduledStopsMade=[]
      self.scheduledStopsMissed=[]
      self.unscheduledStopsMade=[]

    def addScheduledStopMade(self,stop):
        if stop not in self.scheduledStopsMade:
            self.scheduledStopsMade.append(stop)

    def addUnscheduledStopMade(self,stop):
        if stop not in self.unscheduledStopsMade and stop not in self.scheduledStopsMade:
            self.unscheduledStopsMade.append(stop)

#Use this to add a segment for the actual bus trips
    def addSegment(self, stop,bus):
        lastStop=self.lastStop
        newSegment=Segment(lastStop.stopId,stop.stopId,lastStop.boards,stop.alights,lastStop.stopTime,stop.stopTime,bus)
        self.segments.append(newSegment)
        self.lastStop=stop
        self.numberOfStops+=1
        self.tripEndTime=stop.stopTime

#use this for adding segment to historical day
    def addSeg(self, segment):
        self.segments.append(segment)
        self.tripEndTime=segment.timeTerminalStop
        self.lastStopTime=segment.timeTermialStop


    def addBus(self, bus):
        self.buses.append(bus)
        self.currentBus=bus


#need to check if this works right in all cases
    def findStop(self,stop):
        for s in self.segments:
            if stop == s.iStopNumber:
                return self.segments.index(s)
            elif  stop == s.tStopNumber:
                return self.segments.index(s)
            else:
                return 0


class Block:
    def __init__(self, blockNumber):
      self.blockNumber=blockNumber
      self.trips=[]
      self.numberOfTrips=0
      self.numberOfBuses=0
      self.missedTrips=[]

    def addTrip(self, trip):
        self.trips.append(trip)
        self.numberOfTrips+=1
        self.numberOfBuses+=1

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
      self.missedBlocks=[]


    def addBlock(self, block):
        self.blocks.append(block)
        self.numberOfBlocks+=1

    def getBlock(self, blockNumber):
        for b in self.blocks:
            if blockNumber==b.blockNumber:
                return b

    def getBlockNumbers(self):
        list=[]
        for block in self.blocks:
            list.append(block.blockNumber)
        return list

    def addBus(self,bus):
        if bus not in self.busesUsed:
            self.busesUsed.append(bus)
