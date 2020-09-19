#!/bin/bash
#Path to the ubertooth-scan program
SCAN_PROGRAM="/usr/bin/ubertooth-scan"

#Any arguments we should pass to the scan program
#A reliable scan needs at least 20 seconds of runtime to ID active devices
#Anything shorter and you may not get consistent identification.
#Note that devices not actively transmitting data or transmitting very
#little data may not be identifiable.
SCAN_ARGS="-t 20"

#Path to SED or other string editing program
SED_PROG="/usr/bin/sed"

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

#Capture Raw output from the ubertooth 
SCAN_RESULTS="$($SCAN_PROGRAM $SCAN_ARGS)"

#Strip output to just results section
SCAN_RESULTS=$($SED_PROG "$SED_HEADER_STRIP_ARGS" <<< "$SCAN_RESULTS")

#Remove the parts of the scan results we don't care about
SCAN_RESULTS=$($SED_PROG "$SED_RESULTS_FILTER_REGEX" <<< "$SCAN_RESULTS")

#Python makes data processing really easy when stuff is in JSON format.
#Let's try to make the output JSON formatted.
#1. Append {mac: to begining of line and enclose the MAC address in quotes
SCAN_RESULTS=$($SED_PROG -E "s/$MAC_REGEX/{mac:\"&\"/" <<< "$SCAN_RESULTS")
#2. Replace the space/tab b/w the MAC and name with name:"
SCAN_RESULTS=$($SED_PROG -E "s/$NAME_REGEX/,name:\"/" <<< "$SCAN_RESULTS")
#3. Finish enclosing the name in quotes
SCAN_RESULTS=$($SED_PROG -E "s/$NAME_LINE_REGEX/&\"/" <<< "$SCAN_RESULTS")
#4. Close out each line with the closing }
SCAN_RESULTS=$($SED_PROG -E 's/$/}/' <<< "$SCAN_RESULTS")
#5. Indent each line once (for pretty terminal printing)
SCAN_RESULTS=$($SED_PROG -E 's/^/\t/' <<< "$SCAN_RESULTS")
#6. Add commas to all the lines except the last one.
SCAN_RESULTS=$($SED_PROG -E '$!s/$/,/' <<< "$SCAN_RESULTS")
#7. Insert opening square bracket ([) before first line of content
SCAN_RESULTS=$($SED_PROG -E '1i\[' <<< "$SCAN_RESULTS")
#8. Add closing square bracket (]) after last line of content
SCAN_RESULTS=$($SED_PROG -E '$a]' <<< "$SCAN_RESULTS")

#Print the cleaned up scan results
echo "$SCAN_RESULTS"
