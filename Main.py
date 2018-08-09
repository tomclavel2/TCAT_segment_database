#This file is a new version of the old Connection.py file
#It's purpose is to establish a connection to the data base, pose queries to pull
# the relevant information then use the functions in Parse to create classes described
# in Classes to organize the information.

import pyodbc
import sys
from Parse import parseActual, display, parseHistorical, compareDay, compareBlocks, compareTrips, adjustOnboards
from Classes import Day, Block, Trip, Segment, Stop, Deviations, dTrip
from datetime import timedelta, date, datetime  #for date conversion 
from Deviations import report

connection = pyodbc.connect(
    r'DRIVER={ODBC Driver 11 for SQL Server};'
    r'SERVER=AVAILDEV;'                               #need server name here
    r'DATABASE=Utilities;'                            #need database name here
    r'UID=Adam;'
    r'PWD=*L12c3by'
    )

#This function issues two queries to the databases to pull information about the actual and the scheduled trips.
#It pulls all the information from a series of columns and the information is parsed row by row using the parseActual
#and the parseHHistorical function. After that the function calls compare on the actual day object and the scheduled 
#day object to compare the segements. 

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)



def createDays(date):
   # my_date_string = "2017/12/09"
   # date1="2017-12-09"
   # d = datetime.strptime(my_date_string, "%Y/%m/%d")
    print(date)
    cursor = connection.cursor()
    

    selectHistoricalInformation = ( " SELECT service_day,trip_seq, stop_seq, route, trip, direction, block,Pattern_Record_Id, trip_start, trip_end, iStop_Id, tStop_Id,iStop_descr,tStop_descr, segment_feet"
                                " FROM dbo.vHistorical_Stop_Schedule "
                                " WHERE service_day = ?"
                                " ORDER BY trip_seq, stop_seq asc")


    selectActualInformation = ( " SELECT  Message_Type_Id, service_date, block, route, trip, dir, vmh_time, bus, Onboard, boards, alights, Stop_Id,Internet_Name "
                                " FROM dbo.vActual_History"
                                " WHERE service_date =? "
                                "ORDER BY vmh_time asc")
   

    cursor.execute(selectActualInformation, date)
    currentActualDay=Day(date)
    results = cursor.fetchone()
    while results:
        currentActualDay=parseActual(currentActualDay, results)
        results = cursor.fetchone()

    print(1)

    cursor.execute(selectHistoricalInformation,date)
    currentHistoricalDay=Day(date)
    results = cursor.fetchone()
    while results:
        currentHistoricalDay=parseHistorical(currentHistoricalDay, results)
        results = cursor.fetchone()
    print(2)
    compareDay(currentActualDay,currentHistoricalDay)
    adjustOnboards(currentActualDay)
    writeToSegments(currentActualDay, currentHistoricalDay,cursor)
    checkSequence(currentActualDay)
    report(currentActualDay)
    #for t in currentActualDay.deviations.tripsMissed:
    #    print(t)



def checkSequence(currentActualDay):
    for b in currentActualDay.blocks:
        for t in b.trips:
            ind=0
            while ind < len(t.segments):
                if ind==0 and t.segments[ind].segmentSeq != 1:
                    print(str(b.blockNumber)+':'+str(t.tripNumber)+' case 1')
                    ind=ind+1
                else:
                    if ind>0 and t.segments[ind].segmentSeq != (t.segments[ind-1].segmentSeq + 1) :
                        print(str(b.blockNumber)+' : '+str(t.tripNumber)+'case 2')
                    ind=ind+1

def writeToSegments(currentActualDay, currentHistoricalDay,cursor):
    for b in currentActualDay.blocks:
        for t in b.trips:
            for s in t.segments:
                day=currentActualDay.date
                bus=s.bus
                blockNumber=b.blockNumber
                route=t.route
                tripNumber=t.tripNumber
                direction=t.direction
                iStopNumber=s.segmentID[0].stopID
                iStopName=s.segmentID[0].stopName
                iStopType=s.segmentID[0].messageTypeID
                iStopSeen=s.segmentID[0].seen
                tStopNumber=s.segmentID[1].stopID
                tStopName=s.segmentID[1].stopName
                tStopType=s.segmentID[1].messageTypeID
                tStopSeen=s.segmentID[1].seen
                boards=s.segmentID[0].boards 
                alights=s.segmentID[1].alights
                onboard=s.onboard
                adjOnboard=s.adjustedOnboard
                iStopTime=s.segmentID[0].stopTime
                tStopTime=s.segmentID[1].stopTime
                segDistance=s.distance
                pattern=t.pattern
                segseq=s.segmentSeq
                cursor.execute(" INSERT INTO dbo.Segments (ServiceDate, Bus, Block, Route, Trip, Pattern, Direction, iStopID, iStopName, iStopMessageID, iStopSeen, tStopID, tStopName, tStopMessageID, tStopSeen, Boards, Alights, Onboard,AdjustedOnboard , SegmentSequence, StartTime, EndTime, SegmentFeet)"
                " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", day, bus, blockNumber,route, tripNumber,pattern,direction, iStopNumber,iStopName,iStopType, iStopSeen, tStopNumber,tStopName,tStopType, tStopSeen, boards, alights ,onboard ,adjOnboard ,segseq,iStopTime,tStopTime,segDistance )
                connection.commit()


y1 = int(sys.argv[1])
m1 = int(sys.argv[2])
d1 = int(sys.argv[3])

y2 = int(sys.argv[4])
m2 = int(sys.argv[5])
d2 = int(sys.argv[6])

start_date = date(y1, m1, d1)
end_date = date(y2, m2, d2)
for single_date in daterange(start_date, end_date):
    day= single_date.strftime("%Y-%m-%d")
    createDays(day)


connection.close()


