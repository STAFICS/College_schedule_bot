from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import date as vrema
from time import sleep

# ############################

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

SAMPLE_SPREADSHEET_ID = '1ZBJrG8jyDRjknaT9_xiHavdVCA9KhUhj8-i3KumCakY'
main_schedule = "'2 курс'!BC:BC"
other_schedule_1 = "'замены'!A:C"
other_schedule_2 = "'замены'!F:H"
GROOP = 'ЭПУ-21'
weeks = ['Пн','Вт','Ср','Чт','Пт']

def pars():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    sheet = service.spreadsheets()

    result_1 = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=main_schedule).execute()
    values_1 = result_1.get('values', [])

    result_2 = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=other_schedule_1).execute()
    values_2 = result_2.get('values', [])

    result_3 = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=other_schedule_2).execute()
    values_3 = result_3.get('values', [])

    if not values_1:
        return 'No data found.'
    else:
        return values_1, values_2, values_3

def sort_main_data(data):
    off_data = data
    on_data = []
    dop_data = []
    for x in range(1,32):
        dop_data.append(off_data[x])
        if x % 6 == 0:
            on_data.append(dop_data)
            dop_data = []
    return on_data

def sort_other_data(data):
    a = []
    for x in range(2, len(data)):
        if data[x][1] == GROOP:
            a.append(data[x])
    return a

# continue
def ready_raspis(main_data):
    weekday = vrema.today().weekday() + 1
    date = str(vrema.today().day + 1) + '.' + str(vrema.today().month) + '.' + str(vrema.today().year)
    ready_text = 'Расписание на ' + str(date) + '(' + weeks[weekday] + '):\n'
    for x in range(5):
        if x == weekday:
            for y in range(6):
                if main_data[x][y] == []:
                    continue
                else:
                    ready_text += ' ' + str(y+1) + '. ' +str(main_data[x][y][0]) + '\n'
        else:
            continue
    return ready_text

def write_other_data(data, name):
    import json
    list(data)
    file = open(name, 'w')
    file.write(json.dumps(data))
    file.close()

def read_other_data(name):
    import json
    with open(name) as f:
        data = json.loads(f.read())
    return data

def pars_data(main_data, other_data_1, other_data_2):
    ready_text = ''
    date = str(vrema.today().day) + '.' + str(vrema.today().month) + '.' + str(vrema.today().year)
    ready_text = ready_raspis(main_data) + 'Замены: \n'
    if date != date_1:
        for x in range(len(sorted_other_1_data)):
            ready_text += ' ' + str(sorted_other_1_data[x][0] + ' ' + str(sorted_other_1_data[x][2]))
    elif date != date_2:
        for x in range(len(sorted_other_2_data)):
            ready_text += ' ' + str(sorted_other_2_data[x][0] + ' ' + str(sorted_other_2_data[x][2]))
    return ready_text

def init_vk():
    from vk_api import VkApi

    vk_token = '#########'

    vk_session = VkApi(token=vk_token)
    vk_session._auth_token()
    vk = vk_session.get_api()
    return vk
def vk_send_messages_group(message):
    vk = init_vk()

    followers = vk.groups.getMembers(group_id='polepu')
    for x in followers['items']:
        try:
            vk.messages.send(user_id = x, message = message)
        except:
            continue

def vk_send_messages_id(message):
    vk = init_vk()
    my_id = 60934883
    vk.messages.send(user_id = my_id, message = message)

def replacement_check(main_data, write_data, name):
    if main_data != write_data:
        write_other_data(main_data, name)
        vk_send_messages_group(pars_data(sorted_main_data, sorted_other_1_data, sorted_other_2_data))

unsorted_main_data, unsorted_other_data_1, unsorted_other_data_2 = pars()

sorted_main_data = sort_main_data(unsorted_main_data)
sorted_other_1_data = sort_other_data(unsorted_other_data_1)
sorted_other_2_data = sort_other_data(unsorted_other_data_2)
date_1 = unsorted_other_data_1[1][0].split(' ')[4]
date_2 = unsorted_other_data_2[1][0].split(' ')[4]

vk_send_messages_group('https://vk.com/polepu?w=wall-173784811_3')