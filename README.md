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

------------------------------------------------------------------------------------------------------------
def compareBlocks(actualDay,actualBlock,scheduledBlock):

Inputs:actualDay- the day object representing the actual day, actualBlock- block object for the actual 
       block, scheduledBlock- block object for the scheduled block with same block # as actual block
Returns: the function is void, it updates information about the day object
This function iterates through all the trips in a scheduled block and if it cannot find a trip of the
same trip number in  the actual block then it creates a deviation trip and adds it to the deviations 
object for the day. If it finds a matching trip it calls compareTrip() to compare the information
about the segments in the trip.

--------------------------------------------------------------------------------------------------------------
def compareTrips(actualDay,actaulBlock, aTrip, sTrip):

Inputs: actualDay-the actual day object, actualBlock- the actual block object, aTrip- the actual trip
        object, sTrip- the scheduled trip object
Returns: the function is void, it returns nothing it just updates the actualDay object

This function works by looking at the actual and the scheduled versions of a trip, aTrip and sTrip
side by side and comparing the aSegment it is looking at to the sSegment it is looking at by using
two variables to keep track of the indexes of the two segment lists.
           Note: python has a length function len() that returns the length of a list i.e the number of elements in it
                 since indexes in list start at 0 they go until len()-1, which is why the while is < len(list)
#While the aIndex is less than the length of the aTrip segments list and the sIndex is less than the length of sTrip segments:
 #  we get the aSegment at index aIndex of aTrip's segments
 # we get the sSegment at index sIndex of sTrip's segments
   checkCases() is a helper function meant to deal with weird situations that come up, all it does 
       now is deal with an instance where the same stop has a different number in the sTrip than it does in aTrip
   If both stops in the aSegment match both stops in sSegment then we use updateSegment() to add the
       segment distance and sequence number to the aSegment from the sSegment, then we increment both 
       indexes to look at the next pair of segments.
   ElseIf the the first stop of the aSegment matches the first stop of the sSegment then we check 
       If the stop is not is the list of stop in sTip, in which case we mark it as a nonScheduledStop
           mark the aSegment as having a type 2 deviation-nonScheduled stop, and we increment the 
           aIndex to look at the next aSegment  ------------NOT SURE IF I SHOULD INCREMENT sIndex need to test
       Else the stop is in sTrip so we use findSecondStop() to look in the sTrip segment list starting
           at sIndex and try to find a segment whose second stop matches the second stop of aSegment
           If we can't find the stop as a terminal stop i.e. when findSecondStop() returns -1 we try
               to find it as the first stop of some sSegment using findFirstStop() 
               If we can't find it as the inital stop of any of the remaining sSegments then we mark 
                   the segment deviation as a 6 - potential loop on second stop since the stop is in 
                   the sTrip, but it must have occured at some index < our current sIndex, we then 
                   increment the aIndex
               Else we found it as the initial stop of some sSegment, but not as the terminal stop
                   of some sSegment so we move sIndex to that sSegment, we increment aIndex so that
                   they match hopefully and mark the aSegment deviation as 7, found on inital stop
                   but not on terminal stop NOTE: I don't see how this case could occur, but I put this hear to see if it does
           Else we found the second stop of aSegment in sTrip and we now infer stops, we create a 
               new segment1 that is the first stop of aSegment and the second stop of sSegment(this
               will replace aSegment) then we create a segment2 that is the the segment that was found
               by using findSecondStop(), but we update the second stop of the sSegment to include
               the information from the aSegment second stop. Then we grab all segments in sTrip between
               these two stops and mark them all as having a deviation of 1 - infered stop. We insert
               them all into the aTrip segments, then adjust aIndex to point to the next segment after 
               segment 2 and adjust sIndex to the next index after the one that was returned by findSecondStop()
   ElseIf the first stop in aSegment matches the second stop in sSegment then we increment sIndex
       and set the deviation of the aSegment as 4 - miss aligned segment by 1 place
   ElseIf the first stop in sSegment matches the second stop in aSegment then we increment aIndex
       to hopefully align the segments and we add another deviation to aSegment 4 - miss aligned segment
   ElseIf the second stop in both aSegemt and sSegment match then we check:
           If the first stop of sSegment is not in aTrip then we add it to stopsMissed and add a deviation
               to aSegment of 3- scheduled stop missed
           If the first stopof aSegment is not in sTrip then we add it to nonscheudledStopsMade and
               add a devaition to aSegment of 2 - nonscheduled stop made
           regardless of the outcome of the two above if statements we now increment both sIndex and
           aIndex  and add information to the problem field of the trip.
       Note: I am not sure in what context the 3 above ElseIf situations occur so right now I am just 
           trying to align the sequences and record information about each instance when it happens, 
           once I look at the deviation report I can make adjustments to the code to better handle each case
   Else: neither of the stops in the aSegment match either of the sSegment stops so there are alot
           of potential cases
           First we see if the aSegment can be found at some later index in sTrip using the findMatch() 
           and we see if the sSegment can be found at a later index in aTrip using findMatch(), later 
           meaning some index past the current aIndex or sIndex. If a match is found it is placed in
           indexOne and indexTwo respectivly, if no match is found findMatch() returns -1.
           If neither of the segments can find a match then we use the findFirstStop() function four times 
               twice to look in the sTrip for a segment that begins with one of the stops from aSegment
               and to store the indexs in sIndexAStop0 and sIndexAStop1, the other two calls look in
               aTrip for a segment that begins with one of the stops from sSegment, storing the index in
               aIndexSStop0 and aIndexSStop1.
               If all the indexes returned were -1 then  we add the stops to nonscheduled stops made 
                   and stops missed and add the appropraite deviations and increment both aIndex and
                   sIndex
               Else one of the calls returned a valid index so we use getMin() to find out which one
                   of the indexes is  the closest to aIndex and sIndex  while not being -1. Then we
                   increment aIndex or sIndex depending on the value that getMin() returns 
                   Note: I chose the smallest jump index as i thought it would be better, but I have
                       not tested it yet to see if there is a better way to choose which index to go with
                   
                   ElseIf we found a match for the sTrip segment in the aTrip, but could not find the
                       aSegment in the sTrip we move the aTrip index to the match  our sSegment
                   ElseIf we found a match for the aTrip segment in the sTrip, but could not find the 
                       sSegment in the aTrip then we move the sTrip index to the match for our aSegment
                   Else in this case we found matches for both segments so we move the index of the Trip 
                       which is the smallest jump away from one of our current indexes aIndex or sIndex
                       If the match for the aSegment in the sTrip is less of a jump from sIndex then
                           the match for the sSegment in the aTrip then we set sIndex to be the index 
                           of the match of aSegment
                       Else the match for the sSegment in the aTrip is closer to aIndex so we set aIndex
                          equal to the index in aTrip that has a match for sSegment
                          
                    
#Inputs: actualDay-the actual day object, actualBlock- the actual block object, aTrip- the actual trip
#        object, sTrip- the scheduled trip object
#Returns: the function is void, it returns nothing it just updates the actualDay object

#This function works by looking at the actual and the scheduled versions of a trip, aTrip and sTrip
#side by side and comparing the aSegment it is looking at to the sSegment it is looking at by using
#two variables to keep track of the indexes of the two segment lists.
#           Note: python has a length function len() that returns the length of a list i.e the number of elements in it
#                 since indexes in list start at 0 they go until len()-1, which is why the while is < len(list)
#While the aIndex is less than the length of the aTrip segments list and the sIndex is less than the length of sTrip segments:
#   we get the aSegment at index aIndex of aTrip's segments
#   we get the sSegment at index sIndex of sTrip's segments
#   checkCases() is a helper function meant to deal with weird situations that come up, all it does 
#       now is deal with an instance where the same stop has a different number in the sTrip than it does in aTrip
#   If both stops in the aSegment match both stops in sSegment then we use updateSegment() to add the
#       segment distance and sequence number to the aSegment from the sSegment, then we increment both 
#       indexes to look at the next pair of segments.
#   ElseIf the the first stop of the aSegment matches the first stop of the sSegment then we check 
#       If the stop is not is the list of stop in sTip, in which case we mark it as a nonScheduledStop
#           mark the aSegment as having a type 2 deviation-nonScheduled stop, and we increment the 
#           aIndex to look at the next aSegment  ------------NOT SURE IF I SHOULD INCREMENT sIndex need to test
#       Else the stop is in sTrip so we use findSecondStop() to look in the sTrip segment list starting
#           at sIndex and try to find a segment whose second stop matches the second stop of aSegment
#           If we can't find the stop as a terminal stop i.e. when findSecondStop() returns -1 we try
#               to find it as the first stop of some sSegment using findFirstStop() 
#               If we can't find it as the inital stop of any of the remaining sSegments then we mark 
#                   the segment deviation as a 6 - potential loop on second stop since the stop is in 
#                   the sTrip, but it must have occured at some index < our current sIndex, we then 
#                   increment the aIndex
#               Else we found it as the initial stop of some sSegment, but not as the terminal stop
#                   of some sSegment so we move sIndex to that sSegment, we increment aIndex so that
#                   they match hopefully and mark the aSegment deviation as 7, found on inital stop
#                   but not on terminal stop NOTE: I don't see how this case could occur, but I put this hear to see if it does
#           Else we found the second stop of aSegment in sTrip and we now infer stops, we create a 
#               new segment1 that is the first stop of aSegment and the second stop of sSegment(this
#               will replace aSegment) then we create a segment2 that is the the segment that was found
#               by using findSecondStop(), but we update the second stop of the sSegment to include
#               the information from the aSegment second stop. Then we grab all segments in sTrip between
#               these two stops and mark them all as having a deviation of 1 - infered stop. We insert
#               them all into the aTrip segments, then adjust aIndex to point to the next segment after 
#               segment 2 and adjust sIndex to the next index after the one that was returned by findSecondStop()
#   ElseIf the first stop in aSegment matches the second stop in sSegment then we increment sIndex
#       and set the deviation of the aSegment as 4 - miss aligned segment by 1 place
#   ElseIf the first stop in sSegment matches the second stop in aSegment then we increment aIndex
#       to hopefully align the segments and we add another deviation to aSegment 4 - miss aligned segment
#   ElseIf the second stop in both aSegemt and sSegment match then we check:
#           If the first stop of sSegment is not in aTrip then we add it to stopsMissed and add a deviation
#               to aSegment of 3- scheduled stop missed
#           If the first stopof aSegment is not in sTrip then we add it to nonscheudledStopsMade and
#               add a devaition to aSegment of 2 - nonscheduled stop made
#           regardless of the outcome of the two above if statements we now increment both sIndex and
#           aIndex  and add information to the problem field of the trip.

#       Note: I am not sure in what context the 3 above ElseIf situations occur so right now I am just 
#           trying to align the sequences and record information about each instance when it happens, 
#           once I look at the deviation report I can make adjustments to the code to better handle each case
#   Else: neither of the stops in the aSegment match either of the sSegment stops so there are alot
#           of potential cases
#           First we see if the aSegment can be found at some later index in sTrip using the findMatch() 
#           and we see if the sSegment can be found at a later index in aTrip using findMatch(), later 
#           meaning some index past the current aIndex or sIndex. If a match is found it is placed in
#           indexOne and indexTwo respectivly, if no match is found findMatch() returns -1.
#           If neither of the segments can find a match then we use the findFirstStop() function four times 
#               twice to look in the sTrip for a segment that begins with one of the stops from aSegment
#               and to store the indexs in sIndexAStop0 and sIndexAStop1, the other two calls look in
#               aTrip for a segment that begins with one of the stops from sSegment, storing the index in
#               aIndexSStop0 and aIndexSStop1.
#               If all the indexes returned were -1 then  we add the stops to nonscheduled stops made 
#                   and stops missed and add the appropraite deviations and increment both aIndex and
#                   sIndex
#               Else one of the calls returned a valid index so we use getMin() to find out which one
#                   of the indexes is  the closest to aIndex and sIndex  while not being -1. Then we
#                   increment aIndex or sIndex depending on the value that getMin() returns 
#                   Note: I chose the smallest jump index as i thought it would be better, but I have
#                       not tested it yet to see if there is a better way to choose which index to go with
#                   
#                   ElseIf we found a match for the sTrip segment in the aTrip, but could not find the
#                       aSegment in the sTrip we move the aTrip index to the match  our sSegment
#                   ElseIf we found a match for the aTrip segment in the sTrip, but could not find the 
#                       sSegment in the aTrip then we move the sTrip index to the match for our aSegment
#                   Else in this case we found matches for both segments so we move the index of the Trip 
#                       which is the smallest jump away from one of our current indexes aIndex or sIndex
#                       If the match for the aSegment in the sTrip is less of a jump from sIndex then
#                           the match for the sSegment in the aTrip then we set sIndex to be the index 
#                           of the match of aSegment
#                       Else the match for the sSegment in the aTrip is closer to aIndex so we set aIndex
#                           equal to the index in aTrip that has a match for sSegment
def compareTrips(actualDay,actaulBlock, aTrip, sTrip):
