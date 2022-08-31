# fmdv
# Helps find all the nearest appointments available for the
# Texas DMV. Solves the issue of not being able to search for
# greater area to find quicker appointments that are 
# available outside of the 4 locations near the zipcode you 
# put in the site.
#
# To use change your zipcode and miles you want in the
# program entry.
#
# auth : Trenton Stiles

import dmvttp
import zipp
import sorter
import json

if __name__ == "__main__":
    # gets all available appointment times in the state of TX
    data = dmvttp.get_all_appointments(cache=True)
    # get the distance from our zipcode to all the appointments
    data = zipp.generate_distance_data(data, "75074", miles=50)
    # sort the data by earliest date and distance, removes dupes
    data = sorter.sort_data(data)

    save_file = open("appointments.json", "w")
    save_file.write(json.dumps(data))
    save_file.close()



        