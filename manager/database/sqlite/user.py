from .init_db import SQL

table_name = "user"
columns_table = ['user_id', 'password', 'bio', "online", 'created_at', 'updated_at']
type_of_columns = ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'INTEGER']
foreign_key_column = None
reference_table = None
reference_column_of_table = None

users = SQL(table_name, columns_table, type_of_columns, db_name='manager.db')
# users = SQL(table_name, columns_table, type_of_columns, db_name='manager.sql')

# Ide 1 jadiin fungsi aja

def set_to_be_format_presence(data):
    return {
        'stanza': 'presence',
        'from': data[0],
        'username': data[0],
        "bio": data[1],
        "online": data[2],
        "updated_at": data[3],
    }

# Fungsionalitas mendapatkan user dari database berdasarkan username
def get_user_by_username(username=None):
    column_condition = ["user_id"]
    tuple_condition = (username,)
    user = users.get_all_with_limit(1, column_condition, tuple_condition)
    if(user):
        return user[0]
    return user

def save_user_to_db(data_user: list):
    column = ["user_id", "password", "bio", "online", "created_at", "updated_at"]
    users.insert_to_table(column, data_user)

def get_all_users():
    return users.get_all()

# Fungsionalitas untuk mendapatkan status online user
def get_user_online(username):
    columns = ['online']
    columns_condition = ['user_id']
    data_condition_tuple = (username,)
    res = users.get_some_columns_with_limit(columns, 1, columns_condition, data_condition_tuple)
    if(res):
        return res[0][0]
    return 0

def get_presence_user(username):
    columns_target = ["user_id", "bio", "online", "updated_at"]
    column_condition = ['user_id']
    tuple_data_condition = (username,)
    presence = users.get_some_columns_with_limit(columns_target, 1, column_condition, tuple_data_condition)
    if(presence):
        presence = set_to_be_format_presence(presence[0])
        return presence
    return False

def update_status_online(columns_set, data_set_tuple,\
                         columns_condition, data_condition_tuple):
    users.update_data(columns_set, data_set_tuple, columns_condition, data_condition_tuple)
    print(f"UPDATING STATUS ONLINE: {users.get_all(columns_condition, data_condition_tuple)}")

def update_bio(columns_set, data_set_tuple,\
                         columns_condition, data_condition_tuple):
    users.update_data(columns_set, data_set_tuple, columns_condition, data_condition_tuple)
    print(f"UPDATING BIO: {users.get_all()}")

# Fungsionalitas menghapus semua yang ada di database user
def delete_all_data_component_db():
    users.delete_data()

# Ide 2 dijadiin kelas dengan inheritance SQL (SQLite)

class User(SQL):
    def __init__(self, table_name, columns_table, type_of_columns, \
                foreign_key_column = None, reference_table = None, \
                reference_column_of_table = None, db_name = None):
        super().__init__(table_name, columns_table, type_of_columns, \
                foreign_key_column, reference_table, \
                reference_column_of_table, db_name)

    def set_to_be_format_presence(self, data):
        return {
            'stanza': 'presence',
            'from': data[0],
            'username': data[0],
            "bio": data[1],
            "online": data[2],
            "updated_at": data[3],
        }

    def get_user_by_username(self, username=None):
        column_condition = ["user_id"]
        tuple_condition = (username,)
        user = users.get_all_with_limit(1, column_condition, tuple_condition)
        if(user):
            return user[0]
        return user

    def save_user_to_db(self, data_user: list):
        column = ["user_id", "password", "bio", "online", "created_at", "updated_at"]
        users.insert_to_table(column, data_user)

    def get_all_users(self, ):
        return users.get_all()

    def get_user_online(self, username):
        columns = ['online']
        columns_condition = ['user_id']
        data_condition_tuple = (username,)
        print("GUO")
        res = users.get_some_columns_with_limit(columns, 1, columns_condition, data_condition_tuple)
        print(res)
        if(res):
            return res[0][0]
        return 0

    def get_presence_user(self, username):
        columns_target = ["user_id", "bio", "online", "updated_at"]
        column_condition = ['user_id']
        tuple_data_condition = (username,)
        presence = users.get_some_columns_with_limit(columns_target, 1, column_condition, tuple_data_condition)
        if(presence):
            presence = set_to_be_format_presence(presence[0])
            return presence
        return False

    def update_status_online(self, columns_set, data_set_tuple,\
                            columns_condition, data_condition_tuple):
        users.update_data(columns_set, data_set_tuple, columns_condition, data_condition_tuple)
        print(f"UPDATING STATUS ONLINE: {users.get_all()}")

    def update_bio(self, columns_set, data_set_tuple,\
                            columns_condition, data_condition_tuple):
        users.update_data(columns_set, data_set_tuple, columns_condition, data_condition_tuple)
        print(f"UPDATING BIO: {users.get_all()}")

    def delete_all_data_component_db(self, ):
        users.delete_data()