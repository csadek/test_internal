*** Settings ***
Documentation     This resource file executes commands to collect SM deployment results.
Library           SSHLibrary
Library           ArchiveLibrary
Library           OperatingSystem
Library           Collections


*** Keywords ***

# 01 - Revert VM
Collect VM Revert Results
    @{files}=               OperatingSystem.List Files In Directory    ${Prepare VM Results}    ${Revert Log Pattern}
    ${lastModifiedFile}=    Get From List    ${files}    0
    ${time1}=               Get Modified Time    ${Prepare VM Results}\\${lastModifiedFile}
    : FOR                   ${file}    IN    @{files}
    \                       ${time}    Get Modified Time    ${Prepare VM Results}\\${file}
    \                       ${lastModifiedFile}    Set Variable If    '${time1}' <= '${time}'    ${file}    ${lastModifiedfile}
    \                       ${time1}    Set Variable If    '${time1}' <= '${time}'    ${time}    ${time1}
    copy file               ${Prepare VM Results}\\${lastModifiedFile}    ${Logs Destination}

# 02 - Copy Installation Files
Collect Installation Files Copy Results
    @{files}=               OperatingSystem.List Files In Directory    ${Prepare VM Results}    ${Copy Files Log Pattern}
    ${lastModifiedFile}=    Get From List    ${files}    0
    ${time1}=               Get Modified Time    ${Prepare VM Results}\\${lastModifiedFile}
    : FOR                   ${file}    IN    @{files}
    \                       ${time}    Get Modified Time    ${Prepare VM Results}\\${file}
    \                       ${lastModifiedFile}    Set Variable If    '${time1}' <= '${time}'    ${file}    ${lastModifiedfile}
    \                       ${time1}    Set Variable If    '${time1}' <= '${time}'    ${time}    ${time1}
    copy file               ${Prepare VM Results}\\${lastModifiedFile}    ${Logs Destination}

# 03 - Install Prerequisites
Collect Prerequisites Installation Results
    @{files}=               OperatingSystem.List Files In Directory     ${Prereq Install Results}       ${Prereq Log Pattern}
    ${lastModifiedFile}=    Get From List    ${files}    0
    Open Connection         ${Jenkins IP}    port=22    timeout=10 minutes
    sleep                   10s
    Login                   ${Host SSH Username}    ${Host SSH Password}
    SSHLibrary.Put File     ${Prereq Install Results}\\${lastModifiedFile}        ${SSH Logs Destination}\\${lastModifiedFile}
    close connection

# 04 - Post Domain Configuration
Collect Post Domain Configuration Results
    @{files}=               OperatingSystem.List Files In Directory    ${Configure VM Results}    ${Configure Log Pattern}
    ${lastModifiedFile}=    Get From List    ${files}    0
    ${time1}=               Get Modified Time    ${Configure VM Results}\\${lastModifiedFile}
    : FOR                   ${file}    IN    @{files}
    \                       ${time}    Get Modified Time    ${Configure VM Results}\\${file}
    \                       ${lastModifiedFile}    Set Variable If    '${time1}' <= '${time}'    ${file}    ${lastModifiedfile}
    \                       ${time1}    Set Variable If    '${time1}' <= '${time}'    ${time}    ${time1}
    copy file               ${Configure VM Results}\\${lastModifiedFile}    ${Logs Destination}

# 05 - Create SQL and Domain Logins & 06 - SM Installation
Collect SM Installation Results
    @{logins files}=            OperatingSystem.List Files In Directory     ${Install SM Results}       ${Logins Log Pattern}
    ${lastLoginsFile}=          Get From List    ${logins files}    0
    @{install files}=           OperatingSystem.List Files In Directory     ${Install SM Results}       ${SM Install Log Pattern}
    ${lastInstallFile}=         Get From List    ${install files}   0
    Open Connection             ${Jenkins IP}    port=22    timeout=10 minutes
    sleep                       10s
    Login                       ${Host SSH Username}    ${Host SSH Password}
    SSHLibrary.Put File         ${Install SM Results}\\${lastLoginsFile}        ${SSH Logs Destination}\\${lastLoginsFile}
    SSHLibrary.Put File         ${Install SM Results}\\${lastInstallFile}        ${SSH Logs Destination}\\${lastInstallFile}
    close connection

# 07 - SM Smoke Tests
Collect SM Testing Results
    @{smoke files}=             OperatingSystem.List Files In Directory     ${Smoke Test Results}       ${Smoke Log Pattern}
    ${lastModifiedFile}=        Get From List                               ${smoke files}    0
    ${time1}=                   Get Modified Time                           ${Smoke Test Results}\\${lastModifiedFile}
    : FOR                       ${file}    IN    @{smoke files}
    \                           ${time}    Get Modified Time    ${Smoke Test Results}\\${file}
    \                           ${lastModifiedFile}    Set Variable If    '${time1}' <= '${time}'    ${file}    ${lastModifiedfile}
    \                           ${time1}    Set Variable If    '${time1}' <= '${time}'    ${time}    ${time1}
    Open Connection             ${Jenkins IP}    port=22    timeout=10 minutes
    sleep                       10s
    Login                       ${Host SSH Username}    ${Host SSH Password}
    SSHLibrary.Put File         ${Smoke Test Results}\\${lastModifiedFile}        ${SSH Logs Destination}\\${lastModifiedFile}
    close connection

Clear Folder
    [Arguments]    ${path}
    @{folders}=      OperatingSystem.List Directories In Directory   ${path}
    : FOR   ${folder}   IN  @{folders}
    \       remove directory    ${path}\\${folder}  recursive=True
    Remove Files    ${path}\\*

Clean Logs Folders
    create directory    ${Logs Destination}
    Clear Folder        ${Logs Destination}
    create directory    ${Remote Copy Folder}
    Clear Folder        ${Remote Copy Folder}




