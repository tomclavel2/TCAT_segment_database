from Classes import Day, Block, Trip, Segment, Stop
# TODO need to add functionality to parseActual that inferes stops from message id's and changes in onboard counts

 #This function is responsible for looking at every row in the actual stop history
 # table and creating objects for the blocks, trips, segments and stops

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
    if cBlockNumber not in currentDay.getBlockNumbers():                        #
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
                print('Segment : ' +  '(' + str(s.segmentID[0].stopId) +' , ' +str(s.segmentID[1].stopId) +')', end= '; ')
                print("seg length"+str(len(t.segments)))
                #for s in t.segments
#print(str(s.segmentID[0].stopId) +','+str(s.segmentID[1].stopId),  end=' ; ')


def parseHistorical(currentDay,results):
    hStopSeq=[2]
    hRoute=results[3]
    hTrip=results[4]
    hDirection=results[5]
    hBlock=results[6]
    patternRecordID=results[7]
    hTripStart=results[8]
    hTripEnd=results[9]
    hIStopID=results[10]
    hTStopID=results[11]
    hIStopName=results[12]
    hTStopName=results[13]
    hSegmentDistance=results[14]


    if hBlock not in currentDay.getBlockNumbers():
        if hTStopID==None:
            return currentDay
        else:
            iStop=Stop(hIStopID,None,hTripStart,0,0,0,hIStopName,hStopSeq)
            tStop=Stop(hTStopID,None,hTripEnd,0,0,0,hTStopName,hStopSeq)           #what do I do with stop StopSeq
            newSegment=Segment(iStop, tStop,0,0, hTripStart,hTripEnd, None, hSegmentDistance )
            newTrip=Trip( hTrip, 0, 0, 0, 0, 0, 0, 0, hRoute, hDirection, None)
            newTrip.addSeg(newSegment)
            newTrip.stops.append(iStop)
            newTrip.stops.append(tStop)
            newBlock=Block(hBlock)
            newBlock.addTrip(newTrip)
            currentDay.addBlock(newBlock)
            return currentDay
    else:
        currentBlock=currentDay.getBlock(hBlock)
        if hTStopID==None:
            return currentDay
        else:
            if hTrip not in currentBlock.getTripNumbers():
                iStop=Stop(hIStopID,None,hTripStart,0,0,0,hIStopName,hStopSeq)
                tStop=Stop(hTStopID,None,hTripEnd,0,0,0,hTStopName,hStopSeq)           #self, stopId, messageId, stopTime, onboard, boards, alights, stopName,stopseq
                newSegment=Segment(iStop, tStop,0,0, hTripStart,hTripEnd, None, hSegmentDistance )
                newTrip=Trip(  hTrip, 0, 0, 0, 0, 0, 0, 0, hRoute, hDirection, None)
                newTrip.addSeg(newSegment)
                newTrip.stops.append(iStop)
                newTrip.stops.append(tStop)
                currentBlock.addTrip(newTrip)
                return currentDay
            else:
                currentTrip=currentBlock.getTrip(hTrip)
                iStop=currentTrip.stops[-1]
                tStop=Stop(hTStopID,None,hTripEnd,0,0,0,hTStopName,hStopSeq)           #what do I do with stop StopSeq
                newSegment=Segment(iStop, tStop,0,0, hTripStart,hTripEnd, None, hSegmentDistance )
                currentTrip.stops.append(tStop)
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
            compareTrips(actualBlock.getTrip(hTrip.tripNumber), hTrip)

def compareTrips(aTrip, hTrip):

    aIndex=0
    hIndex=0
    while aIndex <= len(aTrip.segments) and hIndex <= len(hTrip.segments):
        aSegment = aTrip.segments[aIndex]
        hSegment = hTrip.segments[aIndex]
        if hSegment.segmentID[1] == None:
            hIndex+=1
        elif aSegment.segmentID[0] == hSegment.segmentID[0] and aSegment.segmentID[1] == hSegment.segmentID[1]:
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
