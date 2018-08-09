from Classes import Day, Block, Trip, Segment, Stop, Deviations, dTrip

 #This function is responsible for looking at every row in the actual stop history table and creating objects for the blocks, trips, segments and stops
 # lines 8-20 are variables that store the information I pulled from one row of the SQL table

def parseActual(currentDay,results):
    cMessageTypeID=results[0]
    cBlockNumber=results[2]
    cRoute=results[3]
    cTripNumber=results[4]
    cDir=results[5]
    cVMHTime=results[6]
    cBus=results[7]
    cOnboard=results[8]
    cBoards=results[9]
    cAlights=results[10]
    cStopID=results[11]
    cStopName=results[12]

    if cStopID==0:                                          #Need to actually deal with this case in compare(), but I put it here to check what it would do
        return currentDay

    elif cBlockNumber not in currentDay.getBlockNumbers():                        #if the block is not in the list of blocks for our current day  object so we create a new block object and trip object
        newBlock=Block(cBlockNumber)
        newTrip = Trip (cTripNumber, cBus, cStopID, cStopName, cVMHTime, cMessageTypeID, cOnboard, cBoards, cAlights,cRoute, cDir, 0)  # the call to create a new trip also creates a new stop object
        newBlock.addTrip(newTrip)
        currentDay.addBlock(newBlock)    
        currentDay.addBus(cBus)
        return currentDay
    else:
        currentBlock=currentDay.getBlock(cBlockNumber)                          #the block number from the list of rows must be in the day objects list of blocks so i get it by using a function that takes a integer block number and returns the block object
        if cTripNumber not in currentBlock.getTripNumbers():                    # if the trip number is not in the list of trips in the block we are ooking at then we make a new trip
            newTrip =Trip (cTripNumber, cBus, cStopID, cStopName, cVMHTime, cMessageTypeID, cOnboard, cBoards, cAlights,cRoute, cDir, 0)
            currentBlock.addTrip(newTrip)
            currentDay.addBus(cBus)
            return currentDay
        else:
            currentTrip = currentBlock.getTrip(cTripNumber)                     #using the trip number from the row we get a reference to the trip object that matches the row we are looking at
            if cBus != currentTrip.currentBus:                                  # if the bus from the row does not match the last bus used by the trip we have to add it to the trip,
                currentTrip.buses.append(cBus)
                currentTrip.currentBus=cBus                                       #adds the bus from the row to the list of buses used by the trip and makes it the most recently used
                currentDay.busesUsed.append(cBus)                               #A list of buses used can be found in currentDay.busesUsed
                if cStopID == currentTrip.lastStop.stopID:                      #if the stop number matches the last stop seen we disregard it, this needs to be changed to account for alights and boards
                    currentTrip.lastStop.onboard=currentTrip.lastStop.onboard+cBoards-cAlights
                    currentTrip.lastStop.seen+=1
                    return currentDay
                else: 
                    currentStop=Stop(cStopID,cStopName, cMessageTypeID,cVMHTime,cOnboard,cBoards,cAlights,1)  #If it gets here then all we have to do is create a new stop object, and then
                    currentTrip.addSegment(currentStop,cBus)                    #use the add segement function to create a segment from the new stop and lst stop
                    return currentDay
            else:
                if cStopID == currentTrip.lastStop.stopID: 
                    currentTrip.lastStop.onboard=currentTrip.lastStop.onboard+cBoards-cAlights                     #same thing as line 39, but for the case of the same bus
                    currentTrip.lastStop.seen+=1
                    return currentDay
                else:
                    currentStop=Stop(cStopID,cStopName, cMessageTypeID,cVMHTime,cOnboard,cBoards,cAlights,1) #same thing as line 42, but for the case of the same bus
                    currentTrip.addSegment(currentStop,cBus)
                    return currentDay

#Given a day object this function will iterate through all of the block, for each block it iterates through all the trips in that block, and for each trip2
# it iterates through the list of segments and prints them, This function is primarily for my own testsing
def display(currentDay):
    print(currentDay.date)
    for b in currentDay.blocks:
        print('block ' + str(b.blockNumber))
        for t in b.trips:
            print('trip ' + str(t.tripNumber))
            for s in t.segments:
                print('Segment : ' +  '(' + str(s.segmentID[0].stopID) +' , ' +str(s.segmentID[1].stopID) +')', end= '; ')
                print("seg distance"+str(s.distance))


#this function is the same as parse actual but works on the scheduled day
#lines 68 to 81 are variables that hold the information taken from one row
def parseHistorical(currentDay,results):
    sSegSeq=results[2]
    sRoute=results[3]
    sTrip=results[4]
    sDirection=results[5]
    sBlock=results[6]
    pattern=results[7]
    sTripStart=results[8]
    sTripEnd=results[9]
    sIStopID=results[10]
    sTStopID=results[11]
    sIStopName=results[12]
    sTStopName=results[13]
    sSegmentDistance=results[14]
    if sRoute==999:
        return currentDay
    if sBlock not in currentDay.getBlockNumbers():                              # if the block from the row is not in the list of blocks from the day then we create two stop objects, make a segment from them, and create a new trip and block object
        if sTStopID==None:                                                      # if the terminal stop number is null we ignore it
            return currentDay
        else:      
            iStop=Stop(sIStopID, sIStopName, 0,0,0,0,0,0)
            tStop=Stop(sTStopID, sTStopName, 0,0,0,0,0,0)
            newSegment=Segment(iStop, tStop,0, sSegmentDistance,sSegSeq )    
            newTrip=Trip( sTrip, 0, 0, 0, 0, 0, 0, 0, 0, sRoute, sDirection, pattern) #( tripNumber, bus, stopID, stopName, stopTime, messageTypeID, onboard, boards, alights,route,direction,pattern)
            newTrip.segments.append(newSegment)
            newTrip.numberOfStops+=1

            newTrip.stops.append(iStop)
            newTrip.stops.append(tStop)
            newBlock=Block(sBlock)
            newBlock.addTrip(newTrip)
            currentDay.addBlock(newBlock)
            return currentDay
    else:
        currentBlock=currentDay.getBlock(sBlock)                                        #since the current block already exsists we get a referece to it
        if sTStopID==None:                                                          # if the terminal stop number is null we ignore it
            return currentDay
        else:
            if sTrip not in currentBlock.getTripNumbers():                      # if the trip from the row is not an object yet we have to create two stop objects, used them to create a segement and then create a trip
                iStop=Stop(sIStopID, sIStopName, 0,0,0,0,0,0)
                tStop=Stop(sTStopID, sTStopName, 0,0,0,0,0,0)
                newSegment=Segment(iStop, tStop,0, sSegmentDistance,sSegSeq )   
                newTrip=Trip( sTrip, 0, 0, 0, 0, 0, 0, 0, 0, sRoute, sDirection, pattern)
                newTrip.segments.append(newSegment)
                newTrip.numberOfStops+=1

                newTrip.stops.append(iStop)
                newTrip.stops.append(tStop)
                currentBlock.addTrip(newTrip)
                return currentDay
            else:
                currentTrip=currentBlock.getTrip(sTrip)
                if sIStopID == currentTrip.stops[-2].stopID and sTStopID == currentTrip.stops[-1].stopID :     
                    return currentDay
                else:
                    iStop=currentTrip.stops[-1]
                    tStop=Stop(sTStopID, sTStopName, 0,0,0,0,0,0)
                    newSegment=Segment(iStop, tStop,0, sSegmentDistance, sSegSeq )   
                    currentTrip.stops.append(tStop)
                    currentTrip.segments.append(newSegment)
                    currentTrip.numberOfStops+=1
                    return currentDay
                  #we get a reference to the trip object and use it to form a new segemnt by using the last stop and the new stop
                

def compareDay(actualDay, scheduledDay):
    actualDay.deviations=Deviations()
    for sBlock in scheduledDay.blocks:
        if sBlock.blockNumber not in actualDay.getBlockNumbers():
            actualDay.deviations.blocksMissed.append(sBlock.blockNumber)
            for sTrip in sBlock.trips:
                dtrip= dTrip(sBlock.blockNumber, sTrip)
                actualDay.deviations.tripsMissed.append(dtrip)
                for sStop in sTrip.stops:
                    actualDay.deviations.stopsMissed.append(sStop.stopID)
        else:
            compareBlocks(actualDay,actualDay.getBlock(sBlock.blockNumber), sBlock)

def compareBlocks(actualDay,actualBlock,scheduledBlock):
    for sTrip in scheduledBlock.trips:
        if sTrip.tripNumber not in actualBlock.getTripNumbers():
            dtrip= dTrip(scheduledBlock.blockNumber, sTrip)
            actualDay.deviations.tripsMissed.append(dtrip)
            for sStop in sTrip.stops:
                actualDay.deviations.stopsMissed.append(sStop.stopID)
        else:
            aTrip= actualBlock.getTrip(sTrip.tripNumber)
            aTrip.updateTrip(sTrip.route, sTrip.pattern)

            compareTrips(actualDay, aTrip, sTrip)

def compareTrips(actualDay, aTrip, sTrip):
    aIndex=0
    sIndex=0
    while aIndex < len(aTrip.segments) and sIndex < len(sTrip.segments):
        aSegment = aTrip.segments[aIndex]
        sSegment = sTrip.segments[sIndex]
        checkCases(aSegment,sSegment)
        if aSegment.segmentID[0].stopID == sSegment.segmentID[0].stopID and aSegment.segmentID[1].stopID == sSegment.segmentID[1].stopID:
            aSegment.updateSegment(sSegment.distance, sSegment.segmentSeq)
            aIndex +=1
            sIndex +=1

        elif aSegment.segmentID[0].stopID == sSegment.segmentID[0].stopID :
            y0 = sTrip.findSecondStop(aSegment.segmentID[1].stopID, sIndex)
            if y0 == -1:      #used to have the case where it looks for a segment match but i took that out since neither of them ever worked
                indexOne = sTrip.findMatch(aSegment.segmentID[0].stopID,  aSegment.segmentID[1].stopID, sIndex)
                indexTwo = aTrip.findMatch(sSegment.segmentID[0].stopID,  sSegment.segmentID[1].stopID, aIndex)
                if indexOne==-1 and indexTwo==-1:
                    print('thought so')
                else :
                    print ('wow '+ 'index one :'+str(indexOne)+ 'index 2 :' +str(indexTwo) )
                if indexOne == -1:
                    aIndex+=1 #also need to mark down that unexpected stop was made
                if indexTwo == -1:
                    actualDay.deviations.stopsMissed.append(sSegment.segmentID[1].stopID)
                    sIndex+=1
                elif indexOne < indexTwo :
                    sIndex= indexOne
                else:
                    aIndex=indexTwo ##NEED TO CHECK THIS CASE
                actualDay.deviations.nonscheduledStopsMade.append(aSegment.segmentID[1].stopID)
                aIndex+=1
            else:
                 seg=sTrip.segments[y0]
                 newSegment1 = Segment(aSegment.segmentID[0], sSegment.segmentID[1], aSegment.bus, sSegment.distance, sSegment.segmentSeq )
                 newSegment2 = Segment(seg.segmentID[0], aSegment.segmentID[1], aSegment.bus, seg.distance, seg.segmentSeq )
                 sPart=sTrip.segments[sIndex+1:y0]
                 aPart=aTrip.segments[:aIndex]
                 aPart.append(newSegment1)
                 aPart.extend(sPart)
                 aPart.append(newSegment2)
                 size=len(aPart)
                 aPart.extend(aTrip.segments[aIndex+1:])
                 aTrip.segments=aPart
                 aIndex=size
                 sIndex = y0 +1

        elif  aSegment.segmentID[0].stopID == sSegment.segmentID[1].stopID:
            sIndex += 1
        elif aSegment.segmentID[1].stopID == sSegment.segmentID[1].stopID:
            sIndex += 1
            aIndex += 1

        else:
            indexOne = sTrip.findMatch(aSegment.segmentID[0].stopID,  aSegment.segmentID[1].stopID, sIndex)
            indexTwo = aTrip.findMatch(sSegment.segmentID[0].stopID,  sSegment.segmentID[1].stopID, aIndex)
            
            #if indexOne==-1 and indexTwo==-1:     stub
            #elif indexOne==-1 and indexTwo!=-1:
            #elif indexOne==-1 and indexTwo!=-1:
            #else:
            indexPartial= sTrip.findFirstStop(aSegment.segmentID[0].stopID, sIndex)
             
            if indexPartial == -1:
                actualDay.deviations.nonscheduledStopsMade.append(aSegment.segmentID[0].stopID)  
                break                                                                             #also need to mark down that unexpected stop was made
            elif indexTwo==-1:
                sPart=sTrip.segments[sIndex:indexPartial]
                a1=aTrip.segments[0:aIndex]
                a2=aTrip.segments[aIndex:]
                a1.extend(sPart)
                size=len(a1)
                a1.extend(a2)
                aTrip.segments=a1
                aIndex=size
                sIndex=indexPartial
            else:
                sIndex+=1







def checkCases(aSegment,sSegment):
    if aSegment.segmentID[0].stopID == 1512 or aSegment.segmentID[0].stopID == 1513 and sSegment.segmentID[0].stopID == 1513 or sSegment.segmentID[0].stopID == 1512 and aSegment.segmentID[1].stopID == sSegment.segmentID[1].stopID :
         aSegment.updateSegment(sSegment.distance, sSegment.segmentSeq)
         aSegment.segmentID[0].stopID = 1513
    elif  aSegment.segmentID[0].stopID == sSegment.segmentID[0].stopID  and aSegment.segmentID[1].stopID == 1512 or aSegment.segmentID[1].stopID == 1513 and sSegment.segmentID[1].stopID== 1513 or  sSegment.segmentID[1].stopID== 1512:
        aSegment.updateSegment(sSegment.distance, sSegment.segmentSeq)
        aSegment.segmentID[1].stopID = 1513


def nones(actualDay):
    for b in actualDay.blocks:
        for t in b.trips:
            s=0
            while s < len(t.segments):
                if t.segments[s].segmentID[1] == none and t.segments[s+1].segmentID[1] != None:
                    t=5


def adjustOnboards(currentActualDay):
    for b in currentActualDay.blocks:
        for t in b.trips:
            index=0
            length= len(t.segments)
            while index < length:    
                s = t.segments[index]
                if index == 0:
                    s.onboard = s.segmentID[0].boards
                    t.boards = s.segmentID[0].boards
                    t.alights= s.segmentID[0].alights
                elif index == length -1 :
                    s.onboard = t.segments[index-1].onboard + s.segmentID[0].boards - s.segmentID[0].alights
                    t.boards += (s.segmentID[0].boards + s.segmentID[1].boards)
                    t.alights += (s.segmentID[0].alights + s.segmentID[1].alights)
                else:
                    s.onboard = t.segments[index-1].onboard + s.segmentID[0].boards - s.segmentID[0].alights
                    t.boards += s.segmentID[0].boards
                    t.alights += s.segmentID[0].alights
                index += 1

    for b in currentActualDay.blocks:
        for t in b.trips:
            error = t.boards - t.alights 
           # print('error :'+str(error)+'boards :'+str(t.boards))
            if error == 0:
                break
            else:
                if error > 0:

                    t.adjustment= error/t.boards
                   # print(t.adjustment)
                    index=0
                    length= len(t.segments)
                    while index < length:    
                        s = t.segments[index]
                        if index == 0:
                            adjboards = s.segmentID[0].boards * t.adjustment
                            s.adjustedOnboard= adjboards
                        else:
                            adjboards = s.segmentID[0].boards * t.adjustment
                            s.adjustedOnboard = t.segments[index-1].adjustedOnboard + adjboards - s.segmentID[0].alights
                       # print('magic :'+str(s.adjustedOnboard))    
                        index += 1

                elif error < 0:
                    t.adjustment= (error * -1) / t.alights
                   # print(t.adjustment)
                    index=0
                    length= len(t.segments)
                    while index < length:    
                        s = t.segments[index]
                        if index == 0:
                            s.adjustedOnboard = s.segmentID[0].boards
                            t.boards = s.onboard
                        else:
                            adjalights = s.segmentID[0].alights * t.adjustment
                            s.adjustedOnboard = t.segments[index-1].adjustedOnboard - adjalights +  s.segmentID[0].boards
                        index += 1
                        #print('wooow :'+str(s.adjustedOnboard))


            
                #print('block :'+str(b.blockNumber)+ ', trip :'+str(t.tripNumber)+ ', finalOnboard :' + str(t.adjustment))
               
            

            
