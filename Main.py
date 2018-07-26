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

cursor = connection.cursor()

selectHistoricalInformation = ( " SELECT service_day,trip_seq, route, trip, direction, block, trip_start, trip_end, iStop_Id, tStop_Id, segment_miles"  # the column you want to pull in
                                " FROM dbo.vHistorical_Stop_Schedule "       # the table you are accessing
                                " WHERE service_day = '2017-01-21'"
                                " ORDER BY trip_seq asc")


selectActualInformation = ( " SELECT  Message_Type_Id, service_date, block, route, trip, dir, vmh_time, bus, Onboard, boards, alights, Stop_Id,Internet_Name "  # what other columns
                                " FROM dbo.vActual_History"
                                " WHERE service_date = '2017-01-21'"
                                " ORDER BY vmh_time asc")


cursor.execute(selectActualInformation)
currentActualDay=Day('2017-01-21')



results = cursor.fetchone()
while results:
    currentActualDay=parseActual(currentActualDay, results)
    results = cursor.fetchone()
#display(currentActualDay)


cursor.execute(selectHistoricalInformation)
currentHistoricalDay=Day('2017-01-21')
results = cursor.fetchone()
while results:
     currentHistoricalDay=parseHistorical(currentHistoricalDay, results)
     results = cursor.fetchone()
display(currentHistoricalDay)

#writeToSegments = (" INSERT INTO dbo.Segments (ServiceDate, Bus, Block, Route, Trip, Pattern, Direction, iStopID, iStopName, tStopID,tStopName, Boards, Alights, Onboard) VALUES ()"" )

for b in currentActualDay.blocks:
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
            tStopNumber=s.segmentID[0].stopId
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
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", day, bus, blockNumber,route, tripNumber,0,direction, iStopNumber,iStopName,iStopType, tStopNumber,tStopName,iStopType, numberboards, numberalights,onboard,stopseq,iStopTime,tStopTime, segDist )
            connection.commit()

connection.close()
