from .init_db import SQL

table_name = "component"
columns_table = ['component_id', 'ip_address', 'port', 'type', 'connection', 'created_at', 'updated_at']
type_of_columns = ['TEXT', 'TEXT', 'INTEGER', 'TEXT', 'INTEGER', 'INTEGER', 'INTEGER']
foreign_key_column = None
reference_table = None
reference_column_of_table = None


components = SQL(table_name, columns_table, type_of_columns, db_name="manager.db")
# components = SQL(table_name, columns_table, type_of_columns, db_name="manager.sql")

# Ide 1 jadiin fungsi aja

def save_component_to_db(component: list, get_timestamp):
    timestamp = get_timestamp()
    column = ['ip_address', 'port', 'type', "component_id", 'connection', 'created_at', 'updated_at']
    component.append(timestamp)
    component.append(timestamp)
    components.insert_to_table(column, component)

def get_relay_with_less_connection_db():
    query = "SELECT component_id, MIN(connection) FROM component"
    res_query = components.get_with_query(query)
    less_connection_id = res_query[0][0]
    res = components.get_all_with_limit(1, ['component_id'], (less_connection_id,))
    res = convert_components_db(res)
    print(f"Relay koneksi paling sedikit {res}")
    return res

def convert_components_db(com):
    print("Convert in COMPONENT DB")
    res = []
    for c in com:
        res.append({
            "username": c[0],
            'ip_local': c[1],
            'port': c[2],
            'type': c[3],
            'connection': c[4],
        })
    print(f"Result {res}")
    return res

def update_total_connection(id, get_timestamp, tipe=None):
    # Mendapatkan total connection dari relay dengan id
    connection = components.get_some_columns_with_limit(['connection'], 1, ['component_id'], (id,))[0][0]
    timestamp = get_timestamp()
    if(tipe == "NCIR"):
        connection += 1
    elif(tipe == "ECIR"):
        connection -= 1
    # Memperbarui total connection dari relay dengan id
    components.update_data(['connection', 'updated_at'], (connection, timestamp), ['component_id'], (id,))
    print(f"{tipe}_DB: {components.get_all()}")

def delete_components_db_by_id(com:SQL,\
    tuple_condition=None, boolean_condition=None):
    column_condition = ['component_id']
    tuple_condition = (tuple_condition,)
    com.delete_data(column_condition, tuple_condition, boolean_condition)
    print(com.get_all())

def delete_all_data_component_db():
    components.delete_data()

# Ide 2 dijadiin kelas dengan inheritance SQL (SQLite)

class Component(SQL):
    def __init__(self, table_name, columns_table, type_of_columns, \
                foreign_key_column = None, reference_table = None, \
                reference_column_of_table = None, db_name = None):
        super().__init__(table_name, columns_table, type_of_columns, \
                foreign_key_column, reference_table, \
                reference_column_of_table, db_name)

    def save_component_to_db(self, component: list, get_timestamp):
        timestamp = get_timestamp()
        column = ['ip_address', 'port', 'type', "component_id", 'connection', 'created_at', 'updated_at']
        component.append(timestamp)
        component.append(timestamp)
        components.insert_to_table(column, component)

    def get_relay_with_less_connection_db(self, ):
        query = "SELECT component_id, MIN(connection) FROM component GROUP BY component_id"
        res_query = components.get_with_query(query)
        # print(f"RES QUERY: {res_query}")
        less_connection_id = res_query[0][0]
        res = components.get_all_with_limit(1, ['component_id'], (less_connection_id,))
        # print(convert_components_db(res))
        res = convert_components_db(res)
        # print(f"GRWLS_DB: {res}")
        return res

    def convert_components_db(self, com):
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

    def update_total_connection(self, id, get_timestamp, tipe=None):
        connection = components.get_some_columns_with_limit(['connection'], 1, ['component_id'], (id,))[0][0]
        timestamp = get_timestamp()
        if(tipe == "NCIR"):
            connection += 1
        elif(tipe == "ECIR"):
            connection -= 1
        components.update_data(['connection', 'updated_at'], (connection, timestamp), ['component_id'], (id,))
        print(f"{tipe}_DB: {components.get_all()}")

    def delete_components_db_by_id(self, com:SQL,\
        tuple_condition=None, boolean_condition=None):
        column_condition = ['component_id']
        tuple_condition = (tuple_condition,)
        com.delete_data(column_condition, tuple_condition, boolean_condition)
        print(com.get_all())

    def delete_all_data_component_db(self, ):
        components.delete_data()