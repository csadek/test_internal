import subprocess
import os.path
import time


class PostDomainConfigurationLibrary(object):

    def __init__(self):
        # Post configuration parameters
        self._post_configuration_bat_file = os.path.join(os.path.dirname(__file__), '..', 'Resources', 'BatchFiles', 'post_domain_creation.bat')

    # Check the node status, it should be up and running after the local domain creation restart
    def Check_the_node_status(self, installation_node):
        # Set the node IP address
        site = installation_node
        # Configure the number of Ping counts
        ping_count = 1
        machine_ready = False
        counter = 0
        # Waiting the node to be restarted
        time.sleep(30)
        while not machine_ready and counter < 300:
            # Ping the node machine
            process = subprocess.Popen(['ping', site, '-n', str(ping_count)])
            return_code = process.wait()
            print (site)
            # Check the return code of ping process
            if return_code == 0:
                print ("The machine is ready")
                time.sleep(60)
                return
            else:
                print ("Trying to access the machine iteration : " + str(counter))
                counter += 1
                time.sleep(1)
        print ("The Machine isn't ready within : " + str(counter) + " iterations")
        #raise AssertionError("Connection Failed")

    def Configure_the_machine_after_domain_creation(self, ps_tool_path, server_ip, username, password, ps_script_location):
        print ("Starting to execute the batch file: " + self._post_configuration_bat_file)
        process = subprocess.Popen([self._post_configuration_bat_file, ps_tool_path, server_ip, username, password, ps_script_location])
        return_code = process.wait()
        if return_code != 0:
            print ("The machine configuration isn't completed successfully with return code : " + str(return_code))
            raise AssertionError("Configuration failed")



