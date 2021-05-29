import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import datetime
import clx.xms
from apscheduler.schedulers.background import BackgroundScheduler
from userdb.models import User_Data

fromaddr = ""
people= [

    # {
    #                     'state':'karnataka',
    #                     'age':'45',
    #                     'district':'davanagere',
    #                     'available_capacity':'_dose2',
    #                     'toaddr':"sourabhraobharadwaj@gmail.com"
    #
# }
]

def check_and_send_mail(state='karnataka',
                        age='45',
                        district='davanagere',
                        available_capacity='_dose2',
                        toaddr ="sourabhraobharadwaj@gmail.com",
                        user_id=0,
                        quantity=1):
    import json
    client = clx.xms.Client(service_plan_id='###PLANID', token='###TOKEN')
    create = clx.xms.api.MtBatchTextSmsCreate()
    create.sender = '#SENDER NUMBER'
    create.recipients = {'#RECIEVERNUMBER'}

    get_district_url = 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/'
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"

    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' }

    states = '{"states":[{"state_id":1,"state_name":"Andaman and Nicobar Islands"},{"state_id":2,"state_name":"Andhra Pradesh"},{"state_id":3,"state_name":"Arunachal Pradesh"},{"state_id":4,"state_name":"Assam"},{"state_id":5,"state_name":"Bihar"},{"state_id":6,"state_name":"Chandigarh"},{"state_id":7,"state_name":"Chhattisgarh"},{"state_id":8,"state_name":"Dadra and Nagar Haveli"},{"state_id":37,"state_name":"Daman and Diu"},{"state_id":9,"state_name":"Delhi"},{"state_id":10,"state_name":"Goa"},{"state_id":11,"state_name":"Gujarat"},{"state_id":12,"state_name":"Haryana"},{"state_id":13,"state_name":"Himachal Pradesh"},{"state_id":14,"state_name":"Jammu and Kashmir"},{"state_id":15,"state_name":"Jharkhand"},{"state_id":16,"state_name":"Karnataka"},{"state_id":17,"state_name":"Kerala"},{"state_id":18,"state_name":"Ladakh"},{"state_id":19,"state_name":"Lakshadweep"},{"state_id":20,"state_name":"Madhya Pradesh"},{"state_id":21,"state_name":"Maharashtra"},{"state_id":22,"state_name":"Manipur"},{"state_id":23,"state_name":"Meghalaya"},{"state_id":24,"state_name":"Mizoram"},{"state_id":25,"state_name":"Nagaland"},{"state_id":26,"state_name":"Odisha"},{"state_id":27,"state_name":"Puducherry"},{"state_id":28,"state_name":"Punjab"},{"state_id":29,"state_name":"Rajasthan"},{"state_id":30,"state_name":"Sikkim"},{"state_id":31,"state_name":"Tamil Nadu"},{"state_id":32,"state_name":"Telangana"},{"state_id":33,"state_name":"Tripura"},{"state_id":34,"state_name":"Uttar Pradesh"},{"state_id":35,"state_name":"Uttarakhand"},{"state_id":36,"state_name":"West Bengal"}],"ttl":24}'
    states_json = json.loads(states)

    district_id = 0
    state_id = 0
    availability = []

    for i in range(len(states_json['states'])):
        if (states_json['states'][i]['state_name'].lower() == state.lower()):
            state_id = (states_json['states'][i]['state_id'])

    district_response = requests.get(get_district_url + str(state_id), headers=header)
    district_json = district_response.json()

    for i in range(len(district_json['districts'])):
        if (district_json['districts'][i]['district_name'].lower() == district.lower()):
            district_id = district_json['districts'][i]['district_id']

    today = datetime.date.today()
    dd = today.strftime("%d-%m-%Y")

    response = requests.get(url, params={'district_id': str(district_id), 'date': str(dd)}, headers=header)
    json = response.json()
    for i in range(len(json['centers'])):
        for j in range(len(json['centers'][i]['sessions'])):
            if (json['centers'][i]['sessions'][j]['available_capacity' + available_capacity] > 0 and
                    json['centers'][i]['sessions'][j]['min_age_limit'] <= int(age)):
                print(json['centers'][i]['sessions'][j])
                availability.append(json['centers'][i]['sessions'][j]);

    if (len(availability) > 0):
        # //Sending mail

        msg = MIMEMultipart()
        # storing the senders email address
        msg['From'] = fromaddr
        # storing the receivers email address
        msg['To'] = toaddr
        # storing the subject

        msg['Subject'] = availability[0]['vaccine'] + " Vaccine is Available, Book your slot right now "
        # string to store the body of the mail

        slots_info = ''
        for i in availability:
            availability_json = i
            slots_info += 'Vaccine : ' + availability_json['vaccine'] + '\n' \
                                                                        'Date : ' + availability_json['date'] + '\n' \
                                                                                                                'Age Limit : ' + str(
                availability_json['min_age_limit']) + '\n' \
                                                      'Slots : ' + str(availability_json['slots']) + '\n' \
                                                                                                     'Available Dose1 : ' + str(
                availability_json['available_capacity_dose1']) + '\n' \
                                                                 'Available Dose2 : ' + str(
                availability_json['available_capacity_dose2']) + '\n\n\n'

        body = "Here is some Available Slots Information :\n\n" + slots_info
        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))
        # Converts the Multipart msg into a string
        text = msg.as_string()

        s = smtplib.SMTP('smtp.gmail.com', 587)

        # start TLS for security
        s.starttls()

        # Authentication
        s.login(fromaddr, "")

        s.sendmail(fromaddr, toaddr, text)

        s.quit()

        User_Data.objects.filter(user_id=user_id).update(quantity=quantity-1)

        #####################    Sending to mobile phone
    # try:
    #     create.body = "Book your slot for Vaccine";
    #     batch = client.create_batch(create)
    # except (requests.exceptions.RequestException, clx.xms.exceptions.ApiException) as ex:
    #     print('Failed to communicate with XMS: %s' % str(ex))



def check_for_all():
    people = User_Data.objects.all()
    for j in people:
        if(j.quantity):
            check_and_send_mail(j.state, j.age , j.district, j.available_capacity, j.toaddr ,j.user_id , j.quantity)

def schedule_Notifier():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_for_all , 'interval', seconds=10)
    scheduler.start()
    # while(1):
    #     pass
