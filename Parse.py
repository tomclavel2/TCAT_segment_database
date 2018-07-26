from Classes import Day, Block, Trip, Segment, Stop
# TODO need to add functionality to parseActual that inferes stops from message id's and changes in onboard counts
def parseActual(currentDay,results):
    cMessageTypeId=results[0]
    cBlockNumber=results[2]
    cRoute=results[3]
    cTripNumber=results[4]
    cDir=results[5]
    cVMHTime=results[6]
    cBus=results[7]
    cOnboard=results[8]
    cBoards=results[9]
    cAlights=results[10]
    cStopId=results[11]
    cStopName=results[12]
    if cBlockNumber not in currentDay.getBlockNumbers():
        newBlock=Block(cBlockNumber)
        newTrip = Trip (cTripNumber, cBus, cStopId, cVMHTime, cMessageTypeId, cOnboard, cBoards, cAlights,cRoute, cDir,cStopName) #tripNumber, bus, stop, stopTime, messageId, onboard, boards, alights,route,direction,stopName
        newBlock.addTrip(newTrip)
        currentDay.addBlock(newBlock)
        currentDay.addBus(cBus)
        return currentDay
    else:
        currentBlock=currentDay.getBlock(cBlockNumber)
        if cTripNumber not in currentBlock.getTripNumbers():
            newTrip =Trip (cTripNumber, cBus, cStopId, cVMHTime, cMessageTypeId, cOnboard, cBoards, cAlights,cRoute, cDir,cStopName)
            currentBlock.addTrip(newTrip)
            currentDay.addBus(cBus)
            return currentDay
        else:
            currentTrip = currentBlock.getTrip(cTripNumber)
            if cBus != currentTrip.currentBus:
                currentTrip.addBus(cBus)
                currentDay.busesUsed.append(cBus)
                if cStopId == currentTrip.lastStop.stopId:   #If i see the same stop id two times in a row should i disregard the second one
                    return currentDay
                else:
                    currentStop=Stop(cStopId,cMessageTypeId,cVMHTime,cOnboard,cBoards,cAlights,cStopName,0)#Stop(self, stopId, messageId, stopTime, onboard, boards, alights, stopName,stopseq
                    currentTrip.addSegment(currentStop,cBus)
                    return currentDay
            else:
                if cStopId == currentTrip.lastStop.stopId:
                    return currentDay
                else:
                    currentStop=Stop(cStopId,cMessageTypeId,cVMHTime,cOnboard,cBoards,cAlights,cStopName,0)#Stop(stop, messageId, stopTime, onboard, boards, alights)
                    currentTrip.addSegment(currentStop,cBus)
                    return currentDay


def display(currentDay):
    print(currentDay.date)
    for b in currentDay.blocks:
        print('block ' + str(b.blockNumber))
        for t in b.trips:
            print('trip ' + str(t.tripNumber))
            for s in t.segments:
                print(str(s.segmentID[0])+str(s.segmentID[1]),  end=' ; ')


def parseHistorical(currentDay,results):
    hRoute=results[2]
    hTrip=results[3]
    hDirection=results[4]
    hBlock=results[5]
    hTripStart=results[6]
    hTripEnd=results[7]
    hIStopID=results[8]
    hTStopID=results[9]
    hSegmentMiles=results[10]

    if hBlock not in currentDay.getBlockNumbers():
        newSegment=Segment(hIStopID, hTStopID, None,None, hTripStart,hTripEnd)
        newSegment.miles=hSegmentMiles
        newTrip=Trip( hTrip, None, None, hTripEnd, None, None, None, None)
        newTrip.addSeg(newSegment)
        newBlock=Block(hBlock)
        newBlock.addTrip(newTrip)
        currentDay.addBlock(newBlock)
        return currentDay
    else:
        currentBlock=currentDay.getBlock(hBlock)
        if hTrip not in currentBlock.trips:
            newSegment=Segment(hIStopID, hTStopID, None,None, hTripStart,hTripEnd)
            newSegment.miles=hSegmentMiles
            newTrip=Trip( hTrip, None, None, hTripEnd, None, None, None, None)
            newTrip.addSeg(newSegment)
            currentBlock.addTrip(newTrip)
            return currentDay
        else:
            currentTrip=currentBlock.getTrip(hTrip)
            newSegment=Segment(hIStopID, hTStopID, None,None, hTripStart,hTripEnd)
            newSegment.miles=hSegmentMiles
            currentTrip.addSeg(newSegment)
            return currentDay

def compareDay(actualDay, historicalDay):
    for hBlock in historicalDay.blocks:
        if hBlock.blockNumber not in actualDay.getBlockNumbers():
           actualDay.missedBlocks.append(hBlock.blockNumber)
        else:
            compareBlocks(actualDay.getBlock(hBlock.blockNumber), hBlock)

def compareBlocks(actualBlock, historicalBlock):
    for hTrip in historicalBlock.trips:
        if hTrip.tripNumber not in actualBlock.getTripNumbers():
            actualBlock.missedTrips.append(hTrip.tripNumber)
        else:
            compareTrips(actualBlock.getTrip(hBlock.tripNumber), hTrip)

def compareTrips(aTrip, hTrip):

    aIndex=0
    hIndex=0
    while aIndex <= aTrip.segments.size() and hIndex <= hTrip.segments.size():

        aSegment = aTrip.segments[aIndex]
        hSegment = hTrip.segments[aIndex]

        if aSegment.segmentID[0] == hSegment.segmentID[0] and aSegment.segmentID[1] == hSegment.segmentID[1]:
           aSegment.miles = hSegment.segment_miles
           actualTrip.addScheduledStopMade(aSegment.segmentID[0])
           actualTrip.addScheduledStopMade(aSegment.segmentID[1])

        elif aSegment.segmentID[0] == hSegment.segmentID[0] :

            aTrip.addScheduledStopMade(aSegment.segmentID[0])
            y0 = hTrip.findStop(aSegment.segmentID[1])
            hPart=hTrip.segments[hIndex:y0]     #need to add information from trip into the trips im adding
            aPart=aTrip.segments[0:aIndex-1]
            aPart.extend(hPart)
            size=aPart.size()
            aPart.extend(aTrip.segments[aIndex+1:])
            aTrip=aPart
            aIndex=size
            hIndex=y0+1
        elif aSegment.segmentID[1]==hSegment.segmentID[1]:
            #mark down the deviation, not sure how to handle this yet
            aIndex=aIndex#this is nonsense
        else:

            #mark down the devitiono
            x0=aTrip.findStop(hSegment.segmentID[0])
            x1=aTrip.findStop(hSegment.segmentID[1])
            y0=hTrip.findStop(aSegment.segmentID[0])
            y1=hTrip.findStop(aSegment.segmentID[1])
