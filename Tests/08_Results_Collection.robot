*** Settings ***
Documentation       This script collects the test results for SM deployment and smoke testing and emails them.

Resource            ../Resources/Config/${Config}
Resource            ../Resources/Config/Client/${ClientVM}
Resource            ../Resources/collect_results.robot

Suite Teardown      Close All Connections


*** Test Cases ***
Clean Logs Folders
    Clear Folder    ${Logs Destination}
    Clear Folder    ${Remote Copy Folder}

Collect Preparation Results
    [Tags]          Preparation
    Collect VM Revert Results
    Collect Installation Files Copy Results

Collect Prerequisites Results
    [Tags]          Prerequisites
    Collect Prerequisites Installation Results

Collect VM Configuration Results
    [Tags]          Configuration
    Collect Post Domain Configuration Results

Collect SM Installation Results
    [Tags]          Installation
    Collect SM Installation Results

Collect Testing Results
    [Tags]          Smoke
    Collect SM Testing Results