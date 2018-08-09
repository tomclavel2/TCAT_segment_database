#A stop object is meant to encapsulate all the information that is recoreded at the stop level
#To create a stop object use the statement 
#           newStop = Stop(stopId, stopName, messageId, stopTime, onboard, boards, alights, seen)
#which creates a new stop object and uses the variable newStop as a reference for the object
#This inculdes in order: The stop number, the stop name, the message ID type, the vmh time, the number of onboard passangers is there
#(but this should not be used since it is unreliable), the number of boards and alights, and how many times the stop has been seen
class Stop:
    def __init__(self, stopID, stopName, messageTypeID, stopTime, onboard, boards, alights, seen):
        self.stopID=stopID
        self.stopName=stopName
        self.messageTypeID=messageTypeID 
        self.stopTime=stopTime  
        self.onboard=0
        self.boards=boards
        self.alights=alights
        self.stopName=stopName
        self.seen=seen

#A Segment object is the main piece of information we need to construct the segments table.
#To create a segment object use the statement
#      newSegment= Segment(iStop, tStop, bus,distance,segmentsequence)
# This includes in order: The intial stop object, the terminal stop object, the bus number, the distance of the segment, and the sequence number of the segment
#In addition to these fields each segment object has a onboard field that tracks how many passengers rode the bus between those two stops
class Segment:
    def __init__(self, iStop, tStop, bus,distance,segseq):
        self.segmentID=(iStop, tStop)
        self.onboard=0
        self.distance=distance
        self.bus=bus
        self.segmentSeq=segseq
        self.adjustedOnboard=0
    
    #This function is void and is meant to act on a segment object using the following syntax: 
    #              segment.updateSegment(150,2)
    #The intended use of this function is to update the segment in an actual day object to include the information of segment distance
    # and sequence number which can only be taken from a segment from the scheduled day object. 
    #This function requires two integer arguements, the distance and the sequence number which must be provided in that order 
    def updateSegment(self,distance,segSeq):
        self.distance=distance
        self.segmentSeq=segSeq

#A trip object contains all the information that is at the trip level
#To create a trip object use the statement 
#           newTrip= Trip(tripNumber, bus, stopID, stopName, stopTime, messageTypeID, onboard, boards, alights, route, direction, pattern)
#Each time a trip is created it also creates a stop object
#Each trip also contains the following fields:
#currentBus-the most recent bus associated with the trip, lastStop-the most recent stop object associated with the trip, numberOfStop,
#tripStartTime,tripEndTime, route, diection, pattern, segments- a list of segments of the trip, buses- a list of busses used,
#and stops- a list of stop objects made on the trip
class Trip:
    def __init__(self, tripNumber, bus, stopID, stopName, stopTime, messageTypeID, onboard, boards, alights, route, direction, pattern):
      self.tripNumber=tripNumber
      self.currentBus = bus
      self.lastStop = Stop(stopID,  stopName, messageTypeID, stopTime, onboard, boards, alights, 1)
      self.numberOfStops = 1
      self.tripStartTime = stopTime
      self.tripEndTime = stopTime
      self.route=route
      self.direction=direction
      self.pattern=pattern
      self.segments=[]
      self.buses=[bus]
      self.stops=[self.lastStop]
      self.adjustment=0
      self.boards=0
      self.alights=0
      self.adjboards=0
      self.adjalights=0

     
    #This function is void and is meant to act on a trip object using the following syntax: 
    #              trip.addSegment(Stop,12)
    #The intended add a segment to a trip in the actual day object,  using a stop object and a bus number passed in as parameters
    #Since the distance and segment sequence are not available in the actual trip history the segment initializes the distance to 0
    # and the sequence number to -1
    def addSegment(self, stop, bus):
        lastStop=self.lastStop
        newSegment=Segment(lastStop,stop,bus,0,-1)
        #newSegment.onboard=lastStop.onboard 
        self.segments.append(newSegment)
        self.stops.append(stop)
        self.lastStop=stop
        self.numberOfStops+=1
        self.tripEndTime=stop.stopTime

    #This function is void and is meant to act on a trip object using the following syntax: 
    #              trip.updateTrip(150,2)
    #The intended use of this function is to update the trip in an actual day object to include the information of route
    #and pattern which can only be taken from a from the scheduled day object. 
    #This function requires two integer arguements, the route and number which must be provided in that order     
    def updateTrip(self, route, pattern):
        self.route = route
        self.parrtern = pattern



    def findFirstStop(self,stop,index):
        x=0
        s=index
        while s < len(self.segments):
            if  stop == self.segments[s].segmentID[0].stopID:
                x=1
                return s
            else:
                s=s+1
        #print(x)
        if x == 0:
          return -1

    #need to check if this works right in all cases
    def findSecondStop(self,stop,index):
        x=0
        s=index
        while s < len(self.segments):
            if  stop == self.segments[s].segmentID[1].stopID:
                x=1
                return s
            else:
                 s=s+1
        if x == 0:
          return -1



    def findMatch(self, idOne, idTwo,index):
        x=0
        s=index
        while s < len(self.segments):
            if self.segments[s].segmentID[0].stopID==idOne and self.segments[s].segmentID[1].stopID==idTwo:
                x=1
                return s
            else:
              s=s+1
        if x==0:
            return -1

    def getStops(self):
        x=[]
        if self.stops==None:
            print('oh man')
            return x
        else:
            for s in self.stops:
                    x.append(s.stopID)
            return x


class dTrip:
    def __init__(self, block, trip):
        self.blockNumber=block
        self.trip=trip


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
        print("Could not find trip")

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
      self.deviations=None


    def addBlock(self, block):
        self.blocks.append(block)
        self.numberOfBlocks+=1

    def getBlock(self, blockNumber):
        for b in self.blocks:
            if blockNumber==b.blockNumber:
                return b
        print("Could not find Block")

    def getBlockNumbers(self):
        list=[]
        for block in self.blocks:
            list.append(block.blockNumber)
        return list

    def addBus(self,bus):
        if bus not in self.busesUsed:
            self.busesUsed.append(bus)

class Deviations:
    def __init__(self):
        self.blocksMissed=[]
        self.tripsMissed=[]
        self.stopsMissed=[]
        self.nonscheduledStopsMade=[]
        self.scheduledStopsMissed=[]
