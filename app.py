from flask import Flask, jsonify, request
import mysql.connector
import html

app = Flask(__name__)

# Thông tin kết nối đến cơ sở dữ liệu MySQL
db_config = {
    'host': '',
    'user': '',
    'password': '',
    'database': '',
    'port': 
}

def convert_unicode_to_string(s):
    return html.unescape(s)

def get_all_tables():
    # Kết nối đến cơ sở dữ liệu
    mydb = mysql.connector.connect(**db_config)
    mycursor = mydb.cursor()

    # Truy vấn danh sách tên các bảng trong cơ sở dữ liệu
    mycursor.execute("SHOW TABLES")

    # Lấy tất cả các tên bảng
    tables = [table[0] for table in mycursor.fetchall()]

    # Đóng kết nối
    mydb.close()

    return tables

def get_table_columns(table_name):
    # Kết nối đến cơ sở dữ liệu
    mydb = mysql.connector.connect(**db_config)
    mycursor = mydb.cursor()

    # Truy vấn thông tin cấu trúc của bảng
    mycursor.execute(f"SHOW COLUMNS FROM `{table_name}`")

    # Lấy tên các cột
    columns = [column[0] for column in mycursor.fetchall()]

    # Đóng kết nối
    mydb.close()

    return columns

def build_query(table_name, params):
    query = f"SELECT * FROM `{table_name}` WHERE "
    query += " AND ".join([f"{column} = %s" for column in params])
    return query

@app.route('/<table_name>', methods=['GET'])
def get_data(table_name):
    # Lấy danh sách tất cả các bảng trong cơ sở dữ liệu và chuyển sang chữ thường
    all_tables = get_all_tables()
    all_tables_lower = [table.lower() for table in all_tables]

    # So sánh tên bảng từ URL với danh sách các bảng
    if table_name in all_tables_lower:
        table_name_db = all_tables[all_tables_lower.index(table_name)]
        table_columns = get_table_columns(table_name_db)
        params = request.args.to_dict(flat=False).keys()

        filtered_params = [param for param in params if param in table_columns]

        if filtered_params:
            query = build_query(table_name_db, filtered_params)
            values = [request.args.get(param) for param in filtered_params]

            # Kết nối đến cơ sở dữ liệu
            mydb = mysql.connector.connect(**db_config)
            mycursor = mydb.cursor(dictionary=True)

            # Thực hiện truy vấn
            mycursor.execute(query, values)
            result = mycursor.fetchall()

            # Đóng kết nối
            mydb.close()

            return jsonify(result)
        else:
            return "No valid parameters provided."
    else:
        return "Table does not exist."

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
