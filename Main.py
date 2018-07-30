#This file is a new version of the old Connection.py file
#It's purpose is to establish a connection to the data base, pose queries to pull
# the relevant information then use the functions in Parse to create classes described
# in Classes to organize the information.

import pyodbc
from Parse import parseActual, display, parseHistorical, compareDay, compareBlocks, compareTrips
from Classes import Day, Block, Trip, Segment, Stop



connection = pyodbc.connect(
    r'DRIVER={ODBC Driver 11 for SQL Server};'
    r'SERVER=AVAILDEV;'                               #need server name here
    r'DATABASE=Utilities;'                            #need database name here
    r'UID=Adam;'
    r'PWD=*L12c3by'
    )


def createDays(date):
    cursor = connection.cursor()
    print(str(date))
    selectHistoricalInformation = ( " SELECT service_day,trip_seq, stop_seq, route, trip, direction, block,Pattern_Record_Id, trip_start, trip_end, iStop_Id, tStop_Id,iStop_descr,tStop_descr, segment_feet"
                                " FROM dbo.vHistorical_Stop_Schedule "
                                " WHERE service_day = '2017-01-25' "
                                " ORDER BY trip_seq, stop_seq asc")


    selectActualInformation = ( " SELECT  Message_Type_Id, service_date, block, route, trip, dir, vmh_time, bus, Onboard, boards, alights, Stop_Id,Internet_Name "
                                " FROM dbo.vActual_History"
                                " WHERE service_date = '2017-01-25' "
                                " ORDER BY vmh_time asc")


    cursor.execute(selectActualInformation)
    currentActualDay=Day(date)
    results = cursor.fetchone()
    while results:
        currentActualDay=parseActual(currentActualDay, results)
        results = cursor.fetchone()
    #display(currentActualDay)


    cursor.execute(selectHistoricalInformation)
    currentHistoricalDay=Day(date)
    results = cursor.fetchone()
    while results:
        currentHistoricalDay=parseHistorical(currentHistoricalDay, results)
        results = cursor.fetchone()
    #display(currentHistoricalDay)
    testUpload(currentActualDay,currentHistoricalDay,cursor)
    #compareDay(currentActualDay,currentHistoricalDay)


def testUploadHistorical(currentHistoricalDay,cursor):
    for b in currentHistoricalDay.blocks:
        for t in b.trips:
            for s in t.segments:
                hblocknum=b.blockNumber
                htripnum=t.tripNumber
                hiStopNumber=s.segmentID[0].stopId
                htStopNumber=s.segmentID[1].stopId
                print('('+str(hiStopNumber)+' , '+str(htStopNumber) +')')
                cursor.execute(" INSERT INTO dbo.seg_trips (block2, trip2 , histop1, htstop2)"
                " VALUES(?,?,?,?)", hblocknum, htripnum, hiStopNumber, htStopNumber)
                connection.commit()

                
def test(currentActualDay, currentHistoricalDay,cursor):
    for hb in currentHistoricalDay.blocks:
        b=currentActualDay.getBlock(hb.blockNumber)
        if b==None:
            print('Whoops')
        else:
            print(str(b.blockNumber)+', '+ str(hb.blockNumber))
            for ht in hb.trips:
                t=b.getTrip(ht.tripNumber)
                if t==None:
                    print(str(ht.tripNumber)+'; '+ 'could not find')
                else:
                    print(str(t.tripNumber)+'; '+ str(ht.tripNumber))
                    for s in ht.stops:
                        print(s.stopId)


def testUpload(currentActualDay, currentHistoricalDay,cursor):
    for b in currentActualDay.blocks:
        hb=currentHistoricalDay.getBlock(b.blockNumber)
        for t in b.trips:
            if hb==None:
                break
            else:
                ht=hb.getTrip(t.tripNumber)
                #ind=0
                if ht==None:
                    break
                else:
                    #for s in t.segments:
                    for s, hseg in zip(t.segments,ht.segments):
                    #   if ind >= len(ht.segments):
                    #        break
                    #    else:
                            ablocknum=b.blockNumber
                            atripnum=t.tripNumber
                            aiStopNumber=s.segmentID[0].stopId
                            atStopNumber=s.segmentID[1].stopId
                    #        hseg=ht.segments[ind]
                            hblocknum=hb.blockNumber
                            htripnum=ht.tripNumber
                            hiStopNumber=hseg.segmentID[0].stopId
                            htStopNumber=hseg.segmentID[1].stopId
                        #    ind=ind+1
                        #    print('('+str(hiStopNumber)+' , '+str(htStopNumber) +')')
                            cursor.execute(" INSERT INTO dbo.seg_trips ( ablock, hblock, atrip, htrip, aistop, atstop, histop, htstop)"
                            " VALUES(?,?,?,?,?,?,?,?)", ablocknum,hblocknum, atripnum,htripnum, aiStopNumber,  atStopNumber,hiStopNumber, htStopNumber)
                            connection.commit()

def writeToSegments():
    for b in currentActualDay.blocks:
        hb=currentHistoricalDay.getBlock(b.blockNumber)
        for t in b.trips:
            for s in t.segments:
                day=currentActualDay.date
                bus=s.bus
                blockNumber=b.blockNumber
                route=t.route
                tripNumber=t.tripNumber
                direction=t.direction
                iStopNumber=s.segmentID[0].stopId
                iStopName=s.segmentID[0].stopName
                iStopType=s.segmentID[0].messageId

                tStopNumber=s.segmentID[1].stopId
                tStopName=s.segmentID[1].stopName
                tStopType=s.segmentID[1].messageId
                numberboards=s.numberBoardsInitialStop
                numberalights=s.numberAlightsTerminalStop
                onboard=s.onboard
                stopseq=0
                iStopTime=s.segmentID[0].stopTime
                tStopTime=s.segmentID[0].stopTime
                segDist=s.distance
                cursor.execute(" INSERT INTO dbo.Segments (ServiceDate, Bus, Block, Route, Trip, Pattern, Direction, iStopID, iStopName,iStopType, tStopID,tStopName, tStopType, Boards, Alights,Onboard,StopSeq,StartTime,EndTime,SegmentFeet)"
                " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", day, bus, blockNumber,route, tripNumber,0,direction, iStopNumber,iStopName,iStopType, tStopNumber,tStopName,tStopType, numberboards, numberalights,onboard,stopseq,iStopTime,tStopTime, segDist )
                connection.commit()
createDays('2017-01-25')
connection.close()
