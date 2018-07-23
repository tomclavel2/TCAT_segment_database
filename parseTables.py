from Classes import Day, Block, Trip, Segment, Stop

def parse(currentDay,results):
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
    if cBlockNumber not in currentDay.getBlockNumbers():
        newBlock=Block(cBlockNumber)
        newTrip = Trip (cTripNumber, cBus, cStopId, cVMHTime, cMessageTypeId, cOnboard, cBoards, cAlights) #(self, tripNumber, bus, stop, stopTime, messageId, onboard, boards, alights
        newBlock.addTrip(newTrip)
        currentDay.addBlock(newBlock)
        currentDay.addBus(cBus)
        return currentDay
    else:
        currentBlock=currentDay.getBlock(cBlockNumber)
        if cTripNumber not in currentBlock.getTripNumbers():
            newTrip = Trip(cTripNumber, cBus, cStopId, cVMHTime, cMessageTypeId, cOnboard, cBoards, cAlights)
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
                    currentStop=Stop(cStopId,cMessageTypeId,cVMHTime,cOnboard,cBoards,cAlights)#Stop(stop, messageId, stopTime, onboard, boards, alights)
                    currentTrip.addSegment(currentStop)
                    return currentDay
            else:
                if cStopId == currentTrip.lastStop.stopId:
                    return currentDay
                else:
                    currentStop=Stop(cStopId,cMessageTypeId,cVMHTime,cOnboard,cBoards,cAlights)#Stop(stop, messageId, stopTime, onboard, boards, alights)
                    currentTrip.addSegment(currentStop)
                    return currentDay


def display(currentDay):
    print(currentDay.date)
    for b in currentDay.getBlocks():
        print('block ' + str(b.blockNumber))
        for t in b.getTrips():
            print('trip ' + str(t.tripNumber))
            for s in t.getSegments():
                print(s.segmentID,  end=' ; ')
