from openpyxl import load_workbook
from datetime import datetime


def readexcel(file):
    wb = load_workbook(file)
    # Loads the file uploaded by the user
    name = wb.get_sheet_names()
    # Gets all the names of the different sheets in the file
    groups = name_valid_groups(name)
    # Checks for valid names
    sheet = wb.get_sheet_by_name(groups.pop(0))
    # Gets the sheet from the first valid group,
    # needs to be called each time a new group should be added
    return sheet


def name_valid_groups(listofnames):
    i = 0
    groups = []
    # Checks if there is a sheet that is named:
    #  P1, P2, P3 etc. or Pulje 1, Pulje 2 etc.
    # All other sheets will be discarded, possible to add more options below
    while i < len(listofnames):
        if listofnames[i] == 'P'+str(i+1) or listofnames[i] == ('Pulje ' + str(i+1)):
            groups.append(listofnames[i])
            i += 1
        else:
            return groups


def read_competition_details(sheet):
    competition_details = []
    competition_category = sheet['C5'].value
    host_club = sheet['H5'].value
    place = sheet['M5'].value
    date = sheet['R5'].value.date()
    group_number = sheet['T5'].value
    competition_details.extend((competition_category, host_club, place, date, group_number))
    return competition_details


def read_competition_staff(sheet):
    competition_staff = []
    competition_leader = sheet['C27'].value
    jury1 = sheet['C29'].value
    jury2 = sheet['C30'].value
    jury3 = sheet['C31'].value
    secretary = sheet['C34'].value
    secretary2 = sheet['C35'].value
    speaker = sheet['C36'].value
    judge1 = sheet['I27'].value
    judge2 = sheet['I28'].value
    judge3 = sheet['I29'].value
    extra_judge = sheet['I30'].value
    technical_inspector = sheet['H32'].value
    chief_marshall = sheet['H33'].value
    timekeeper = sheet['H34'].value
    competition_staff.extend((competition_leader, jury1, jury2, jury3, secretary, secretary2, speaker, judge1, judge2,
                              judge3, extra_judge, technical_inspector, chief_marshall, timekeeper))
    return competition_staff


def read_lifters(sheet):
    lifters = []
    for row in range(9, 24):  # Here you can add or reduce the rows
        for column in "ABCDFGHIJKLM":  # Here you can add or reduce the columns
            cell_name = "{}{}".format(column, row)
            if isinstance(sheet[cell_name].value, datetime):  # Change the dates to correct type of date
                lifters.append(sheet[cell_name].value.date())
            elif sheet[cell_name].value is not None:  # Checks if there is data in a cell
                lifters.append(sheet[cell_name].value)
    return lifters


def read_competition_details_5kamp(sheet):
    competition_details = []
    competition_category = sheet['C5'].value
    host_club = sheet['J5'].value
    place = sheet['P5'].value
    date = sheet['U5'].value.date()
    group_number = sheet['X5'].value
    competition_details.extend((competition_category, host_club, place, date, group_number))


def read_competition_staff_5kamp(sheet):
    competition_staff = []
    competition_leader = sheet['C34'].value
    jury1 = sheet['C36'].value
    jury2 = sheet['C37'].value
    jury3 = sheet['C38'].value
    secretary = sheet['C40'].value
    secretary2 = sheet['C41'].value
    speaker = sheet['C42'].value
    judge1 = sheet['K34'].value
    judge2 = sheet['K35'].value
    judge3 = sheet['K36'].value
    extra_judge = sheet['K37'].value
    technical_inspector = sheet['K38'].value
    chief_marshall = sheet['K39'].value
    timekeeper = sheet['K40'].value
    competition_staff.extend((competition_leader, jury1, jury2, jury3, secretary, secretary2, speaker, judge1, judge2,
                              judge3, extra_judge, technical_inspector, chief_marshall, timekeeper))
    return competition_staff


def read_lifters_5kamp(sheet):
    lifters = []
    for row in range(9, 32):  # Here you can add or reduce the rows
        for column in "ABCDEGHIJKLM":  # Here you can add or reduce the columns
            cell_name = "{}{}".format(column, row)
            if isinstance(sheet[cell_name].value, datetime):
                lifters.append(sheet[cell_name].value.date())  # Change the dates to correct type of date
            elif sheet[cell_name].value is not None:  # Checks if there is data in a cell
                lifters.append(sheet[cell_name].value)
    return lifters


data = readexcel('testfil.xlsx')
print(read_lifters(data))
