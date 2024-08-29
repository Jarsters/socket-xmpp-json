from .init_db import SQL

table_name = "component"
columns_table = ['component_id', 'ip_address', 'port', 'type', 'connection', 'created_at']
type_of_columns = ['TEXT', 'TEXT', 'INTEGER', 'TEXT', 'INTEGER', 'INTEGER']
foreign_key_column = None
reference_table = None
reference_column_of_table = None


components = SQL(table_name, columns_table, type_of_columns, db_name="manager.db")

def save_component_to_db(component: list):
    column = ['ip_address', 'port', 'type', "component_id", 'connection']
    components.insert_to_table(column, component)

def convert_components_db(com):
    res = []
    for c in com:
        res.append({
            "username": c[0],
            'ip_local': c[1],
            'port': c[2],
            'type': c[3],
            'connection': c[4],
        })
    return res

def delete_components_db_by_id(com:SQL,\
    tuple_condition=None, boolean_condition=None):
    column_condition = ['component_id']
    tuple_condition = (tuple_condition,)
    com.delete_data(column_condition, tuple_condition, boolean_condition)
    print(com.get_all())

def delete_all_data_component_db():
    components.delete_data()