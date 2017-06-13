*** Settings ***
Resource                    config.robot
*** Variables ***
# Test Execution parameters
${Test Browser}             Chrome
${VM Name}                  135977-02_Win2012R2_UnifiedCore_1.1-002-mohab.ayman@carefusion.com
${Snapshot}                 Ready for Silent Install

# Systems Manager parameters
${Server IP}                10.160.212.25
${Server Name}              SMAuto-Staging.Autostaging.Local
${Server Port}              3613
${AES Key}                  3D 29 DD 5C F5 69 46 17 61 D9 1B 70 EE 80 48 63
${Server Username}          alarisadmin
${Server Password}          $ecureC0re@2018
${Trusted Domain}           AutoStaging.Local
${DB User UserName}         smautouser
${DB User Password}         password_123456

# Device Parameters
${Device Version}           12.1.0.0

# Facility Creation parameters
${Facility Name}            SMFTest
${Facility Desc}            Test the automation of Adding Facility
${IP Start}                 1.0.0.0
${IP End}                   255.255.255.255
${Shared Folder Path}       \\\\10.160.213.86\\M2_Automation\\SM Data

# SM Installation parameters
${SM Installer Path}        C:\\DropFolder-Staging\\Release
${PCI Installer Path}       C:\\DropFolder-Staging\\PCI_Folder\\release
${SM Domain Username}       AutoStaging\\AlarisAdmin
${SM Domain}                AutoStaging
${DB Server}                SMAuto-Staging
${SM Domain Password}       \$ecureC0re\@2018
${SM DB Admin Username}     AutoStaging\\CFNLocaladmin
${SM Cert File}             C:\\Certs\\SMAuto-Staging.Autostaging.Local.pfx
${SM Cert Password}         cBB9xk8yU$S_B@X6+GvD|jY

# SSH Connection parameters
${SSH Username}             cfnlocaladmin
${SSH Password}             $ecureC0re#13579
${SM DropFolder}            C:\\M2_Automation\\DropFolder-Staging

# PCU Simulator parameters
${Number of Devices}        2
${Current number of CQI Logs}   0
${Cursor}                   None
${PCU DLLs Src}             ${SM DropFolder}\\output\\PCUSimulator
${PCU DLLs Dest}            ${Workspace}\\Libraries\\PCU_Simulator\\include-net

# Jenkins Setup parameters
${Logs Destination}         ${Jenkins Home}\\DeploymentResults-Staging
${SSH Logs Destination}     ../../Program Files (x86)/Jenkins/workspace/DeploymentResults-Staging
${Remote Copy Folder}       C:\\copyresult

# Results Collection parameters
${Prepare VM Results}       ${Jenkins Home}\\Staging 01 - Prepare\\Results
${Prereq Install Results}   ${Jenkins Slave Home}\\Staging 02 - Install Prerequisites\\Results
${Configure VM Results}     ${Jenkins Home}\\Staging 03 - Configure VM\\Results
${Install SM Results}       ${Jenkins Slave Home}\\Staging 04 - Install SM\\Results
${Smoke Test Results}       ${Jenkins Slave Home}\\Staging 05 - Smoke\\Results
${RDP Session Start}        /job/Staging%20-%20Smoke%20Session/buildWithParameters?RDP_File=
${RDP Session End}          /job/Staging%20-%20Smoke%20Session/lastBuild/stop

# Wireless Package parameters
${Deployment Group Name}    DG1
${Package Password}         $ecureC0re@2018

# PCI Prerequisites Parameters
${Domain Name}               AutoStaging
${PSEXEC batch Path}         C:\\RobotTests\\Resources\\BatchFiles\\PostConfiguration.bat