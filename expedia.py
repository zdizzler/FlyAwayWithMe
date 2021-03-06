import datetime
from dateutil import parser
import requests
import json
import heapq
def comparator(a, b):
    if (float(a['FlightPriceSummary']['TotalPrice']) > float(b['FlightPriceSummary']['TotalPrice'])) :
        return 1;
    if (float(a['FlightPriceSummary']['TotalPrice']) < float(b['FlightPriceSummary']['TotalPrice'])):
        return -1;
    else:
        return 0;
def getFlightInfo(depAirPort):
    url = 'http://terminal2.expedia.com:80/x/flights/overview/get'

    header = {'Authorization': 'expedia-apikey key=OzVFoq2hbfr0ZDroP9yuPeZsEHapjptr',
            'Content-Type': 'application/json', 'Accept': 'application/json'}

    end = datetime.date(2016,11,1)
    date_list = [end - datetime.timedelta(days=x) for x in range(0, 30)]

    minPrice = 100000
    flightInfo = {}

    for date in date_list:
        payload = {
            'MessageHeader': 
            {'ClientInfo':
                {'DirectClientName': 'Hackathon'},
                'TransactionGUID': ''},
                'tpid': 1,
                'eapid': 0,
                'PointOfSaleKey':
                {'JurisdictionCountryCode': 'USA',
                    'CompanyCode': '10111',
                    'ManagementUnitCode': '1010'},
                'OriginAirportCodeList': 
                {'AirportCode': [depAirPort]},
                'DestinationAirportCodeList': 
                {'AirportCode': ['ATL','ORD','LAX','DFW','DEN','JFK','SFO','LAS','PHX','IAH','CLT','MIA','MCO','EWR','SEA','MSP','DTW','PHL','BOS','LGA','FLL','BWI','IAD','SLC','MDW','DCA','HNL','SAN','TPA','PDX','STL','MCI','HOU','BNA','MKE','OAK','RDU','AUS','CLE','SMF','MEM','MSY','SNA','SJC','PIT','SAT','DAL','RSW','IND','CVG']},
                'FareCalendar': {
                    "StartDate" : date.isoformat(),
                    "DayCount" : 30 }
        }
        r = requests.post(url, data=json.dumps(payload), headers=header)
        data = json.loads(r.text)

        orderedOffers = data['FareCalendar']['AirOfferSummary']

    offersWithRemovedSameDates = []
    for offer in orderedOffers:
        if parser.parse(offer['FlightItinerarySummary']['OutboundDepartureTime']).date() != parser.parse(offer['FlightItinerarySummary']['InboundDepartureTime']).date():
            offersWithRemovedSameDates.append(offer);

    offersWithRemovedSameDates.sort(comparator)

    formattedOrderedOffers = []

    for offer in offersWithRemovedSameDates:
        home = offer['FlightItinerarySummary']['OutboundDepartureAirportCode']
        visit = offer['FlightItinerarySummary']['InboundDepartureAirportCode']
        outDate = offer['FlightItinerarySummary']['OutboundDepartureTime']
        inDate = offer['FlightItinerarySummary']['InboundDepartureTime']
        outAirLine = offer['FlightItinerarySummary']['OutboundDepartureAirlineCode']
        inAirLine = offer['FlightItinerarySummary']['InboundDepartureAirlineCode']
        price = offer['FlightPriceSummary']['TotalPrice']

        flightInfo = {'home':home,'visit':visit,'outDate':outDate,'inDate':inDate,
                'minPrice':price,'outAirLine':outAirLine,'inAirLine':inAirLine}

        formattedOrderedOffers.append(flightInfo)

        outDate = outDate.split('T')[0]
        outDate = outDate.split("-")[1] + "/" + outDate.split("-")[2] + "/" +  outDate.split("-")[0]
        inDate = inDate.split('T')[0]
        inDate = inDate.split("-")[1] + "/" + inDate.split("-")[2] + "/" +  inDate.split("-")[0]

        #Make link that doesn't show the flight....
        link = 'https://www.expedia.com/Flights-Search?trip=roundtrip&leg1=from:'
        link += home + ',to:' + visit + ',departure:' + outDate + 'TANYT&leg2=from:' 
        link += visit + ',to:' + home + ',departure:' + inDate + 'TANYT&passengers=children:0,adults:'
        link += '1,seniors:0,infantinlap:Y&mode=search'



    return formattedOrderedOffers
