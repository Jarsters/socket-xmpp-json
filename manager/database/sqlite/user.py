from init_db import SQL

table_name = "user"
columns_table = ['user_id', 'password', 'bio', "online", 'created_at', 'updated_at']
type_of_columns = ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'INTEGER']
foreign_key_column = None
reference_table = None
reference_column_of_table = None

users = SQL(table_name, columns_table, type_of_columns)

def get_user_by_username(tuple_condition=None):
    column_condition = ["user_id"]
    tuple_condition = (tuple_condition,)
    return users.get_all_with_limit(1, column_condition, tuple_condition)[0]

def save_user_to_db(data_user: list):
    column = ["user_id", "password", "bio", "online", "created_at", "updated_at"]
    users.insert_to_table(column, data_user)

def update_status_online(columns_set, data_set_tuple,\
                         columns_condition, data_condition_tuple):
    pass