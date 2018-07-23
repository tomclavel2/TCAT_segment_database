import pyodbc
from parseTables import parse, display
from Classes import Day, Block, Trip, Segment, Stop

connection = pyodbc.connect(
    r'DRIVER={ODBC Driver 11 for SQL Server};'        #need to confirm the driver
    r'SERVER=AVAILDEV;'                               #need server name her
    r'DATABASE=Utilities;'                            #need database name here
    r'UID=Adam;'
    r'PWD=*L12c3by'
    )


cursor = connection.cursor()

selectHistoricalInformation = ( " SELECT Pattern_Record_Id, trip, tStop_Id"  # what other columns
                                " FROM dbo.vHistorical_Stop_Schedule "
                                " WHERE service_day = '2017-01-21'" )    # need to confirm the table name

selectActualInformation = ( " SELECT  Message_Type_Id, service_date, block, route, trip, dir, vmh_time, bus, Onboard, boards, alights, Stop_Id "  # what other columns
                                " FROM dbo.vActual_History"
                                " WHERE service_date = '2017-01-21'")

#cursor.execute(selectHistoricalInformation)
cursor.execute(selectActualInformation)

currentDay=Day('2017-01-21')

results = cursor.fetchone()
while results:
    currentDay=parse(currentDay, results)
    results = cursor.fetchone()          # to parse that particular row
display(currentDay)

#cursor.execute(selectActualInformation)
#results = cursor.fetchone()
#while results:
#     print(results[0], results[1], results[2])     # Need to make a parse table function
#     results = cursor.fetchone()                        # to parse that particular row



connection.close()


# for row in cursor:                                      # could either use results or just use the cursor
#    print('row = %r' % (row,))

# for row in cursor:
#     print('row = %r' % (row,))
