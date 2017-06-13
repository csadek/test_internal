from PcuSim import PcuSim

class PCUConnectionLibrary(object):
    def __init__(self):
        print ("Starting PCU Simulator Library ...")

    def Set_PCU_Connection_Parameters(self, server_ip, server_port, aes_key):
        self.server_ip = server_ip
        self.server_port = server_port
        self.aes_key = aes_key

    def Start_PCU_Simulator(self, device_count, device_version):
        self.pcusim = PcuSim()
        self.pcusim.start_simulator(device_count, device_version, self.server_ip, self.server_port, self.aes_key)

    def Verify_PCUs_Are_Connected(self):
        self.pcusim.verify_simulator_status("Current")

    def Disconnect_PCUs(self):
        self.pcusim.stop_simulator()

    def Verify_PCUs_Are_Disconnected(self):
        self.pcusim.verify_simulator_status("Disconnected")

    def Clear_PCU_List(self):
        self.pcusim.clear_existing_pcus()
