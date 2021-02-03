#!/bin/bash
#Path to the ubertooth-scan program
SCAN_PROGRAM="/usr/bin/ubertooth-scan"

#Any arguments we should pass to the scan program
#A reliable scan needs at least 20 seconds of runtime to ID active devices
#Anything shorter and you may not get consistent identification.
#Note that devices not actively transmitting data or transmitting very
#little data may not be identifiable.
#If you have multiple ubertooth devices attached to your system you may need to
#add the -U flag to specify which device to user for scans.
SCAN_ARGS="-t 20"

#Path to the ubertooth-util program. We use this to get the microcontroller
#serial number of the ubertooth, which is the closest thing to a UUID for
#ubertooth devices in this context.
UTIL_PROGRAM="/usr/bin/ubertooth-util"

#Arguments passed to the ubertooth-utli program. Should only need -s to get
#microcontroller serial #
UTIL_ARGS="-s"

#Path to SED or other string editing program
SED_PROG="/usr/bin/sed"

#Path to nc or ncat which are used to send scan results to middleware
NC_PROG="/usr/bin/nc"

#Arguments to pass to nc or ncat. Provided arguments specify that we're using a
#UNIX Socket, and tell nc to quit after sending its initial data instead of
#persisting. Arguments can be added or modified by editing the below line if
#needed.
NC_ARGS="-N -U"

#UNIX Socket where we should send scan results to using nc
DATA_SOCKET="/run/bt-surveillance/processing.sock"

#ubertooth-scan dumps a lot of unneeeded info before reporting results.
#We need to know what the header (line before results) looks like
#So we can strip out earlier lines
SED_HEADER_STRIP_ARGS="0,/Scan results:/d"

#ubertooth-scan outputs other scan results data than just MAC address and name
#We need a regex pattern to strip out this data so we can just parse the MAC
#and name (if name provided)
SED_RESULTS_FILTER_REGEX="/AFH.*/d"

#Regex to match MACs returned by ubertooth-scan
MAC_REGEX='((\?|[A-F]|[0-9]){2}\:){5}(\?|[A-F]|[0-9]){2}'

#Regex to match device name returned by ubertooth-scan (if any)
#This really just matches on what precedes the name than the name itself
NAME_REGEX='\s{1}'

#Regex to match lines missing a closing quote (any line with name key)
NAME_LINE_REGEX='^.*[^"]$'

#Get the Serial # of the ubertooth device for later use in results
SERIAL_NUMBER="$($UTIL_PROGRAM $UTIL_ARGS)"
SERIAL_NUMBER=$($SED_PROG -E "s/Serial No: //" <<< $SERIAL_NUMBER)

#Capture Raw output from the ubertooth 
SCAN_RESULTS="$($SCAN_PROGRAM $SCAN_ARGS)"

#Strip output to just results section
SCAN_RESULTS=$($SED_PROG "$SED_HEADER_STRIP_ARGS" <<< "$SCAN_RESULTS")

#Remove the parts of the scan results we don't care about
SCAN_RESULTS=$($SED_PROG "$SED_RESULTS_FILTER_REGEX" <<< "$SCAN_RESULTS")

#Python makes data processing really easy when stuff is in JSON format.
#Let's try to make the output JSON formatted.
#1. Append {"mac": to begining of line and enclose the MAC address in quotes
SCAN_RESULTS=$($SED_PROG -E "s/$MAC_REGEX/{\"mac\":\"&\"/" <<< "$SCAN_RESULTS")
#2. Replace the space/tab b/w the MAC and name with "name":"
SCAN_RESULTS=$($SED_PROG -E "s/$NAME_REGEX/,\"name\":\"/" <<< "$SCAN_RESULTS")
#3. Finish enclosing the name in quotes
SCAN_RESULTS=$($SED_PROG -E "s/$NAME_LINE_REGEX/&\"/" <<< "$SCAN_RESULTS")
#4. Close out each line with the closing }
SCAN_RESULTS=$($SED_PROG -E 's/$/}/' <<< "$SCAN_RESULTS")
#5. Add commas to all the lines except the last one.
SCAN_RESULTS=$($SED_PROG -E '$!s/$/,/' <<< "$SCAN_RESULTS")
#6. Remove the linebreaks.
SCAN_RESULTS=$(tr -d '\n' <<< "$SCAN_RESULTS")
#7. Enclose Results in brackets
SCAN_RESULTS=$($SED_PROG -E "s/.*/[&]/" <<< "$SCAN_RESULTS")

#Combine the ubertooth serial number with the scan results to form the report
#string we send to the data socket.
REPORT="{\"ubertooth_serial_number\":\"$SERIAL_NUMBER\",\"scan_results\":$SCAN_RESULTS}"

#Print the cleaned up scan results and forward them to middleware using nc
echo "$REPORT" | python3 -mjson.tool
echo "$REPORT" | $NC_PROG $NC_ARGS $DATA_SOCKET
