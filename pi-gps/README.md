# Query
I exported the coordinates with a query like below. Note that I grouped the coordinates by the average in each 10 sec interval to reduce the number of coordinates in the output.

> mysql -e "select avg(cast(lat as decimal(20, 15))) as lat, avg(cast(lng as decimal(20, 15))) as lng from gps_loc group by (substring(t_created, 1, 18))" -u pz -p exports > cooridnates.csv

Then I replaced blanks in the exported file with comma.


# Plug Onto Map
Then, I uploaded the exported coordinates onto `https://maps.co/gis/` in CSV format, and the website automatically plotted them on Google map (The website has a 500 coordinates limit).


# Reference
I followed [this guide](https://developer.here.com/blog/read-gps-data-with-a-raspberry-pi-zero-w-and-node.js?cid=Developer-Facebook_Comms-CM--Devblog-).