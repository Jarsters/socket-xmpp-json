from .init_db import SQL

table_name = "component"
columns_table = ['component_id', 'ip_address', 'port', 'type', 'is_private', 'status', 'created_at', 'updated_at']
type_of_columns = ['', 'TEXT', 'INTEGER', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'INTEGER']
foreign_key_column = None
reference_table = None
reference_column_of_table = None

components = SQL(table_name, columns_table, type_of_columns, db_name="tracker.db")
# components = SQL(table_name, columns_table, type_of_columns, db_name="tracker.sql")

'''
    {
        "ip_address"
        "port"
        "type"
        "created_at",
        "updated_at",
        "status": True/False
    }
'''

def save_component_to_db(component: list, get_timestamp):
    timestamp = get_timestamp()
    column = ['ip_address', 'port', 'type', 'is_private', 'created_at', 'updated_at', 'status']
    component.append(timestamp)
    component.append(timestamp)
    component.append(1)
    return components.insert_to_table(column, component)

def formatting_components(data):
    res = []
    if(data and len(data[0]) == 5):
        for d in data:
            res.append({
                'ip_local': d[0],
                'port': d[1],
                'type': d[2],
                'is_private': d[3],
                'status': d[4]
            })
    else:
        for d in data:
            res.append({
                'ip_local': d[0],
                'port': d[1],
                'type': d[2],
                'is_private': d[3],
            })
    return res

def get_all():
    column = ['ip_address', 'port', 'type', 'is_private', 'status']
    res = components.get_some_columns(column)
    return formatting_components(res)

def get_components():
    column = ['ip_address', 'port', 'type', 'is_private']
    column_condition = ['status']
    tuple_condition = (1,)
    res = components.get_some_columns(column, column_condition, tuple_condition)
    return formatting_components(res)

def delete_component_by_id(id, get_timestamp):
    timestamp = get_timestamp()
    column_set = ['status', 'updated_at']
    tuple_set = (0, timestamp,)
    column_condition = ['component_id']
    tuple_condition = (id,)
    components.update_data(column_set, tuple_set, column_condition, tuple_condition)

def delete_components():
    components.delete_data()