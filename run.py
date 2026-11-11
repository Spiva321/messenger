# from app import create_app
#
# app = create_app()
#
# if __name__ == '__main__':
#     app.run()

import psycopg2
conn = psycopg2.connect(host='10.199.200.129',
                        port=5432, dbname='messenger',
                        user='PostgresSpookky',
                        password=input('Password: '),
                        connect_timeout=5)
print('PostgreSQL connection successful'); conn.close()