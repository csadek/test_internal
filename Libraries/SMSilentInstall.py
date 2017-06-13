import os
import subprocess
import requests
from requests_ntlm import HttpNtlmAuth
from time import sleep


class SMSilentInstall(object):

    def __init__(self):
        print 'Starting SM silent installation'

    def extract_MSI_installer(self, initial_path):
        print 'Extracting MSI installer from the EXE'
        build_name = os.listdir(initial_path)[0]
        installer_path = initial_path + "\\" + build_name
        msi_folder = os.path.dirname(installer_path) + '\\setupfiles'
        print 'MSI Path is: ' + msi_folder
        subprocess.call('"' + installer_path + '"' + ' /s /x /b"' + msi_folder + '" /v" /qn"')
        print 'MSI file is extracted'
        self.msi_path = os.path.join(msi_folder, u"Alaris Systems Manager.msi")
        print 'MSI Full path is: ' + self.msi_path

    def set_installation_parameters(self):
        self.IS_SQLSERVER_SERVER = self.sql_server
        self.IS_NET_API_LOGON_USERNAME = self.domain_name + '\\' + self.user_name
        self.IS_NET_API_LOGON_PASSWORD = self.password
        self.SQLJOBADMIN = self.domain_name + '\\' + self.user_name
        self.AUTHENTICATION_DOMAIN = self.domain_name
        self.AUTHENTICATION_USERNAME = self.user_name
        self.SMADMIN_LOGON_USERNAME = self.user_name
        self.IS_NET_API_LOGON_DOMAIN_TOKEN = self.domain_name
        self.IS_NET_API_LOGON_USERNAME_TOKEN = self.user_name
        self.SSLCERTPATH = self.cert_file
        self.CERTPASSWORD = self.cert_password
        self.SM_APPPOOL_USERNAME = self.domain_name + '\\' + self.user_name
        self.SM_APPPOOL_PWD = self.password

    def set_domain_name(self, domain_name):
        self.domain_name = domain_name

    def set_credentials(self, user_name, password):
        self.user_name = user_name
        self.password = password

    def set_sql_server(self, sql_server):
        self.sql_server = sql_server

    def set_certificate(self, cert_file, cert_password):
        self.cert_file = cert_file
        self.cert_password = cert_password

    def run_SM_installation(self):
        install_command = 'msiexec.exe /i "' + self.msi_path + '" '\
                               'IS_SQLSERVER_SERVER=' + self.IS_SQLSERVER_SERVER + ' '\
                               'IS_NET_API_LOGON_USERNAME=' + self.IS_NET_API_LOGON_USERNAME + ' '\
                               'IS_NET_API_LOGON_PASSWORD=' + self.IS_NET_API_LOGON_PASSWORD + ' '\
                               'AUDITLOGEXPENABLE=1 SQLJOBADMIN=' + self.SQLJOBADMIN + ' '\
                               'AUTHENTICATION_DOMAIN=' + self.AUTHENTICATION_DOMAIN + ' '\
                               'AUTHENTICATION_USERNAME=' + self.AUTHENTICATION_USERNAME + ' '\
                               'SMADMIN_LOGON_USERNAME=' + self.SMADMIN_LOGON_USERNAME + ' '\
                               'IS_NET_API_LOGON_DOMAIN_TOKEN=' + self.IS_NET_API_LOGON_DOMAIN_TOKEN + ' '\
                               'IS_NET_API_LOGON_USERNAME_TOKEN=' + self.IS_NET_API_LOGON_USERNAME_TOKEN + ' '\
                               'SSLCERTPATH=' + self.SSLCERTPATH + ' CERTPASSWORD="' + self.CERTPASSWORD + '" '\
                               'SM_APPPOOL_USERNAME=' + self.SM_APPPOOL_USERNAME + ' '\
                               'SM_APPPOOL_PWD=' + self.SM_APPPOOL_PWD + ' /norestart /log InstallLog.txt /passive'

        print 'Installation command is: ' + install_command
        subprocess.call(install_command)

    def verify_SM_is_installed(self, trials=40, interval=15):
        session = requests.session()
        session.auth = HttpNtlmAuth(self.user_name, self.password, session)
        session.verify = False
        verified = False
        while (trials > 0) and not verified:
            sleep(interval)
            response = session.get('https://localhost/SystemsManager')
            if response.status_code == 200:
                verified = True
                session.close()
            else:
                trials -= 1

        if not verified:
            raise Exception('SM not installed within the specified time frame of {} seconds'.format(str(trials*interval)))

    def install_certificate(self):
        print 'Importing certificate'
        subprocess.call('CERTUTIL -f -p "{}" -importpfx {}'.format(self.CERTPASSWORD, self.SSLCERTPATH))
