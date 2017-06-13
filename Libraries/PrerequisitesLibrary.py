import os.path
import subprocess
import pyodbc
import time


class PrerequisitesLibrary(object):
    def __init__(self):
        # Dependencies parameters
        self._dependencies_bat_file = os.path.join(os.path.dirname(__file__), '..', 'Resources', 'BatchFiles', 'Dependencies.bat')
        self._power_shell_path = r'C:\Windows\sysnative\WindowsPowerShell\v1.0\powershell.exe'

        # SQL Login Parameters
        self._sql_script_path = os.path.join(os.path.dirname(__file__), '..', 'Resources', 'create_domain_logins.sql')

        # SQL Installation Parameters
        self._sql_install_bat_file = os.path.join(os.path.dirname(__file__), '..', 'Resources', 'BatchFiles', 'SQL_Installation.bat')

        # Restart SQl server parameters
        self._sql_server_restart_bat_file = os.path.join(os.path.dirname(__file__), '..', 'Resources', 'BatchFiles', 'restart_sql_server.bat')

        # Domain controller parameters
        self._domain_controller_bat_file = os.path.join(os.path.dirname(__file__), '..', 'Resources', 'BatchFiles', 'create_local_domain.bat')

    # Install project dependencies: Python + Modules
    def install_dependencies(self):
        print ("Starting to execute the batch file: " + self._dependencies_bat_file)
        with open("dependencies_install.log", "w+") as f:
            subprocess.call(self._dependencies_bat_file, stdout=f, stderr=f)

    # Installing SQl Server
    def install_sql_server(self, cfn_tools_path, sql_key):
        print ("Starting to execute the batch file: " + self._sql_install_bat_file)
        path = '&"' + self._sql_install_bat_file + '"'
        with open("sql_install.log", "w+") as f:
            subprocess.Popen([self._power_shell_path, path, '"' + cfn_tools_path + '"', sql_key], stdout=f, stderr=f)

    # Verify the installation of sql server is completed successfully
    def verify_sql_server_installation(self, server_name):
        # Set the SQL server connection string
        _master_connection_string = 'DRIVER={SQL Server Native Client 11.0};SERVER=' + server_name + '; Trusted_Connection=Yes;'
        counter = 0
        # Try to connect to SQL for 30 minutes
        while counter < 1800:
            try:
                print ("Try to connect to the SQL ......")
                pyodbc.connect(_master_connection_string)
                print ("The connection is succeeded")
                time.sleep(60)
                return
            except Exception:
                print ("The connection is failed")
                counter += 1
                time.sleep(1)
                pass
        print ("The SQL server isn't installed successfully")
        raise AssertionError("Test Failed")

    # Disable the restart flag to avoid the machine restart before starting the other projects
    def Disable_Restart_Flag(self, cfn_tools_path):
        file_path = os.path.join(cfn_tools_path, 'AlarisDCPromo.bat')

        # Read contents of the batch file for domain creation
        bat_file = open(file_path, "r")
        content = bat_file.read()
        bat_file.close()

        # Replace the reboot flag to avoid forced reboot of VM
        old_flag = "NoRebootOnCompletion:$false"
        new_flag = "NoRebootOnCompletion:$true"
        content = content.replace(old_flag, new_flag)

        # Write new file contents
        bat_file = open(file_path, "w")
        bat_file.write(content)
        bat_file.close()

    # Create a local domain controller with domain name
    def create_local_domain_controller(self, cfn_tools_path, domain_name):
        print ("Starting to execute the batch file: " + self._domain_controller_bat_file + " with Domain Name: " + domain_name)
        path = '&"' + self._domain_controller_bat_file + '"'
        with open("domain_creation.log", "w+") as f:
            subprocess.call([self._power_shell_path, path, '"' + cfn_tools_path + '"', domain_name], stdout=f, stderr=f)

    def restart_VM(self, wait_time):
        subprocess.Popen("shutdown -r -t " + wait_time)

    # Create the SQL Login
    def Create_SQL_Login_from_Domain(self, domain_name):
        print ("Starting to execute the batch file: " + self._sql_script_path + " with Domain Name: " + domain_name)
        subprocess.call("sqlcmd -i " + self._sql_script_path + " -v Domain_Name = " + domain_name)

    # Restart sql services after sql login creation
    def Restart_SQL_Service(self):
        print ("Starting to execute the batch file: " + self._sql_server_restart_bat_file)
        subprocess.call(self._sql_server_restart_bat_file)




