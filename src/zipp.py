import geopy.distance

# parses data provided parse_zipcensus and adds distance from
# given zip code. The miles parameter is max amount of miles
# that will be kept and the rest will be dumped out of memory
def generate_distance_data(data, zipcode, miles=150):
    # search for zip in the zip data set and extract the lat long
    # which will be put into home_data
    home_data = None
    for line in data:
        if line["zipcode"] == str(zipcode):
            home_data = line
            break
 
    home_cords = (home_data["lat"], home_data["long"])

    # copy of data but with the distance from home added
    data_dist = []

    # iterate over the data set and add the distance
    # of our home to all the zipcode objects in memory
    for d in data:
        d_cords = (d["lat"], d["long"])
        d["dist"] = geopy.distance.geodesic(
            home_cords,
            d_cords
        ).miles
        data_dist.append(d)

    # sorts all the data by distance
    sorted_data = sorted(data_dist, key=lambda d: d["dist"])

    # only return data within the given miles parameter
    closest_data = []
    for i in sorted_data:
        if i["dist"] < miles:
            closest_data.append(i)
        else:
            break

    return closest_data