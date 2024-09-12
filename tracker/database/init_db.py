import sqlite3
from utils.get_time import get_timestamp

class SQL():
    def __init__(self, table_name, columns_table, type_of_columns, \
                foreign_key_column = None, reference_table = None, \
                reference_column_of_table = None, db_name = None):
        self.table_name = table_name
        self.column = columns_table
        self.type_column = type_of_columns
        self.foreign_key_column = foreign_key_column
        self.reference_table = reference_table
        self.reference_column_of_table = reference_column_of_table
        self.db_name = db_name
        self.creating_new_table()

    # Helper
    def open_connection(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        return connection, cursor
    
    def close_connection(self, connection):
        connection.commit()
        connection.close()

    def helper_set_command(self, command, data, values = False):
        if(values):
            for i in data:
                command += "?" + ","
        else:
            for i in data:
                command += f"'{i}'" + ","
        command = command[:-1]
        command += ')'
        return command
    
    def helper_set_condition(self, column_condition, boolean_condition):
        idx_boolean = -1
        res = ""
        for idx in range(len(column_condition)):
            res += f"{boolean_condition[idx_boolean]+' ' if idx_boolean>-1 else ''}"
            res += f"{column_condition[idx]}=? "
            idx_boolean += 1
        return res
    
    # C
    def creating_new_table(self):
        connection, cursor = self.open_connection()
        cursor.execute("PRAGMA foreign_keys = ON;")
        command = "CREATE TABLE IF NOT EXISTS " + self.table_name + "("
        if(not self.type_column[0]):
            command += self.column[0] + " INTEGER PRIMARY KEY,"
        else:
            command += self.column[0] + f" {self.type_column[0]} PRIMARY KEY,"
        for i in range(1, len(self.column)):
            command += f"{self.column[i]} {self.type_column[i]},"
        if(self.reference_table):
            for i in range(len(self.foreign_key_column)):
                column_reference = self.foreign_key_column[i]
                table_reference = self.reference_table[i]
                column_of_table = self.reference_column_of_table[i]
                command += f" FOREIGN KEY ({column_reference}) REFERENCES {table_reference} ({column_of_table}) ON DELETE CASCADE,"
        command = command[:-1] + ")"
        cursor.execute(command)
        # cursor.execute("PRAGMA foreign_keys = OFF;")
        self.close_connection(connection)

    def insert_to_table(self, column, data):
        connection, cursor = self.open_connection()
        timestamp = get_timestamp()
        # Menambahkan timestamp created_at
        column.append('created_at')
        data.append(timestamp)
        command = f"INSERT INTO {self.table_name}("
        command = self.helper_set_command(command, column)
        command += " VALUES ("
        command = self.helper_set_command(command, data, 1)
        cursor.execute(command, data)
        inserted_id = cursor.lastrowid
        self.close_connection(connection)
        return inserted_id

    # R
    def get_with_query(self, query, data=None):
        connection, cursor = self.open_connection()
        res = None
        if(not data):
            res = cursor.execute(query)
        else:
            res = cursor.execute(query, data)
        res = res.fetchall()
        self.close_connection(connection)
        return res

    def get_all(self, column_condition=None, tuple_condition=None, boolean_condition=None):
        connection, cursor = self.open_connection()
        cmd = f"SELECT * FROM {self.table_name}"
        if(tuple_condition):
            cmd += f" WHERE {self.helper_set_condition(column_condition, boolean_condition)}"
            res = cursor.execute(cmd, tuple_condition)
        else:    
            res = cursor.execute(cmd)
        res = res.fetchall()
        self.close_connection(connection)
        return res
    
    def get_some_columns(self, columns, column_condition=None, tuple_condition=None, boolean_condition=None):
        connection, cursor = self.open_connection()
        cmd = f"SELECT {', '.join(columns)} FROM {self.table_name}"
        if(tuple_condition):
            cmd += f" WHERE {self.helper_set_condition(column_condition, boolean_condition)}"
            res = cursor.execute(cmd, tuple_condition)
        else:    
            res = cursor.execute(cmd)
        res = res.fetchall()
        self.close_connection(connection)
        return res
    
    # def get_one(self, column_condition=None, tuple_condition=None, boolean_condition=None):
    #     connection, cursor = self.open_connection()
    #     cmd = f"SELECT * FROM {self.table_name}"
    #     if(tuple_condition):
    #         cmd += f" WHERE {self.helper_set_condition(column_condition, boolean_condition)}"
    #         res = cursor.execute(cmd, tuple_condition)
    #     else:    
    #         res = cursor.execute(cmd)
    #     res = res.fetchone()
    #     self.close_connection(connection)
    #     return res
    
    def get_all_with_limit(self, limit=1, column_condition=None, tuple_condition=None, boolean_condition=None):
        connection, cursor = self.open_connection()
        cmd = f"SELECT * FROM {self.table_name}"
        if(tuple_condition):
            cmd += f" WHERE {self.helper_set_condition(column_condition, boolean_condition)}"
            print(f"CMD: {cmd}, {tuple_condition}")
            res = cursor.execute(cmd, tuple_condition)
        else:    
            res = cursor.execute(cmd)
        res = res.fetchmany(limit)
        self.close_connection(connection)
        return res
    
    def get_some_columns_with_limit(self, columns, limit=1, column_condition=None, tuple_condition=None, boolean_condition=None):
        connection, cursor = self.open_connection()
        cmd = f"SELECT {', '.join(columns)} FROM {self.table_name}"
        if(tuple_condition):
            cmd += f" WHERE {self.helper_set_condition(column_condition, boolean_condition)}"
            res = cursor.execute(cmd, tuple_condition)
        else:    
            res = cursor.execute(cmd)
        res = res.fetchmany(limit)
        self.close_connection(connection)
        return res
    
    # U
    def update_data(self, columns_set, data_set_tuple, column_condition=None,\
                    data_condition_tuple=None, boolean_condition=None):
        connection, cursor = self.open_connection()
        cmd = f"UPDATE {self.table_name} SET {'=?, '.join(columns_set)}=?"
        data_complete = data_set_tuple + data_condition_tuple
        if(column_condition):
            cmd += f" WHERE {self.helper_set_condition(column_condition, boolean_condition)}"
            res = cursor.execute(cmd, data_complete)
        else:    
            res = cursor.execute(cmd)
        res = res.rowcount
        self.close_connection(connection)
        return res
    
    # D
    def delete_data(self, column_condition=None,\
                    tuple_condition=None, boolean_condition=None):
        connection, cursor = self.open_connection()
        # cmd = f"DELETE FROM {self.table_name} WHERE {'?= AND '.join(columns)}=?"
        # res = cursor.execute(cmd, data_tuple)
        cmd = f"DELETE FROM {self.table_name}"
        if(tuple_condition):
            cmd += f" WHERE {self.helper_set_condition(column_condition, boolean_condition)}"
            print(cmd, tuple_condition)
            res = cursor.execute(cmd, tuple_condition)
        else:    
            res = cursor.execute(cmd)
        res = res.rowcount
        self.close_connection(connection)
        return res