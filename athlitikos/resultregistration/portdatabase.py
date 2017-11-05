import jaydebeapi
import psycopg2
import datetime
# import pyodbc


def read_mdb():
    # You need to input the path to the UCanAccess Jars below
    ucanaccess_jars = [
        "/Users/ChristianRossow/Downloads/UCanAccess-4.0.2-bin/ucanaccess-4.0.2.jar",
        "/Users/ChristianRossow/Downloads/UCanAccess-4.0.2-bin/lib/commons-lang-2.6.jar",
        "/Users/ChristianRossow/Downloads/UCanAccess-4.0.2-bin/lib/commons-logging-1.1.1.jar",
        "/Users/ChristianRossow/Downloads/UCanAccess-4.0.2-bin/lib/hsqldb.jar",
        "/Users/ChristianRossow/Downloads/UCanAccess-4.0.2-bin/lib/jackcess-2.1.6.jar",
    ]
    classpath = ":".join(ucanaccess_jars)
    cnxn = jaydebeapi.connect(
        "net.ucanaccess.jdbc.UcanaccessDriver",
        # Input path below to the mdb file jdbc:ucanaccess://Pathtofile
        "jdbc:ucanaccess:///Users/ChristianRossow/Downloads/NVF Historiske resultater.mdb",
        ["", ""],
        classpath
    )
    curs = cnxn.cursor()

    # Use this for Windows
    # mdb_path = 'c:/path/to/my.mdb' # Path to the NVF Historiske resultater.mdb
    # driver = '{Microsoft Access Driver (*.mdb)}'
    # con = pyodbc.connect('DRIVER={};DBQ={};'.format(driver, mdb_path))
    # curs = con.cursor()

    return curs


def read_new_mdb():
    # You need to input the path to the UCanAccess Jars below
    ucanaccess_jars = [
        "/Users/ChristianRossow/Downloads/UCanAccess-4.0.2-bin/ucanaccess-4.0.2.jar",
        "/Users/ChristianRossow/Downloads/UCanAccess-4.0.2-bin/lib/commons-lang-2.6.jar",
        "/Users/ChristianRossow/Downloads/UCanAccess-4.0.2-bin/lib/commons-logging-1.1.1.jar",
        "/Users/ChristianRossow/Downloads/UCanAccess-4.0.2-bin/lib/hsqldb.jar",
        "/Users/ChristianRossow/Downloads/UCanAccess-4.0.2-bin/lib/jackcess-2.1.6.jar",
    ]
    classpath = ":".join(ucanaccess_jars)
    # Input path below to the mdb file jdbc:ucanaccess://Pathtofile
    cnxn = jaydebeapi.connect(
        "net.ucanaccess.jdbc.UcanaccessDriver",
        "jdbc:ucanaccess:///Users/ChristianRossow/Downloads/Resultater_.mdb",
        ["", ""],
        classpath
    )
    crsr = cnxn.cursor()

    # Use this for Windows
    # mdb_path = 'c:/path/to/my.mdb' # Path to the Resultater_.mdb
    # driver = '{Microsoft Access Driver (*.mdb)}'
    # con = pyodbc.connect('DRIVER={};DBQ={};'.format(driver, mdb_path))
    # crsr = con.cursor()

    return crsr


# Connect to the PostgreSQL database
def connect_postgre():
    try:
        conn = psycopg2.connect("dbname='athlitikos' user='postgres' host='localhost' password='postgre314'")
    except psycopg2.DatabaseError:
        print("I am unable to connect to the database")
    return conn


# Read all the clubs in both mdb files and store each unique club to the database
def clubs(crsr, conn, curs):
    cur = conn.cursor()
    crsr.execute('SELECT * FROM [Klubber]')
    club = crsr.fetchall()
    crsr.execute('SELECT Klubb FROM [Resultater]')
    more_clubs = crsr.fetchall()

    for club2 in more_clubs:
        if not club2[0]:
            pass
        elif club2 not in club:
            club.append(club2)

    curs.execute('SELECT KLUBB FROM [1938-1972 Oversikt - Resultater] '
                 'UNION ALL SELECT KLUBB FROM [1972-1985 Oversikt - Resultater] '
                 'UNION ALL SELECT KLUBB FROM [1986-1992 Oversikt - Resultater] '
                 'UNION ALL SELECT KLUBB FROM [1992-1997 Resultater]')
    old_clubs = curs.fetchall()

    for old_club in old_clubs:
        if not old_club[0]:
            pass
        elif old_club not in club:
            club.append(old_club)

    for row in club:
        sql = "INSERT INTO public.resultregistration_club (club_name) VALUES (%s);"
        cur.execute(sql, (row,))

    conn.commit()
    cur.close()


# Returns the club_id for a club in the database
def get_club_id(conn):
    cur = conn.cursor()
    cur.execute('SELECT id, club_name FROM public.resultregistration_club')
    rows = cur.fetchall()
    club_id = {}
    for row in rows:
        club_id[row[1]] = row[0]
    return club_id


# Very simple check if a name is valid
def valid_name(first, last):
    valid = True
    if len(first) < 2 or len(last) < 2:
        valid = False
    return valid


def old_1938_1972(curs, conn):
    cur = conn.cursor()
    curs.execute('SELECT * FROM [1938-1972 Oversikt - Resultater]')
    rows = curs.fetchall()
    club_dict = get_club_id(conn)
    person_id_dict = {}
    competition_id_dict = {}
    invalid_data = []
    # Reads in data from each row
    for row in rows:
        name = row[6]
        if name[-1:] == ' ':  # Fixes the problem where some names had whitespaces at the end
            first_name = row[6].rsplit(' ', 2)[0].lower().title()
            last_name = row[6].rsplit(' ', 2)[-2].lower().title()
        else:
            first_name = row[6].rsplit(' ', 1)[0].lower().title()
            last_name = row[6].rsplit(' ', 1)[-1].lower().title()
        club = row[7]
        club_id = club_dict.get(club)
        competition_category = row[0]
        host = row[1]
        start_date = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S').date()  # converts to correct date format
        weight_class = row[3]
        body_weight = row[4]
        age_group = row[5]
        best_press = row[8]
        best_snatch = row[9]
        best_clean_and_jerk = row[10]
        total_lift = row[11]
        points = row[12]

        # Checks if name is valid and that the lifter has a club
        if valid_name(first_name, last_name) and club_id is not None:
            if (first_name, last_name) in person_id_dict:  # Checks if person already exist and then get their ID
                person_id = person_id_dict[first_name, last_name]
            else:  # If not store the person in the database and put the ID in the person_id dictonary
                sql_person = "INSERT INTO public.resultregistration_person (first_name, last_name, club_id) " \
                             "VALUES (%s,%s,%s) RETURNING id;"
                cur.execute(sql_person, (first_name, last_name, club_id,))
                person_id = cur.fetchone()[0]
                person_id_dict[first_name, last_name] = person_id

            # Checks if competition already exist and then get the ID
            if (competition_category, host, start_date) in competition_id_dict:
                competition_id = competition_id_dict[competition_category, host, start_date]
            else:  # If not store the competition in the database and put the ID in the competition_id dictonary
                sql_competition = "INSERT INTO public.resultregistration_competition " \
                                  "(competition_category, host, start_date) VALUES (%s,%s,%s) RETURNING id;"
                cur.execute(sql_competition, (competition_category, host, start_date,))
                competition_id = cur.fetchone()[0]
                competition_id_dict[competition_category, host, start_date] = competition_id

            # Insert the result in the database
            sql_old_result = "INSERT INTO public.resultregistration_oldresults " \
                             "(weight_class, age_group, body_weight, best_press, best_snatch, " \
                             "best_clean_and_jerk, total_lift, points, competition_id, lifter_id, lifter_club_id) " \
                             "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            cur.execute(sql_old_result, (weight_class, age_group, body_weight, best_press, best_snatch,
                                         best_clean_and_jerk, total_lift, points, competition_id, person_id, club_id))
        else:
            invalid_data.append(row)

    print(invalid_data)  # Prints invalid data, so it is easy to see which data that are incorrect
    print(len(invalid_data))  # Number of invalid data rows
    conn.commit()
    cur.close()


def old_1972_1985(curs, conn):
    cur = conn.cursor()
    curs.execute('SELECT * FROM [1972-1985 Oversikt - Resultater]')
    rows = curs.fetchall()
    club_dict = get_club_id(conn)
    person_id_dict = {}
    competition_id_dict = {}
    invalid_data = []
    for row in rows:
        name = row[7]
        if name[-1:] == ' ':
            first_name = row[7].rsplit(' ', 2)[0].lower().title()
            last_name = row[7].rsplit(' ', 2)[-2].lower().title()
        else:
            first_name = row[7].rsplit(' ', 1)[0].lower().title()
            last_name = row[7].rsplit(' ', 1)[-1].lower().title()
        club = row[8]
        club_id = club_dict.get(club)
        competition_category = row[1]
        host = row[2]
        start_date = datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S').date()
        weight_class = row[4]
        body_weight = row[5]
        age_group = row[6]
        best_snatch = row[9]
        best_clean_and_jerk = row[10]
        total_lift = row[11]
        points = row[12]

        if valid_name(first_name, last_name) and club_id is not None:
            if (first_name, last_name) in person_id_dict:
                person_id = person_id_dict[first_name, last_name]
            else:
                sql_person = "INSERT INTO public.resultregistration_person (first_name, last_name, club_id) " \
                             "VALUES (%s,%s,%s) RETURNING id;"
                cur.execute(sql_person, (first_name, last_name, club_id,))
                person_id = cur.fetchone()[0]
                person_id_dict[first_name, last_name] = person_id

            if (competition_category, host, start_date) in competition_id_dict:
                competition_id = competition_id_dict[competition_category, host, start_date]
            else:
                sql_competition = "INSERT INTO public.resultregistration_competition " \
                                  "(competition_category, host, start_date) VALUES (%s,%s,%s) RETURNING id;"
                cur.execute(sql_competition, (competition_category, host, start_date,))
                competition_id = cur.fetchone()[0]
                competition_id_dict[competition_category, host, start_date] = competition_id

            sql_old_result = "INSERT INTO public.resultregistration_oldresults " \
                             "(weight_class, age_group, body_weight, best_snatch, " \
                             "best_clean_and_jerk, total_lift, points, competition_id, lifter_id, lifter_club_id) " \
                             "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            cur.execute(sql_old_result, (weight_class, age_group, body_weight, best_snatch, best_clean_and_jerk,
                                         total_lift, points, competition_id, person_id, club_id))
        else:
            invalid_data.append(row)

    print(invalid_data)
    print(len(invalid_data))
    conn.commit()
    cur.close()


def old_1986_1992(curs, conn):
    cur = conn.cursor()
    curs.execute('SELECT * FROM [1986-1992 Oversikt - Resultater]')
    rows = curs.fetchall()
    club_dict = get_club_id(conn)
    person_id_dict = {}
    competition_id_dict = {}
    invalid_data = []
    for row in rows:
        name = row[7]
        if name[-1:] == ' ':
            first_name = row[7].rsplit(' ', 2)[0].lower().title()
            last_name = row[7].rsplit(' ', 2)[-2].lower().title()
        else:
            first_name = row[7].rsplit(' ', 1)[0].lower().title()
            last_name = row[7].rsplit(' ', 1)[-1].lower().title()
        club = row[8]
        club_id = club_dict.get(club)
        competition_category = row[1]
        host = row[2]
        start_date = datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S').date()
        weight_class = row[4]
        body_weight = row[5]
        age_group = row[6]
        best_snatch = row[9]
        best_clean_and_jerk = row[10]
        total_lift = row[11]
        points = row[12]

        if valid_name(first_name, last_name) and club_id is not None:
            if (first_name, last_name) in person_id_dict:
                person_id = person_id_dict[first_name, last_name]
            else:
                sql_person = "INSERT INTO public.resultregistration_person (first_name, last_name, club_id) " \
                             "VALUES (%s,%s,%s) RETURNING id;"
                cur.execute(sql_person, (first_name, last_name, club_id,))
                person_id = cur.fetchone()[0]
                person_id_dict[first_name, last_name] = person_id

            if (competition_category, host, start_date) in competition_id_dict:
                competition_id = competition_id_dict[competition_category, host, start_date]
            else:
                sql_competition = "INSERT INTO public.resultregistration_competition " \
                                  "(competition_category, host, start_date) VALUES (%s,%s,%s) RETURNING id;"
                cur.execute(sql_competition, (competition_category, host, start_date,))
                competition_id = cur.fetchone()[0]
                competition_id_dict[competition_category, host, start_date] = competition_id

            sql_old_result = "INSERT INTO public.resultregistration_oldresults " \
                             "(weight_class, age_group, body_weight, best_snatch, " \
                             "best_clean_and_jerk, total_lift, points, competition_id, lifter_id, lifter_club_id) " \
                             "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            cur.execute(sql_old_result, (weight_class, age_group, body_weight, best_snatch, best_clean_and_jerk,
                                         total_lift, points, competition_id, person_id, club_id))
        else:
            invalid_data.append(row)

    print(invalid_data)
    print(len(invalid_data))
    conn.commit()
    cur.close()


def old_1992_1997(curs, conn):
    cur = conn.cursor()
    curs.execute('SELECT * FROM [1992-1997 Resultater]')
    rows = curs.fetchall()
    club_dict = get_club_id(conn)
    person_id_dict = {}
    competition_id_dict = {}
    invalid_data = []
    for row in rows:
        res_id = str(row[1])
        name = row[5]
        if name[-1:] == ' ':
            first_name = row[5].rsplit(' ', 2)[0].lower().title()
            last_name = row[5].rsplit(' ', 2)[-2].lower().title()
        else:
            first_name = row[5].rsplit(' ', 1)[0].lower().title()
            last_name = row[5].rsplit(' ', 1)[-1].lower().title()
        club = row[6]
        club_id = club_dict.get(club)

        # Here is the old database a bit different, therfore do we need to get competition details from a other table
        sql = "SELECT * FROM [1992-1997 Ovesikt] WHERE ID LIKE ? "
        curs.execute(sql, (res_id,))
        competition_row = curs.fetchone()

        competition_category = competition_row[1]
        host = competition_row[2]
        start_date = datetime.datetime.strptime(competition_row[3], '%Y-%m-%d %H:%M:%S').date()
        weight_class = row[2]
        body_weight = row[3]
        age_group = row[4]
        best_snatch = row[7]
        best_clean_and_jerk = row[8]
        total_lift = row[9]
        points = row[10]
        sinclair_coefficient = row[11]

        if valid_name(first_name, last_name) and club_id is not None:
            if (first_name, last_name) in person_id_dict:
                person_id = person_id_dict[first_name, last_name]
            else:
                sql_person = "INSERT INTO public.resultregistration_person (first_name, last_name, club_id) " \
                             "VALUES (%s,%s,%s) RETURNING id;"
                cur.execute(sql_person, (first_name, last_name, club_id,))
                person_id = cur.fetchone()[0]
                person_id_dict[first_name, last_name] = person_id

            if (competition_category, host, start_date) in competition_id_dict:
                competition_id = competition_id_dict[competition_category, host, start_date]
            else:
                sql_competition = "INSERT INTO public.resultregistration_competition " \
                                  "(competition_category, host, start_date) VALUES (%s,%s,%s) RETURNING id;"
                cur.execute(sql_competition, (competition_category, host, start_date,))
                competition_id = cur.fetchone()[0]
                competition_id_dict[competition_category, host, start_date] = competition_id

            sql_old_result = "INSERT INTO public.resultregistration_oldresults " \
                             "(weight_class, age_group, body_weight, best_snatch, best_clean_and_jerk, " \
                             "total_lift, points, sinclair_coefficient, competition_id, lifter_id, lifter_club_id) " \
                             "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            cur.execute(sql_old_result, (weight_class, age_group, body_weight, best_snatch, best_clean_and_jerk,
                                         total_lift, points, sinclair_coefficient, competition_id, person_id, club_id))
        else:
            invalid_data.append(row)

    print(invalid_data)
    print(len(invalid_data))
    conn.commit()
    cur.close()

# Be aware that this function takes in a other argument than the other functions,
# this is because the old data is stored in a other file


def old_1998_2017(crsr, conn):
    cur = conn.cursor()
    crsr.execute('SELECT * FROM [Resultater]')
    rows = crsr.fetchall()
    club_dict = get_club_id(conn)
    person_id_dict = {}
    competition_id_dict = {}
    invalid_data = []
    current_date = datetime.datetime.now().date()
    for row in rows:
        res_id = str(row[0])
        comp_id = str(row[1])
        name = row[5]
        if name[-1:] == ' ':
            first_name = row[5].rsplit(' ', 2)[0].lower().title()
            last_name = row[5].rsplit(' ', 2)[-2].lower().title()
        else:
            first_name = row[5].rsplit(' ', 1)[0].lower().title()
            last_name = row[5].rsplit(' ', 1)[-1].lower().title()
        club = row[6]
        club_id = club_dict.get(club)

        sql = "SELECT * FROM [Stevnedata] WHERE [Stevne-ID] LIKE ? "
        crsr.execute(sql, (comp_id,))
        competition_row = crsr.fetchone()
        if competition_row is not None:
            competition_category = competition_row[1]
            host = competition_row[2]
            location = competition_row[3]
            start_date = datetime.datetime.strptime(competition_row[4], '%Y-%m-%d %H:%M:%S').date()
        weight_class = row[2]
        body_weight = row[3]
        age_group = row[4]
        best_snatch = row[7]
        best_clean_and_jerk = row[8]
        total_lift = row[9]
        points = row[10]
        sinclair_coefficient = row[11]

        if valid_name(first_name, last_name) and club_id is not None and start_date <= current_date \
                and competition_row is not None:
            if (first_name, last_name) in person_id_dict:
                person_id = person_id_dict[first_name, last_name]
            else:
                sql_person = "INSERT INTO public.resultregistration_person (first_name, last_name, club_id) " \
                             "VALUES (%s,%s,%s) RETURNING id;"
                cur.execute(sql_person, (first_name, last_name, club_id,))
                person_id = cur.fetchone()[0]
                person_id_dict[first_name, last_name] = person_id

            if (competition_category, host, location, start_date) in competition_id_dict:
                competition_id = competition_id_dict[competition_category, host, location, start_date]
            else:
                sql_competition = "INSERT INTO public.resultregistration_competition " \
                                  "(competition_category, host, location, start_date) " \
                                  "VALUES (%s,%s,%s,%s) RETURNING id;"
                cur.execute(sql_competition, (competition_category, host, location, start_date,))
                competition_id = cur.fetchone()[0]
                competition_id_dict[competition_category, host, location, start_date] = competition_id

            sql_old_result = "INSERT INTO public.resultregistration_oldresults " \
                             "(weight_class, age_group, body_weight, best_snatch, best_clean_and_jerk, " \
                             "total_lift, points, sinclair_coefficient, competition_id, lifter_id, lifter_club_id) " \
                             "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"
            cur.execute(sql_old_result, (weight_class, age_group, body_weight, best_snatch, best_clean_and_jerk,
                                         total_lift, points, sinclair_coefficient, competition_id, person_id, club_id))
            result_id = cur.fetchone()[0]

            # Get pentathlon results and store them in the new database
            sql_pentathlon = "SELECT * FROM [Femkamp] WHERE [Resultat-ID] LIKE ? "
            crsr.execute(sql_pentathlon, (res_id,))
            pentathlon_row = crsr.fetchone()
            if pentathlon_row is not None:
                pentathlon_age_group = pentathlon_row[2]
                shot_put = pentathlon_row[3]
                shot_put_points = pentathlon_row[4]
                forty_meter = pentathlon_row[5]
                forty_meter_points = pentathlon_row[6]
                triple_jump = pentathlon_row[7]
                triple_jump_points = pentathlon_row[8]
                sum_all = pentathlon_row[9]
                sql_pentathlon_result = "INSERT INTO public.resultregistration_oldpentathlonresult " \
                                        "(age_group, shot_put, shot_put_points, forty_meter, forty_meter_points, " \
                                        "jump, jump_points, sum_all, competition_id, lifter_id, result_id) " \
                                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                cur.execute(sql_pentathlon_result, (pentathlon_age_group, shot_put, shot_put_points,
                                                    forty_meter, forty_meter_points, triple_jump, triple_jump_points,
                                                    sum_all, competition_id, person_id, result_id))

        else:
            invalid_data.append(row)

    print(invalid_data)
    print(len(invalid_data))
    conn.commit()
    cur.close()


# Run the clubs(new_cursor, connection, cursor) first, then the other functions can be called randomly,
# but I recommend to run them in the order set up below.

# new_cursor = read_new_mdb()
# connection = connect_postgre()
# cursor = read_mdb()
# clubs(new_cursor, connection, cursor)
# old_1938_1972(cursor, connection)
# old_1972_1985(cursor, connection)
# old_1986_1992(cursor, connection)
# old_1992_1997(cursor, connection)
# old_1998_2017(new_cursor, connection)


# Names not valid if it contains a ?, one letter or if it has for example a ')' in it
# Club for a lifter is the club which the lifter represented in the first competition.
# If the date is in the future the results are invalid
# The runtime is not very good, especially on the 1998-2017 porting (takes a few minutes to run)
