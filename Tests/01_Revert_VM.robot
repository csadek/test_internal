*** Settings ***
Documentation   This test reverts and starts the VM on which the SM will be installed.

Resource        ../Resources/Config/${Config}
Resource        ../Resources/Config/Client/${ClientVM}
Resource        ../Resources/copy_resource.robot
Resource        ../Resources/collect_results.robot
Library         ../Libraries/Selenium/vCommanderLibrary.py

Suite Setup     Clean Logs Folders

*** Test Cases ***
Extract SM Files & Copy PCU DLLs
    Extract SM Installation Files
    Load PCU DLLs

Extract PCI Files
    [Tags]      PCI
    Extract PCI Installation Files

Revert VM
    log to console                  \n| Starting
    Open Browser To Login Page      ${Revert Browser}      ${Login URL}
    Login To vCommander             ${Login Username}   ${Login Password}
    Select VM                       ${VM Name}
    Revert And Start Selected VM    ${Snapshot}
    Close The Browser