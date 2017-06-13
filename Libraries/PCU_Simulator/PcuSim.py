"""Library for integrating *PCU Simulator* with Robot Framework.

This library will utilize the existing libraries from the PCU Simulator
to emulate several PCU devices for stress and activity testing

`start_simulator` will start the defined number of PCU device simulators


"""
import sys
import os
from time import sleep
import clr

module_dir, module_file = os.path.split(__file__)
sys.path.append(module_dir + "\\include-net")
clr.AddReference(module_dir + '\\include-net\\PcuSimulator')
clr.AddReference('System.Net')
from PcuSimulator import Simulator, RandomOrSequentialOptions, ConfigurationOptions, DeviceOptions, DeviceVersionInfo, ModuleInfo, ModuleType, LogOptions, DataSetOptions, DeviceElementOptions
from System.Net import IPEndPoint, IPAddress

__version__ = '0.3'


class PcuSim:
    # PcuCollection = []
    current_sn = 0

    def __init__(self):
        self.PcuCollection = []
        self._pcusim = Simulator()
        self._pcusim.PcuCreated += self._pcu_created_event
        # self._pcusim.PcuConnectionStatusChanged += self._pcu_connection_status_changed
        self._current_status = ""

    def _pcu_connection_status_changed(self, pcu):
        print("Connection Status Changed: " + pcu.Status)

    def _pcu_created_event(self, pcu):
        print("PCU Created with SN: " + str(pcu.DeviceOptions.Serial))
        self.PcuCollection.append(pcu)

    def _start_pcus(self):
        print("Starting PCU's")
        sleep(0.5 * len(self.PcuCollection))
        for pcu in self.PcuCollection:
            ip_address = IPAddress.Parse(self._server_address)
            ip_endpoint = IPEndPoint(ip_address, self._server_port)
            # pcu.PropertyChanged += self._property_changed
            pcu.Connect(ip_endpoint)
            print("PCU Started, SN: " + str(pcu.DeviceOptions.Serial))
            sleep(2)

    def stop_simulator(self):
        for pcu in self.PcuCollection:
            pcu.Disconnect(True)
            print ("PCU Disconnected, SN: " + str(pcu.DeviceOptions.Serial))
            sleep(3)

    def start_simulator(self, number_of_devices, pcu_version, server_address, server_port, aes_key):
        """Start Simulator Starts the specified number of PCU Simulator Instances
           Start Simulator  number_of_devices  server_address  server_port  aes_key
        """

        # Settings > General > Configuration Options
        configuration_options = ConfigurationOptions()
        configuration_options.ServerAddress = server_address
        configuration_options.ServerPort = int(server_port)
        configuration_options.NetworkInterfaceCard = "Default"
        self._server_address = server_address
        self._server_port = int(server_port)

        # Settings > General > Serial Number Options
        serial_options = RandomOrSequentialOptions()
        serial_options.OptionType = 0
        serial_options.SequentialStartValue = self.current_sn + 1
        serial_options.SequentialIncrement = 1
        serial_options.ModuleOptionType = 0
        serial_options.ModuleSequentialStartValue = 1
        serial_options.ModuleSequentialIncrement = 1

        # Settings > General > Initial Connection Delay Options
        connection_options = RandomOrSequentialOptions()
        connection_options.OptionType = 1
        # connection_options.SequentialStartValue = 0
        # connection_options.SequentialIncrement = 0

        # Settings > Device > Version Options
        device_version = DeviceVersionInfo()
        device_version.MainVersion = pcu_version
        device_version.BootVersion = "1.0.0.0"
        device_version.PowerSupplyVersion = "1.0.0.0"
        device_version.KeyboardVersion = "1.0.0.0"

        # Settings > Device > Module Options
        module_info = ModuleInfo()
        module_info.ModuleChannel = 'A'
        module_info.MoudleType = 1
        module_info.ModuleVersion = "1.0.0.0"

        # Settings > Device > Device Options
        device_options = DeviceOptions()
        device_options.Bssid = "00:11:22:33:44:55"
        device_options.Model = 8015
        device_options.Serial = 1
        device_options.PatientId = "Test Patient"
        device_options.IsDcmpV3 = True
        device_options.IsDcmpV2 = False

        # Settings > Connection > Encryption Options
        device_options.UseAuthentication = True
        device_options.UseInvalidSharedSecret = False
        device_options.UseAuthenticationMessageEcho = False
        device_options.DisconnectAfterSocketOpen = False

        device_options.EnableEncryption = True
        device_options.SupportCbc = True
        device_options.SupportEcb = False
        device_options.AesKey = aes_key

        # Settings > Connection > Other Options
        device_options.DeviceLatencyInMilliseconds = 0
        device_options.InitialConnectionDelayInMilliseconds = 0
        device_options.ReconnectDelayInSeconds = 1
        device_options.EnforceSerialNumberBounds = False
        device_options.ReconnectOnDisconnect = False
        device_options.UseInitialConnectionDelay = False
        device_options.DeviceVersionInfo = device_version
        device_options.ModuleA = module_info

        # Settings > Logs
        log_options = LogOptions()
        log_options.HistoricalLogCount = 10
        log_options.OverrideHistoricalLogSequence = False
        log_options.CqiLogCount = 10
        log_options.GuardrailsLogVersion = "2.0.0.0"

        # Settings > Data Set
        dataset_options = DataSetOptions()

        # V12 Device Element Options
        device_element_options = DeviceElementOptions()
        device_element_options.AutoIdId = "N/A"
        device_element_options.PcuFirmwareId = "N/A"
        device_element_options.LvpFirmwareId = "N/A"
        device_element_options.NetworkConfigId = "N/A"
        device_element_options.ManifestFileName = "None"
        device_element_options.SupportValidatePackage = False
        device_element_options.SupportResumePackage = False

        self._pcusim.CreatePcus(number_of_devices, configuration_options, serial_options, connection_options,\
                                 device_options, log_options, dataset_options, device_element_options, None)
        self._start_pcus()

    def verify_simulator_status(self, status, number_of_trials=60, trial_intervals=10):
        # Verifying that the PCU's status is either Current or Disconnected
        """ Number of trials and trial intervals are set to 12 and 15 respectively, unless explicitly specified in the
        test step."""
        for pcu in self.PcuCollection:
            # If the status of the PCU doesn't immediately match the expected status:
            int_number_of_trials = int(number_of_trials)
            int_trial_intervals = int(trial_intervals)

            # Loop until the status matches the expected status, or timeout occurs.
            while (int_number_of_trials != 0) and (status not in pcu.Status):
                if pcu.Status != status:
                    print ("Waiting for PCU: %s to become %s..." % (str(pcu.DeviceOptions.Serial), status))
                    int_number_of_trials -= 1
                    sleep(int_trial_intervals)

            # After exiting the While Loop, verify that the PCU status is as expected.
            if status in pcu.Status:
                print ("Verified. The status of PCU: %s is now %s!" % (str(pcu.DeviceOptions.Serial), status))
            else:
                raise AssertionError("Verification timeout. The status of PCU: %s is %s!"
                                     % (str(pcu.DeviceOptions.Serial), pcu.Status))

    def verify_dataset_deployment(self, dataset_name, number_of_trials=30, wait_time=20):
        # Verify that the Data set is deployed successfully to each PCU
        for pcu in self.PcuCollection:
            while (number_of_trials != 0) and ("Current" not in pcu.Status):
                sleep(wait_time)
                number_of_trials -= 1
        # Assert if the uploaded data set name is the same data set name deployed
            if (number_of_trials == 0) and ("Current" not in pcu.Status):
                raise Exception("Verification timeout. Data Set deployment took longer than expected.")

            if "Current" in pcu.Status:
                if dataset_name in pcu.DatasetStatusText:
                    print("DataSet:%s is deployed successfully to this PCU" % (str(pcu.DatasetStatusText)))
                else:
                    raise AssertionError("DataSet is not deployed successfully to this PCU")

    def verify_wireless_package_deployment(self, number_of_trials=30, wait_time=10):
        # Verify that the Wireless Package is deployed successfully to each PCU
        for pcu in self.PcuCollection:
            while (number_of_trials != 0) and ("Current" not in pcu.Status):
                sleep(wait_time)
                number_of_trials -= 1

            if (number_of_trials == 0) and ("Current" not in pcu.Status):
                raise Exception("Verification timeout. Wireless Package deployment took longer than expected.")

            if "Current" in pcu.Status:
                print("Wireless Package is deployed successfully to this PCU")
            else:
                raise AssertionError("Wireless Package is not deployed successfully to this PCU")

    def clear_existing_pcus(self):
        """ This method is used to clear the list of created PCUs, in case the scenario needs to start over with
        creating new PCUs """
        self.PcuCollection = []
        print str(self.PcuCollection) + ". Existing PCUs are cleared."
