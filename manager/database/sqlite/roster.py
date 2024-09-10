from .init_db import SQL

table_name = "roster"
columns_table = ['roster_id', 'id_owner_roster', 'jid', 'name', 'subscription', 'created_at', 'updated_at']
type_of_columns = ['', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER']
foreign_key_column = ['id_owner_roster']
reference_table = ['user']
reference_column_of_table = ['user_id']

rosters = SQL(table_name, columns_table, type_of_columns, foreign_key_column,\
              reference_table, reference_column_of_table, db_name='manager.db')
# rosters = SQL(table_name, columns_table, type_of_columns, foreign_key_column,\
#               reference_table, reference_column_of_table, db_name='manager.sql')

# Ide 1 jadiin fungsi aja

def set_to_be_format(the_roster):
    res = []
    for roster in the_roster:
        res.append({
            "jid": roster[0],
            "name": roster[1],
            "subscription": roster[2]
        })
    return res

# Fungsionalitas untuk menyimpan atau mengubah roster item
def save_rosters(roster: list, timestamp):
    column = None
    roster.append(timestamp)
    roster.append(timestamp)
    print(f"PANJANG ROSTER: {len(roster)}")
    if(len(roster) == 5):
        column = ['id_owner_roster', 'jid', 'subscription', 'created_at', 'updated_at']
    elif(len(roster) == 6):
        column = ['id_owner_roster', 'jid', 'name', 'subscription', 'created_at', 'updated_at']
    print(f"COLUMN: {column}, {roster}")
    res = rosters.insert_to_table(column, roster)
    print(res)
    return res

# Fungsionalitas untuk mendapatkan all roster item dari user's roster, berdasarkan tipe subscriptionnya 'from'/'to' dan 'both'
def get_rosters_user(username, data_subscription_tuple):
    query = "SELECT jid, name, subscription FROM roster WHERE id_owner_roster=? AND (subscription=? OR subscription=?)"
    # data = (username, 'to', 'both')
    data = (username,) + data_subscription_tuple
    res = rosters.get_with_query(query, data)
    res = set_to_be_format(res)
    print(f"RES GR_DB: {res}")
    return res

# Fungsionalitas membaca database untuk data jid, name, dan subscriptionnya, berdasarkan kondisi id_owner_roster dan jid-nya.
def get_roster_user(username, jid_target):
    select_column = ["jid", 'name', 'subscription']
    columns_condition = ['id_owner_roster', 'jid']
    tuple_data_condition = (username, jid_target,)
    boolean_condition = ['AND']
    res = rosters.get_some_columns_with_limit(select_column, 1, columns_condition, tuple_data_condition, boolean_condition)
    res = set_to_be_format(res)
    if(res):
        return res[0]
    return res

def update_subscription(data_set_tuple, data_condition_tuple):
    columns_set = ['name', 'subscription']
    column_condition = ['id_owner_roster', 'jid']
    boolean_condition = ['AND']
    updating = rosters.update_data(columns_set, data_set_tuple, column_condition, data_condition_tuple, boolean_condition)
    print(f"UPDATING DATA ROSTER: {updating}")
    print(rosters.get_all())

def delete_roster_user(id_owner_roster, jid):
    columns_condition = ['id_owner_roster', 'jid']
    tuple_condition = (id_owner_roster, jid,)
    boolean_condition = ['AND']
    res = rosters.delete_data(columns_condition, tuple_condition, boolean_condition)
    print(res)
    print(f"ROSTER DB IN DELETE: {rosters.get_all()}")
    return res

# Ide 2 dijadiin kelas dengan inheritance SQL (SQLite)

class Roster(SQL):
    def __init__(self, table_name, columns_table, type_of_columns, \
                foreign_key_column = None, reference_table = None, \
                reference_column_of_table = None, db_name = None):
        super().__init__(table_name, columns_table, type_of_columns, \
                foreign_key_column, reference_table, \
                reference_column_of_table, db_name)
        
    def set_to_be_format(self, the_roster):
        res = []
        for roster in the_roster:
            res.append({
                "jid": roster[0],
                "name": roster[1],
                "subscription": roster[2]
            })
        return res

    def save_rosters(self, roster: list, timestamp):
        column = None
        roster.append(timestamp)
        roster.append(timestamp)
        print(f"PANJANG ROSTER: {len(roster)}")
        if(len(roster) == 5):
            column = ['id_owner_roster', 'jid', 'subscription', 'created_at', 'updated_at']
        elif(len(roster) == 6):
            column = ['id_owner_roster', 'jid', 'name', 'subscription', 'created_at', 'updated_at']
        print(f"COLUMN: {column}, {roster}")
        res = rosters.insert_to_table(column, roster)
        print(res)
        return res

    def get_rosters_user(self, username, data_subscription_tuple):
        query = "SELECT jid, name, subscription FROM roster WHERE id_owner_roster=? AND (subscription=? OR subscription=?)"
        # data = (username, 'to', 'both')
        data = (username,) + data_subscription_tuple
        res = rosters.get_with_query(query, data)
        res = set_to_be_format(res)
        print(f"RES GR_DB: {res}")
        return res

    def get_roster_user(self, username, jid_target):
        select_column = ["jid", 'name', 'subscription']
        columns_condition = ['id_owner_roster', 'jid']
        tuple_data_condition = (username, jid_target,)
        boolean_condition = ['AND']
        res = rosters.get_some_columns_with_limit(select_column, 1, columns_condition, tuple_data_condition, boolean_condition)
        res = set_to_be_format(res)
        if(res):
            return res[0]
        return res

    def update_subscription(self, data_set_tuple, data_condition_tuple):
        columns_set = ['name', 'subscription']
        column_condition = ['id_owner_roster', 'jid']
        boolean_condition = ['AND']
        updating = rosters.update_data(columns_set, data_set_tuple, column_condition, data_condition_tuple, boolean_condition)
        print(f"UPDATING DATA ROSTER: {updating}")
        print(rosters.get_all())

    def delete_roster_user(self, id_owner_roster, jid):
        columns_condition = ['id_owner_roster', 'jid']
        tuple_condition = (id_owner_roster, jid,)
        boolean_condition = ['AND']
        res = rosters.delete_data(columns_condition, tuple_condition, boolean_condition)
        print(res)
        print(f"ROSTER DB IN DELETE: {rosters.get_all()}")
        return res