import pyodbc
import time
import math

# This class contains the keywords necessary for connecting to SM's databases
# server_name is the server on which the database is located.
# domain_name is the domain on which the database server is located.
# user_name and password are the credentials required to connect to database (domain user).
# The server_name, domain_name, user_name and password are supplied when the class is being instantiated.
class SMDBLibrary(object):
    def __init__(self, server_IP, user_name, password):
        # Initializing the connection strings for the Infusion and CQI databases
        self._InfusionOlTP_connection_string = 'DRIVER={SQL Server};SERVER=' + server_IP + ';DATABASE=InfusionOLTP;' \
                                               'UID=' + user_name + ';PWD=' + password + ';Integrated Security=False'
        self._CQI_connection_string = 'DRIVER={SQL Server};SERVER=' + server_IP + ';DATABASE=CQI;' \
                                      'UID=' + user_name + ';PWD=' + password + ';Integrated Security=False'
        self.connection = pyodbc.Connection
        self.cursor = pyodbc.Cursor

    # This method creates a connection with the specified database. Only InfusionOLTP and CQI are supported.
    def connect_to_db(self, db_name):
        if db_name in 'InfusionOLTP' or 'CQI':
            try:
                if db_name in 'InfusionOLTP':
                    print ("Current connection string for 'InfusionOLTP' is : %s"
                           % self._InfusionOlTP_connection_string)
                    self.connection = pyodbc.connect(self._InfusionOlTP_connection_string)
                    self.cursor = self.connection.cursor()
                    return self.cursor

                elif db_name in 'CQI':
                    print ("Current connection string for 'CQI' is : %s"
                           % self._CQI_connection_string)
                    self.connection = pyodbc.connect(self._CQI_connection_string)
                    self.cursor = self.connection.cursor()
                    return self.cursor

            except Exception as e:
                raise Exception("couldn't connect to '%s' database due to exception: %s" % (db_name, str(e)))

        else:
            raise Exception("Couldn't connect to the specified Database. Please make sure that the Database name"
                            "is either 'InfusionOLTP' or 'CQI'.")

    # This method quickly counts the rows in a table
    @staticmethod
    def row_count(table_name, cursor):
        # Formulate the SQL query that would return the row count of the specified table
        sql_statement = 'select count(*) from ' + table_name

        # Execute query and return results
        cursor.execute(sql_statement)
        rows = cursor.fetchone()
        return int(rows[0])

    # This method verifies that the number of newly added CQI logs matches the number of devices multiplied by
    # CQI logs per device
    def verify_the_new_row_count_against_the_original_row_count(self, original_cqi_log_count, number_of_devices,
                                                                number_of_trials=60):
        # Get the new log count for the initial trial.
        new_cqi_log_count = self.row_count('dbo.Sequence', self.cursor)
        log_count_verified = False

        # Loop until the new log count matches the expected loop count, or timeout occurs after 60 trials
        while not log_count_verified and number_of_trials != 0:
            # Pass if the number of the newly added logs matches the number of logs from PCU Simulator
            if (new_cqi_log_count - original_cqi_log_count) == (int(number_of_devices) * 10):
                log_count_verified = True
                # Print the number of the newly added logs
                print "The number of newly added CQI logs is: " + str(new_cqi_log_count - original_cqi_log_count) + \
                      ", for %i connected devices" % int(number_of_devices)
                print "SUCCESS!"
                pass
            else:
                number_of_trials -= 1
                time.sleep(10)
                new_cqi_log_count = self.row_count('dbo.Sequence', self.cursor)
                print "The current number of CQI logs transferred to the database is: %i, " \
                      "while it is expected to be: %i." \
                      "Waiting for the rest of the logs to be transferred. %i trials left before timeout." \
                      % ((new_cqi_log_count - original_cqi_log_count), int(number_of_devices) * 10,
                         number_of_trials)

        if not log_count_verified:
            raise AssertionError("Test Failure. The number of newly added CQI logs should be: %i."
                                 % (int(number_of_devices) * 10))

    # This method closes the open connection with the database
    def close_the_open_database_connection(self):
        self.cursor.close()
        del self.cursor
        self.connection.close()

    # This method verifies that the number of CQI log sets added into the InfusionOLTP database is correct.
    def verify_that_the_correct_number_of_CQI_log_Sets_is_collected_by_Systems_Manager(self, original_log_set_count,
                                                                                       number_of_devices,
                                                                                       number_of_trials=60):
        # Get the new log count for the initial trial.
        new_log_set_count = self.row_count('Infusion.InfusionMonitorControllerCQILogEntry', self.cursor)
        log_set_count_verified = False

        # Loop until the new log set count matches the expected log set count, or timeout occurs after 60 trials
        while not log_set_count_verified and number_of_trials != 0:
            # Pass if the number of the newly added log sets matches the number of logs from PCU Simulator
            # according to the specified formula.
            if (new_log_set_count - original_log_set_count) == (int(number_of_devices) * (1 + math.ceil(10/4.0))):
                log_set_count_verified = True
                # Print the number of the newly added logs
                print "The number of newly added CQI log Sets is: " + str(new_log_set_count - original_log_set_count) \
                      + ", for %i connected devices." % int(number_of_devices)
                print "SUCCESS!"
                pass

            # If the number of newly added log sets is not correct, sleep, log the status, then continue.
            else:
                number_of_trials -= 1
                time.sleep(10)
                new_log_set_count = self.row_count('Infusion.InfusionMonitorControllerCQILogEntry', self.cursor)
                print "The current number of CQI log sets transferred to the database is: %i, but it should be %i. " \
                      "Waiting for the rest of the logs to be transferred. %i trials left before timeout." \
                      % ((new_log_set_count - original_log_set_count), int(number_of_devices) * (1 + math.ceil(10 / 4)),
                         number_of_trials)

        if not log_set_count_verified:
            raise AssertionError("Test Failure. The number of newly added CQI log Sets should be: %i."
                                 % (int(number_of_devices) * (1 + math.ceil(10/4))))
