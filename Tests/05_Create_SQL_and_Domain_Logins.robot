*** Settings ***
Documentation       This Test Suite creates SQL Logins and new domain user login.

Resource        ../Resources/Config/${Config}
Library         ../Libraries/PrerequisitesLibrary.py
Library         ../Libraries/Selenium/AssigningPermissionLibrary.py


*** Test Cases ***
SQL Logins creation and server role assignment
    [Tags]    SQLLogins
    log to console                  \n| Starting
    Create SQL Login from Domain    ${Domain Name}
    Restart SQL Service

Create New Domain User
    log to console                      \n| Starting
    create user in active directory     ${Server Name}    ${Server Username}      ${Server Password}     ${Domain Name}    ${New User Name}   ${New User Password}