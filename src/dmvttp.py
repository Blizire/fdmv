import json
import requests

# headers I used when I inspected network traffic when searching for an
# appoint in my zipcode
def make_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json;charset=utf-8",
        "Origin": "https://www.txdpsscheduler.com",
        "Connection" : "keep-alive",
        "Referer": "https://www.txdpsscheduler.com/",
        "Sec-Fetch-Dest" : "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }

# fills the data field of the request for the zipcode being searched
def make_zipcode_data(zipcode):
    raw_data = '{"TypeId":"71", "ZipCode":"%s", "CityName":"", "PreferredDay":"0"}' % (zipcode)
    return json.loads(raw_data)

# actually executes the HTTP POST request and returns a requests object
def make_txdps_request(zipcode):
    url     = "https://publicapi.txdpsscheduler.com/api/AvailableLocation"
    headers = make_headers()
    data    = make_zipcode_data(zipcode)

    req = requests.post(
        url, 
        headers=headers, 
        data=json.dumps(data)
        )

    print("%s %s" % (str(zipcode), str(req.status_code)))

    return req

# run this as cached if youre going to run this script multiple times
# so you dont not flood the TXDMV with requests already
#
# gets every single appointment available in the state of texas lol c:
def get_all_appointments(cache=False):
    appointment_data = []

    if(not cache):
        # file source https://www.census.gov/geo/maps-data/data/gazetteer2014.html
        f = open("2014_Gaz_zcta_national.txt")    
        zipcode_pos_data = json.loads(f.read())
        
        for zips in zipcode_pos_data:
            req = make_txdps_request(int(zips["zip"]))
            for i in req.json():
                appointment_data.append({
                    "id": i["Id"],
                    "address": i["Address"],
                    "date": i["NextAvailableDate"],
                    "zipcode": zips["zip"],
                    "lat": zips["lat"],
                    "long": zips["long"]
                })
        cache_file = open("cache.txt", "w")
        cache_file.write(json.dumps(appointment_data))
        cache_file.close()
        f.close()
    else:
        # loads the file as json string and converts to py objects
        cache_file = open("cache.txt", "r")
        appointment_data = json.loads(cache_file.read())
        cache_file.close()
    return appointment_data