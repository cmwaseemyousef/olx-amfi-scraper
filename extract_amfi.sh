#!/bin/bash
curl -s https://www.amfiindia.com/spages/NAVAll.txt | \
awk -F ';' 'BEGIN {OFS="\t"; print "Scheme Name", "Asset Value"} 
$4 && $6 && $4 != "Scheme Name" {print $4, $6}' > nav_data.tsv
