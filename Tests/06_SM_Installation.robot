*** Settings ***
Documentation     This Test Suite installs the SM on the server VM.

Resource        ../Resources/Config/${Config}
Library         ../Libraries/SMSilentInstall.py


*** Test Cases ***
SM Silent Installation
    [Tags]    SMInstall
    log to console              \n| Starting
    extract MSI installer       ${SM Installer Path}
    set domain name             ${SM Domain}
    set credentials             ${Server Username}      ${Server Password}
    set sql server              ${DB Server}
    set certificate             ${SM Cert File}        ${SM Cert Password}
    set installation parameters
    run SM installation
    Then verify SM is installed
    install certificate
