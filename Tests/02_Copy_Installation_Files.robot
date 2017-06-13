*** Settings ***
Documentation   This test accomplishes the following:
...             1- Copy SM & PCI installation files to server VM.
...             2- Copy solution folder to server and client VMs.

Resource        ../Resources/Config/${Config}
Resource        ../Resources/Config/Client/${ClientVM}
Resource        ../Resources/copy_resource.robot
Resource        ../Resources/collect_results.robot


*** Test Cases ***
Copy Installation Files
    log to console                  \n| Starting
    verify connection               ${Server IP}    ${SSH Username}    ${SSH Password}
    log to console                  | Opening connection to ${Server IP}
    Open Connection And Log In      ${Server IP}    ${SSH Username}    ${SSH Password}
    log to console                  | Copying Files
    Copy Extracted Files To VM
    Copy Solution Files to VM
    close connection

Copy Workspace To Client VM
    log to console                  \n| Starting
    verify connection               ${Client VM IP}    ${Client SSH Username}    ${Client SSH Password}
    log to console                  | Opening connection to ${Client VM IP}
    Open Connection And Log In      ${Client VM IP}    ${Client SSH Username}    ${Client SSH Password}
    log to console                  | Copying Files
    Copy Smoke Tests To VM10
    close connection

Empty Drop Folder
    Clear Folder                    ${SM DropFolder}

