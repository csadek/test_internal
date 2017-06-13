*** Settings ***
Documentation     This resource file contains the custom Robot Keywords and Variables, necessary for executing
...               PCU smoke tests

Library           RequestsLibrary
Library           ../Libraries/Selenium/CreateFacilityLibrary.py
Library           ../Libraries/SMDBLibrary.py     ${Server IP}     ${DB User UserName}    ${DB User Password}


*** Variables ***
${Cursor}                       None
${Original row count}           0
${New row count}                0

*** Keywords ***
Create a database connection with
    [Arguments]  ${DB Name}
    ${Cursor}=      connect to db   ${DB Name}
    set suite variable      ${Cursor}

Get the current number of CQI Logs
    ${Original row count}=   row count  dbo.Sequence       ${Cursor}
    set suite variable      ${Original row count}
    log     Current number of CQI Logs is: ${Original row count}

verify that the correct number of CQI logs is collected by Systems Manager
    verify the new row count against the original row count     ${Original row count}    ${Number of Devices}

Get the current number of CQI Log Sets
    ${Original row count}=   row count  Infusion.InfusionMonitorControllerCQILogEntry       ${Cursor}
    set suite variable      ${Original row count}
    log     Current number of CQI Log Sets is: ${Original row count}

Start Smoke Test Session
    Create Session      Jenkins     ${Jenkins URL}
    post request        Jenkins     ${RDP Session Start}${Client RDP File}

End Smoke Test Session
    Create Session      Jenkins     ${Jenkins URL}
    post request        Jenkins     ${RDP Session End}

Create Facility And Add IP Address Range
    [Tags]  UI  enabled
    sleep           15s
    log to console                      Starting Suite Setup - Creating facility & IP address range
    log to console                      \n| Navigating to manage network page
    open browser and login then navigate to manage network page   ${Test Browser}     ${Server IP}   ${Server Username}   ${Server Password}
    sleep          3s
    log to console                      | Adding facility: ${Facility Name}
    add facility    ${Facility Name}    ${Facility Desc}   ${AES Key}
    log to console                      | Adding IP Range from ${IP Start} to ${IP End}
    add ip address range    ${IP Start}     ${IP End}
    sleep           3s
    end create facility test