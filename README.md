# TCAT_segment_database

Main.py
====================================================================================================================================
This file is responsible for establishing a connection to the SQL database  and the contorl flow of 
the program.
This file can be run using the command line by navigating to the folder it is in, currently this is
Adam\Documents then issuing the command      
python main.py 2017 11 01 2017 11 15
The 6 integer arguements passed are necessary, the format must be yyyy mm dd yyyy mm dd
they specify the date range to be processed and begin on the first date and process every day up 
until but not including the last date. This means that the above command does not look at 2017-11-15.

-------------------------------------------------------------------------------------------------
def createDays(date):

Inputs: requires a string input called date, which is that service date that will be processed
Returns: a 2-d array containing the actualDay object and the scheduledDay object
This function issues two queries to the databases to pull information about the actual and the scheduled trips.
It pulls all the information from a series of columns  and stores it in a two dimensional array,
which is stored in the cursor object. 
cursor.execute(selectActualInformation, date)  issues the query passed in the string selectActualInformation
using the date string passed in through the createDays(date) arguement date. Then I create a day Object.
results = cursor.fetchone() grabs one row from the 2-d array containing the information I pulled from
the database, and calls parseActual() to process this row. The fetchone() function removes one row 
from the array so each time it is called the array grows shorter. The while loop runs as long as 
there is information in array that has not been parsed yet. Inside the while loop I look at a row of 
information and call one of the parse() functions on the information from that row. The parse() function
returns an updated version of the day with the information from that row, and then another row of 
data from the array is place in results by results = cursor.fetchone(). 
The createDays() function does this first for the actualDay, then for the scheduled day

-------------------------------------------------------------------------------------------
def writeToSegments(actualDay):

Inputs: the day object you want to write to the table
Returns: the function is void, it returns nothing
This function iterates through the all the blocks in a day, the trips in each block, and the 
segments in each trip, writing the information to the Segments database.

--------------------------------------------------------------------------------------------------
def daterange(start_date, end_date):

Inputs: start_date- a date object representing the the first date in a range, end_date- a date object
       representing the final date in a the range.
This is a helper function used to itterate through days given a start date object and an ending
date object. It is used to create a sort of mirror to the range() function in python, but for 
date objects.

-------------------------------------------------------------------------------------------------
def main():

This is the function that takes the arguements passed into the file, creates two date objects for 
them and then uses the daterange function to iterrate through every day between them and call the 
createDays funtion.
It then compares the actualDay object and the scheduledDay object using compareDay(),
Adds onboard and adjusted Onboard information to the updated actualDay using adjustedOnbboards(),
Writes the information from the actualDay to the Segments table using writeToSegments(),
Looks for deviations in the trip using checkSequece(), and generates a breif report of the 
deviations using report(). After processing all days it closes the connection to the table.

------------------------------------------------------------------------------------------------------

Parse.py
========================================================================================================




Classes.py
========================================================================================================


Compare.py
========================================================================================================
def compareDay(actualDay, scheduledDay):

Inputs: actualDay- the day object for the actual day, scheduledDay- the day object for the scheduled day
Returns: the function is void, it updates information about the day object
This function is used to compare the scheduled day and the actual day and to record and deviations
between the two days, to update the information in the actual day and to infer stops that were not
recorded in the actual day
It iterates through all the blocks in the scheduled day, and if it cannot find that block number in
the actaul day it adds that block number to the missed block list in the deviations. It then adds all
the trips and stops in the that block to the deviations object. While doing this it creates a dTrip
object which is just a modification of the trip object that also conatains the block of the trip.
If the scheduled block has a match in the actual day then it calls the compareBlocks() function
passing the actualDay, actualBlock and scheduledBlock as arguements.
