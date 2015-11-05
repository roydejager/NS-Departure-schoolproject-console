__author__ = 'Roy'
import requests
import codecs
import xmltodict
import time


gekozenstation= ""

auth_details = ('username', 'password')

def schrijf_xml(bestandsnaam, response):
    bestand = codecs.open(bestandsnaam, "w", "utf-8")
    bestand.write(str(response.text))
    bestand.close()


def create_stationlist():
    bestand = open('stationslijst.xml', 'r')
    xml_string = bestand.read()
    return xmltodict.parse(xml_string)

def create_vertreklist():
    bestand = open('vertrektijden.xml', 'r')
    xml_string = bestand.read()
    return xmltodict.parse(xml_string)

def input_station():
        global gekozenstation
        station = input('Voer een station in:\n')
        if station in lijst_stations:
            gekozenstation  = station
            return vertrektijden_lijst(station)
        else:
            print ('Station bestaat niet\n')
            input_station()

def vertrektijden_lijst(station):
    url = 'http://webservices.ns.nl/ns-api-avt?station=' + station
    response = requests.get(url, auth = auth_details)
    schrijf_xml('vertrektijden.xml',response)
    return xmltodict.parse(response.text)



station_url = 'http://webservices.ns.nl/ns-api-stations-v2'
response = requests.get(station_url, auth = auth_details)
schrijf_xml('stationslijst.xml',response)
stations_dict = create_stationlist()

lijst_stations = []
for station_naam in stations_dict['Stations']['Station']:
    lijst_stations.append(station_naam['Namen']['Lang'])


vertrektijden_dict = input_station()

lijst_vertrek = []

def refresh():
    global vertrektijden_dict, gekozenstation
    print('{:20}{:30}{:30}{:30}'.format ('\nTijd:', 'Eindbestemming:', 'Treinsoort:','Vertrekspoor'))
    for vertrekken in vertrektijden_dict['ActueleVertrekTijden']['VertrekkendeTrein']:
        vertraging = ''
        if vertrekken['VertrekSpoor']['@wijziging'] == 'true':
            vertraging = 'Gewijzigd vertrekspoor'
        print('{:20}{:30}{:30}{:30}{:10}'.format(vertrekken['VertrekTijd'][11:19], vertrekken['EindBestemming'], vertrekken['TreinSoort'], vertrekken['VertrekSpoor']['#text'], vertraging))
    time.sleep(5)
    vertrektijden_dict = vertrektijden_lijst(gekozenstation)
try:
    while True:
        refresh()
except TypeError:
    print ('Station bestaat niet')
    input_station()
else:
    print ('Error')
    input_station()
