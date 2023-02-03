from .config import Config
from colorama import Fore, init, Style
import pymysql

class dbUtils():
    def __init__(self):
        # Connect to database
        self.connection = pymysql.connect(host=Config().db_host, user=Config().db_user, password=Config().db_pass, db=Config().db_name)

    # Function to create table if it doesn't exist
    async def create_table(self):
        print(f"{Fore.CYAN}>{Fore.WHITE} Database connected")
        try:
            # Create cursor
            with self.connection.cursor() as cursor:

                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                # check if the table already exists or not
                if ('chats',) in tables:
                    print(f"{Fore.MAGENTA}>{Fore.WHITE} Table already exists, skipping creation...")
                else:
                    # Create the table
                    sql = "CREATE TABLE chats (id INT AUTO_INCREMENT PRIMARY KEY, discord_user_id BIGINT NOT NULL, channel_id BIGINT, context_id VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, expires_at TIMESTAMP DEFAULT DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 15 MINUTE));"
                    cursor.execute(sql)
                    print(f"{Fore.GREEN}>{Fore.WHITE} Table created")

            # Save changes
            self.connection.commit()

        except Exception as e:
            # If something goes wrong, print error message
            print(f"{Fore.RED}>{Fore.WHITE} Error creating Table: {e}")
            self.connection.rollback()

    # Function to insert data into table
    async def add_user(self, discord_user_id: int, channel_id: int, context_id: str):
        try:
            # Create cursor
            with self.connection.cursor() as cursor:
                # Insert data
                sql = "INSERT INTO chats (discord_user_id, channel_id, context_id) VALUES (%s, %s, %s)"
                cursor.execute(sql, (discord_user_id, channel_id, context_id))

            # Make sure data is committed to the database
            self.connection.commit()
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
            self.connection.rollback()

    # Function to delete user from table
    async def delete_user(self, discord_user_id: int):
        try:
            # Create cursor
            with self.connection.cursor() as cursor:
                # Insert data
                sql = "DELETE FROM chats WHERE discord_user_id = %s"
                cursor.execute(sql, (discord_user_id))

            # Make sure data is committed to the database
            self.connection.commit()
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
            self.connection.rollback()

    # Function to check if user has a context id
    async def check_user(self, discord_user_id: int):
        try:
            # Create cursor
            with self.connection.cursor() as cursor:
                # Insert data
                sql = "SELECT context_id FROM chats WHERE discord_user_id = %s"
                cursor.execute(sql, (discord_user_id))
                result = cursor.fetchone()
                if result is not None:
                    return result[0]
                else:
                    return False
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
            self.connection.rollback()

    # Function to get total users in database
    async def get_total_users(self):
        try:
            # Create cursor
            with self.connection.cursor() as cursor:
                # Insert data
                sql = "SELECT COUNT(*) FROM chats"
                cursor.execute(sql)
                result = cursor.fetchone()
                return result[0]
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
            self.connection.rollback()

    # Function to get the discord_ids in the database
    async def get_discord_ids(self):
        try:
            # Create cursor
            with self.connection.cursor() as cursor:
                # Insert data
                sql = "SELECT discord_user_id FROM chats"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
            self.connection.rollback()

    # Function to delete expired users
    async def deleteExpiredUsers(self):

        try:
            # Create cursor
            with self.connection.cursor() as cursor:
                # Insert data
                sql = "DELETE FROM chats WHERE expires_at < NOW()"
                cursor.execute(sql)
                
            # Make sure data is committed to the database
            self.connection.commit()
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
            self.connection.rollback()

    # Function to get expired channels
    async def getExpiredChannels(self):
        try:
            # Create cursor
            with self.connection.cursor() as cursor:
                # Insert data
                sql = "SELECT channel_id FROM chats WHERE expires_at < NOW()"
                cursor.execute(sql)
                fetch = cursor.fetchall()
                result = []
                for channel in fetch:
                    result.append(channel[0])
                return result
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
            self.connection.rollback()