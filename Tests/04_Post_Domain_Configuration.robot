*** Settings ***
Documentation       This Test Suite confugres the server VM after domain controller installation.

Resource            ../Resources/Config/${Config}
Library             ../Libraries/PostDomainConfigurationLibrary.py
Library             ../Libraries/SourceCopyLibrary.py


*** Test Cases ***
Configure the installation node
    [Tags]      PostDomainCreation
    log to console                                  \n| Waiting 6 minutes for VM to finish the restarts
    sleep                                           360s
    Check the node status                           ${Server IP}
    log to console                                  | Configuring the VM
    Configure the machine after domain creation     ${PSEXEC tool Path}     ${Server IP}    ${SSH Username}    ${SSH Password}   ${PSEXEC batch Path}

Wait For Connection And Log In
    sleep                   60s
    verify connection       ${Server IP}    ${Server Username}    ${Server Password}