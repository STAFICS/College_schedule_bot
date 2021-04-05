from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from datetime import date
import json 

class GSheets():
	def __init__(self, course, group):
		self.SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
		self.SPREADSHEET_ID = '1ZBJrG8jyDRjknaT9_xiHavdVCA9KhUhj8-i3KumCakY'
		self.main_schedule_list = "'{} курс'".format(str(course))
		self.replacements_1_list = "'замены'!A:C"
		self.replacements_2_list = "'замены'!F:H"
		self.GROOP = group

		self.weeks = ['Пн','Вт','Ср','Чт','Пт', 'Сб', 'Вс']
		self.today = date.today().day
		self.tomonth = date.today().month
		self.toyeat = date.today().year
		self.toweek = date.today().weekday() + 1

		self.list_les = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']

	def init_gsheets(self):
	    store = file.Storage('token.json')
	    creds = store.get()
	    if not creds or creds.invalid:
	        flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
	        creds = tools.run_flow(flow, store)
	    service = build('sheets', 'v4', http=creds.authorize(Http()))
	    sheet = service.spreadsheets()
	    return sheet

	def write_sheet(self, file, name):
		with open(name, 'w', encoding='utf-8') as f:
			json.dump(file, f, indent = 1, ensure_ascii = False)

	def read_sheet(self):
		pass

	def get_sheets(self):
		raw_main_schedule_row = self.init_gsheets().values().get(spreadsheetId=self.SPREADSHEET_ID,range=self.main_schedule_list, majorDimension='ROWS').execute().get('values', [])
		raw_main_schedule_col = self.init_gsheets().values().get(spreadsheetId=self.SPREADSHEET_ID,range=self.main_schedule_list, majorDimension='COLUMNS').execute().get('values', [])
		raw_replacements_1 = self.init_gsheets().values().get(spreadsheetId=self.SPREADSHEET_ID,range=self.replacements_1_list).execute().get('values', [])
		raw_replacements_2 = self.init_gsheets().values().get(spreadsheetId=self.SPREADSHEET_ID,range=self.replacements_2_list).execute().get('values', [])

		self.write_sheet(raw_main_schedule_row, 'raw_main_schedule_row.json')
		self.write_sheet(raw_main_schedule_col, 'raw_main_schedule_col.json')
		self.write_sheet(raw_replacements_1, 'raw_replacements_1.json')
		self.write_sheet(raw_replacements_2, 'raw_replacements.json')

	def sort_main_schedule(self):
		pass		

GSheets(2, 'ЭПУ-21').get_sheets()

# print(a[0])
# print(b[1])
