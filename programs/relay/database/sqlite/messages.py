from .init_db import SQL

table_name = "messages"
columns_table = ['message_id', 'initiator', 'receiver', "message", 'created_at']
type_of_columns = ['', 'TEXT', 'TEXT', 'TEXT', 'INTEGER']
foreign_key_column = None
reference_table = None
reference_column_of_table = None

message = SQL(table_name, columns_table, type_of_columns, db_name='relay.db')

def save_message_to_db(data_message: list):
    column = ["initiator", "receiver", "message", "created_at"]
    message.insert_to_table(column, data_message)

def get_all_message():
    return message.get_all()

# Fungsionalitas menghapus semua yang ada di database message
def delete_all_data_message_db():
    message.delete_data()