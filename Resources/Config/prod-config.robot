*** Settings ***
Resource                    config.robot
*** Variables ***
# Test Execution parameters
${Test Browser}             Chrome
${VM Name}                  135977-02_Win2012R2_UnifiedCore_1.1-001-mohab.ayman@carefusion.com
${Snapshot}                 Ready for PCI Installation

# Systems Manager parameters
${Server IP}                10.160.210.149
${Server Name}              SMautovm2.SMAutomation.Local
${Server Port}              3613
${AES Key}                  3D 29 DD 5C F5 69 46 17 61 D9 1B 70 EE 80 48 63
${Server Username}          alarisadmin
${Server Password}          $ecureC0re@2018
${Trusted Domain}           SMAutomation.Local
${DB User UserName}         smautouser
${DB User Password}         password_123456

# Device Parameters
${Device Version}           12.1.0.0

# Facility Creation parameters
${Facility Name}            SMFTest
${Facility Desc}            Test the automation of Adding Facility
${IP Start}                 0.0.0.0
${IP End}                   255.255.255.255
${Shared Folder Path}       \\\\10.160.213.86\\M2_Automation\\SM Data

# SM Installation parameters
${SM Installer Path}        C:\\DropFolder\\Release
${PCI Installer Path}       C:\\DropFolder\\PCI_Folder\\release
${SM Domain Username}       SMAutomation\\AlarisAdmin
${DB Server}                SMAutoVM2
${SM Domain Password}       \$ecureC0re\@2018
${SM DB Admin Username}     SMAutomation\\CFNLocaladmin

# SSH Connection parameters
${SSH Username}             cfnlocaladmin
${SSH Password}             $ecureC0re#13579
${SM DropFolder}            C:\\M2_Automation\\DropFolder

# PCU Simulator parameters
${Number of Devices}        2
${Current number of CQI Logs}   0
${Cursor}                   None
${PCU DLLs Src}             ${SM DropFolder}\\output\\PCUSimulator
${PCU DLLs Dest}            ${Workspace}\\Libraries\\PCU_Simulator\\include-net

# Jenkins Setup parameters
${Logs Destination}         ${Jenkins Home}\\DeploymentResults-Prod
${SSH Logs Destination}     ../../Program Files (x86)/Jenkins/workspace/DeploymentResults-Prod
${Remote Copy Folder}       C:\\copyresult

# Results Collection parameters
${Prepare VM Results}       ${Jenkins Home}\\Prod 01 - Prepare\\Results
${Prereq Install Results}   ${Jenkins Slave Home}\\Prod 02 - Install Prerequisites\\Results
${Configure VM Results}     ${Jenkins Home}\\Prod 03 - Configure VM\\Results
${Install SM Results}       ${Jenkins Slave Home}\\Prod 04 - Install SM\\Results
${Smoke Test Results}       ${Jenkins Slave Home}\\Prod 05 - Smoke\\Results
${RDP Session Start}        /job/Start%20Smoke%20Test%20Session/buildWithParameters?RDP_File=
${RDP Session End}          /job/Start%20Smoke%20Test%20Session/lastBuild/stop

# Wireless Package parameters
${Deployment Group Name}    DG1
${Package Password}         !1Carefusion

# PCI Prerequisites Parameters
${Domain Name}               SMAutomation
${PSEXEC batch Path}         C:\\RobotTests\\Resources\\BatchFiles\\PostConfiguration.bat