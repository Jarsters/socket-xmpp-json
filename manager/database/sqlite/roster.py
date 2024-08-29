from init_db import SQL

table_name = "roster"
# user_id atau phone_number, bisa so so lah ya
columns_table = ['roster_id', 'id_owner_roster', 'jid', 'name', 'subscription', 'created_at', 'updated_at']
type_of_columns = ['', 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER']
foreign_key_column = ['id_owner_roster']
reference_table = ['user']
reference_column_of_table = ['user_id']

rosters = SQL(table_name, columns_table, type_of_columns, foreign_key_column,\
              reference_table, reference_column_of_table)