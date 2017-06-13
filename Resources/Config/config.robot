*** Variables ***
# vCommander parameters
${Revert Browser}           Chrome
${Login URL}                https://vcommander01.cfnp.local/portal
${Login Username}           SA-M2-Test-Automatio
${Login Password}           Welcome@1234567

# Build files extraction parameters
${Build File Pattern}       svrapps_*.zip
${Build Version Prefix}     svrapps_
${PCI File Pattern}         alaris-system-manager-pci_*.zip
${PCI Version Prefix}       alaris-system-manager-pci_
${SM Destination}           ../../
${Workspace}                C:\\M2_Automation\\Workspace-V12
${Remote Workspace}         ../../RobotTests

# Jenkins parameters
${Jenkins IP}               10.160.213.86
${Jenkins URL}              http://${Jenkins IP}:8080
${Jenkins Home}             C:\\Program Files (x86)\\Jenkins\\workspace
${Jenkins Slave Home}       C:\\JenkinsSlave\\workspace
${Host SSH Username}        administrator
${Host SSH Password}        carefusion

# Log files parameters
${Revert Log Pattern}       01_Revert_VM_Log*.html
${Copy Files Log Pattern}   02_Copy_Files_Log*.html
${Prereq Log Pattern}       03_Install_Prereq_Log*.html
${Configure Log Pattern}    04_Post_Domain_Config_Log*.html
${Logins Log Pattern}       05_Create_Logins_Log*.html
${SM Install Log Pattern}   06_SM_Installation_Log*.html
${Smoke Log Pattern}        07_SM_Smoke_Tests_Log*.html

# Prerequisites parameters
${SQL Key}                   RBGFQ-HY6V7-PKF93-8GGM3-VB23Y
${CFN tool Path}             C:\\CFN Tools
${PSEXEC tool Path}          C:\\PSTools

# New User Credentials
${New User Name}            TestUser
${New User Password}        $ecureC0re@1234
${New User ID}              ${New User Name}@${Trusted Domain}