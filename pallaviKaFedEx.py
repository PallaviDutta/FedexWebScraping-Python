import requests
import json
from datetime import date as dt
import calendar as cl



tracking_number = '744668909687'

data = requests.post('https://www.fedex.com/trackingCal/track', data={
    'data': json.dumps({
        'TrackPackagesRequest': {
            'appType': 'wtrk',
            'uniqueKey': '',
            'processingParameters': {
                'anonymousTransaction': True,
                'clientId': 'WTRK',
                'returnDetailedErrors': True,
                'returnLocalizedDateTime': False
            },
            'trackingInfoList': [{
                'trackNumberInfo': {
                    'trackingNumber': tracking_number,
                    'trackingQualifier': '',
                    'trackingCarrier': ''
                }
            }]
        }
    }),
    'action': 'trackpackages',
    'locale': 'en_US',
    'format': 'json',
    'version': 99
}).json()

def get_day(date, month, year):
    d, m, y = int(date), int(month), int(year)
    tempDate = dt(y, m, d)
    dayName = cl.day_name[tempDate.weekday()]
    return dayName[:3]


packageDetail = data["TrackPackagesResponse"]["packageList"][0]
mainData = packageDetail["statusWithDetails"]
rawShipDate = packageDetail["displayTenderedDt"].split('/')
dayNameShipment = get_day(rawShipDate[1], rawShipDate[0], rawShipDate[2])
desiredShipDate = rawShipDate[1] + '/' + rawShipDate[0] + '/' + rawShipDate[2]

mainDataSplit = mainData.split(':')
status = mainDataSplit[0]
rawDeliveryDate = mainDataSplit[1][1:10].split('/')
dayNameDelivery = get_day(rawDeliveryDate[1], rawDeliveryDate[0], rawDeliveryDate[2])
deliveryDate = rawDeliveryDate[1] + '/' + rawDeliveryDate[0] + '/' + rawDeliveryDate[2]

time = mainDataSplit[1][-1] + ':' + mainDataSplit[2][:6]

output = '{\n"tracking no"' + ': ' + tracking_number + ',\n"ship date"'+ ':  "'+ dayNameShipment + ' ' + desiredShipDate + '",\n"status" ' + ':  "'+ status + '",\n"schedule delivery" '+ ': "' + dayNameDelivery + ' ' + deliveryDate + ' ' + time + '"\n}'

print(output)