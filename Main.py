import urllib.parse
import urllib.request
import json


class MapQuest:
    def __init__(self, APIkey):
        self._APIkey = APIkey
        self._BASE_URL = 'http://open.mapquestapi.com'

    def urlBuild(self, locations):
        query_parameters = [('key',
                             self._APIkey)]  # This is a list of 2-element tuple(s) that will go into urllib.parse.urlencode function
        query_parameters.append(('from', locations[
            0]))  # Append the locations starting with a 'from' as the first index and the rest are 'to'.
        for location in locations[1:]:
            query_parameters.append(('to', location))  # Location is the second index
        URLBuild = self._BASE_URL + '/directions/v2/route?' + urllib.parse.urlencode(query_parameters)  # Making the URL
        response = urllib.request.urlopen(URLBuild)  # opens the URL
        return json.load(response)  # Loads up a JSON version of the URL

    def totalDistance(self, locations: list) -> float:
        if len(locations) == 0 or len(locations) == 1:
            return 0
        else:

            jsonLoad = MapQuest.urlBuild(self,
                                         locations)  # Calls the urlBuild function and assigns to jsonLoad variable
            return jsonLoad['route']['distance']  # Gets the distance. jsonLoad is a long dictionary.

    # Had to print jsonLoad to look for where the distance is. Can also look at MapQuest website for the JSON format to see where the distance is

    def totalTime(self, locations: list) -> int:
        if len(locations) == 0 or len(locations) == 1:
            return 0
        else:
            jsonLoad = MapQuest.urlBuild(self, locations)
            legs = jsonLoad['route']['legs']  # Used website to look for the times in the dictionary
            time = 0
            for leg in legs:
                time += leg['time']  # Added up all the times in each leg
            return time

    def directions(self, locations: list) -> str:
        if len(locations) == 0 or len(locations) == 1:
            return 0
        else:
            strDirections = ''
            jsonLoad = MapQuest.urlBuild(self, locations)
            legs = jsonLoad['route']['legs']
            for leg in legs:
                for manuever in leg['maneuvers']:  # Each leg has maneuver
                    strDirections += manuever['narrative'] + '\n'  # Maneuver has the directions in each narrative
        return strDirections

    def pointOfInterest(self, locations: str, keyword: str, results: int):
        query_parameters = [('key', self._APIkey), ('location', locations)]
        urlBaseLocation = 'http://www.mapquestapi.com/geocoding/v1/address?'  # Different BASE URL!
        urlLocation = urlBaseLocation + urllib.parse.urlencode(query_parameters)
        responseLocation = urllib.request.urlopen(urlLocation)
        jsonLocation = json.load(responseLocation)
        for result in jsonLocation[
            'results']:  # Basically looked for where the latitude and longitude are in this dictionary
            for location in result['locations']:
                Lat, Lng = (location['latLng'].values())

        POIparam = [('q', keyword), ('sort', 'distance'), ('pageSize', results),
                    ('key', self._APIkey)]  # required parameters
        POIURL = 'https://www.mapquestapi.com/search/v4/place?' + 'location=' + str(Lng) + ',' + str(
            Lat) + '&' + urllib.parse.urlencode(
            POIparam)  # Does not work if lat and lng are included in the POI parameters
        response = urllib.request.urlopen(POIURL)  # Had to manually put Lng and Lat into the URL for this to work
        jsonLoad = json.load(response)
        lst_result = []
        for result in jsonLoad['results']:
            lst_result.append(result['displayString'])  # This is all the results found from the json dictionary
        return lst_result  # Appended these to a list and returned the list
