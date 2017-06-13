*** Settings ***
Documentation       This Test Suite contains a set of test cases responsible for installing PCI Application,
...                 SQL Server and Domain Controller. A server restart is expected after the last test case.

Resource            ../Resources/Config/${Config}
Library             ../Libraries/WhiteFramework/PCIWhiteInstallationLibrary.py
Library             ../Libraries/PrerequisitesLibrary.py


*** Test Cases ***
Install PCI application
    [Tags]      PCIInstallation
    log to console          \n| Installing dependencies
    install dependencies
    log to console          | Starting PCI Installation
    ${build_name} =  get the build name          ${PCI Installer Path}
    start installation at   ${PCI Installer Path}\\${build_name}
    Then The installer should open
    Then Ensure the net framework is installed
    click Install on main screen
    click Ok on completion screen

Install SQL Server
    [Tags]      SQLInstallation
    log to console                      \n| Starting SQL installation
    install sql server                  ${CFN tool Path}      ${SQL Key}
    verify sql server installation      ${DB Server}

Create The local domain controller
    [Tags]      DomainCreation
    log to console                      \n| Disabling restart flag
    Disable Restart Flag                ${CFN tool Path}
    log to console                      | Creating local domain controller
    create local domain controller      ${CFN tool Path}      ${Domain Name}