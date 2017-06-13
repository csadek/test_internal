*** Settings ***
Documentation   This Test Suite contains the Test Cases responsible for smoke testing of SM.

Resource        ../Resources/Config/${Config}
Resource        ../Resources/Config/Client/${ClientVM}
Resource        ../Resources/pcu_smoke_tests_resource.robot
Library         ../Libraries/PCU_Simulator/PCUConnectionLibrary.py
Library         ../Libraries/Selenium/DataSetDeploymentLibrary.py
Library         ../Libraries/Selenium/WirelessPackageDeploymentLibrary.py
Library         ../Libraries/Selenium/AssigningPermissionLibrary.py

Suite Setup     Run Keywords            End Smoke Test Session
...             AND                     Start Smoke Test Session
...             AND                     Create Facility And Add IP Address Range
Suite Teardown  End Smoke Test Session

Metadata        Browser             ${Test Browser}
Metadata        SM Server           https://${Server IP}/SystemsManager/
Metadata        PCU Version         ${Device Version}
Metadata        Dataset Folder      ${Shared Folder Path}

*** Test Cases ***
PCU Simulator Connect and Disconnect
    [Tags]    enabled
    log to console                          \n| Starting
    Set PCU Connection Parameters           ${Server IP}   ${Server Port}    ${AES Key}
    log to console                          | Connecting ${Number of Devices} PCUs with version: ${Device Version}
    Start PCU Simulator                     ${Number of Devices}    ${Device Version}
    log to console                          | Verifying PCUs are connected
    Verify PCUs Are Connected
    log to console                          | Disconnecting PCUs
    Disconnect PCUs
    log to console                          | Verifying PCUs are disconnected
    Verify PCUs Are Disconnected
    Clear PCU List

Import User And Assign Permission
    [Tags]  UI  enabled
    log to console              \n| Navigating to manage users page
    open browser and login then navigate to manage users page  ${Test Browser}     ${Server IP}   ${Server Username}   ${Server Password}
    log to console              | Importing user: ${New User ID}
    import user    ${New User ID}
    end assign permission test

Manage Dataset with Authorized Facility user
    [Tags]  UI  enabled
    log to console              \n| Navigating to data sets page
    open browser and login then navigate to manage data sets page     ${Test Browser}   ${Server IP}    ${New User ID}    ${New User Password}
    then the user should be authorized to access
    end data set management test

Remove Permission And Manage Dataset with non Authorized Facility user
    [Tags]  UI  enabled
    log to console              \n| Navigating to manage users page
    open browser and login then navigate to manage users page     ${Test Browser}   ${Server IP}    ${Server Username}    ${Server Password}
    sleep           3s
    remove permission  ${New User ID}
    close web browser
    login with non authorized facility user then navigate to manage data sets page     ${Test Browser}   ${Server IP}    ${New User ID}    ${New User Password}
    then the user should not be authorized to access
    end data set management test

Import Dataset and Activate with Admin user
    [Tags]  UI  enabled
    log to console              \n| Navigating to data sets page
    open browser and login then navigate to manage data sets page     ${Test Browser}   ${Server IP}    ${Server Username}    ${Server Password}
    sleep          3s
    log to console              | Uploading & deploying data sets
    upload and deploy data sets    ${Shared Folder Path}    ${Number of Devices}     ${Device Version}   ${Server IP}    ${Server Port}    ${AES Key}
    sleep           3s
    end data set management test

Import Wireless Package and Deploy
    [Tags]  UI  enabled
    log to console              \n| Navigating to deployment groups page
    open browser and login then navigate to manage deployment groups page   ${Test Browser}   ${Server IP}    ${Server Username}    ${Server Password}
    sleep           3s
    log to console              | Creating deployment group: ${Deployment Group Name}
    create deployment group     ${Deployment Group Name}
    sleep           3s
    log to console              | Importing wireless package
    import wireless package and deploy      ${Shared Folder Path}  ${Facility Name}    ${Deployment Group Name}     ${Package Password}     ${Number of Devices}    ${Device Version}   ${Server IP}   ${Server Port}    ${AES Key}
    end wireless package management test


Verify CQI Log count in CQI Database
    [Tags]    enabled
    log to console                      \n| Starting
    sleep   40s
    log to console                      | Opening DB connection
    Create a database connection with   CQI
    Get the current number of CQI Logs
    log to console                      | Connecting PCUs
    Set PCU Connection Parameters               ${Server IP}   ${Server Port}    ${AES Key}
    Start PCU Simulator                         ${Number of Devices}    ${Device Version}
    Verify PCUs Are Connected
    sleep  10s
    log to console                      | Verifying correct count of logs
    Then verify that the correct number of CQI logs is collected by Systems Manager
    Disconnect PCUs
    Clear PCU List
    Close the open database connection

Verify CQI Log set count in Infusion Database
    [Tags]    enabled
    log to console                      \n| Starting
    sleep   30s
    log to console                      | Opening DB connection
    Create a database connection with   InfusionOLTP
    Get the current number of CQI Log Sets
    log to console                      | Connecting PCUs
    Set PCU Connection Parameters               ${Server IP}   ${Server Port}    ${AES Key}
    Start PCU Simulator                         ${Number of Devices}    ${Device Version}
    Verify PCUs Are Connected
    sleep  10s
    log to console                      | Verifying correct count of logs
    Then verify that the correct number of CQI log Sets is collected by Systems Manager     ${Original row count}    ${Number of Devices}
    Disconnect PCUs
    Clear PCU List
    Close the open database connection

Verify CQI Log are not overwritten in CQI Database
    [Tags]    enabled
    log to console                      \n| Starting
    sleep   40s
    log to console                      | Opening DB connection
    Create a database connection with   CQI
    Get the current number of CQI Logs
    log to console                      | Connecting PCUs
    Set PCU Connection Parameters               ${Server IP}   ${Server Port}    ${AES Key}
    Start PCU Simulator                         ${Number of Devices}    ${Device Version}
    Verify PCUs Are Connected
    sleep  10s
    log to console                      | Verifying correct count of logs
    Then verify that the correct number of CQI logs is collected by Systems Manager
    Disconnect PCUs
    Clear PCU List
    sleep   20s
    Get the current number of CQI Logs
    Set PCU Connection Parameters               ${Server IP}   ${Server Port}    ${AES Key}
    Start PCU Simulator                         ${Number of Devices}    ${Device Version}
    Verify PCUs Are Connected
    sleep  10s
    Then verify that the correct number of CQI logs is collected by Systems Manager
    Disconnect PCUs
    Clear PCU List
    Close the open database connection

Verify CQI Log are not overwritten in Infusion Database
    [Tags]    enabled
    log to console                      \n| Starting
    sleep   30s
    log to console                      | Opening DB connection
    Create a database connection with   InfusionOLTP
    Get the current number of CQI Log Sets
    log to console                      | Connecting PCUs
    Set PCU Connection Parameters               ${Server IP}   ${Server Port}    ${AES Key}
    Start PCU Simulator                         ${Number of Devices}    ${Device Version}
    Verify PCUs Are Connected
    sleep  10s
    log to console                      | Verifying correct count of logs
    Then verify that the correct number of CQI log Sets is collected by Systems Manager     ${Original row count}    ${Number of Devices}
    Disconnect PCUs
    Clear PCU List
    sleep   20s
    Get the current number of CQI Log Sets
    Set PCU Connection Parameters               ${Server IP}   ${Server Port}    ${AES Key}
    Start PCU Simulator                         ${Number of Devices}    ${Device Version}
    Verify PCUs Are Connected
    sleep  10s
    Then verify that the correct number of CQI log Sets is collected by Systems Manager     ${Original row count}    ${Number of Devices}
    Disconnect PCUs
    Clear PCU List
    Close the open database connection

Smoke Tests Data Cleanup
    [Tags]  enabled
    log to console          \n| Removing facilities
    open browser and login then navigate to manage network page   ${Test Browser}     ${Server IP}   ${Server Username}   ${Server Password}
    delete facilities
    log to console          | Removing wireless packages
    open browser and login then navigate to manage deployment groups page  ${Test Browser}     ${Server IP}   ${Server Username}   ${Server Password}
    delete wireless packages
