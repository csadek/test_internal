*** Settings ***
Documentation          This resource file demonstrates executing commands on a remote machine
...                    and putting folders in it.

Library                SSHLibrary
Library                ArchiveLibrary
Library                OperatingSystem
Library                String
Library                ../Libraries/SourceCopyLibrary.py


*** Keywords ***
Open Connection And Log In
   [Arguments]    ${ServerIP}   ${ServerUsername}   ${ServerPassword}
   Open Connection      ${ServerIP}   port=22     timeout=10 minutes
   sleep                30s
   Login                ${ServerUsername}    ${ServerPassword}

Extract SM Installation Files
   ${Build File Name}=  OperatingSystem.list files in directory            ${SM DropFolder}   ${Build File Pattern}
   Extract Zip File     ${SM DropFolder}\\${Build File Name[0]}      dest=${SM DropFolder}
   ${temp}=   fetch from right    ${Build File Name[0]}   ${Build Version Prefix}
   ${Build File version}=   fetch from left  ${temp}      .zip
   set suite metadata   SM Build version    ${Build File version}
   sleep                5s
   Remove File          ${SM DropFolder}\\${Build File Name[0]}

Extract PCI Installation Files
   ${PCI File Name}=    OperatingSystem.list files in directory            ${SM DropFolder}   ${PCI File Pattern}
   Extract Zip File     ${SM DropFolder}\\${PCI File Name[0]}      dest=${SM DropFolder}\\PCI_Folder
   ${temp}=   fetch from right  ${PCI File Name[0]}     ${PCI Version Prefix}
   ${PCI File version}=     fetch from left  ${temp}     .zip
   set suite metadata   PCI Build version   ${PCI File version}
   sleep                5s
   Remove File          ${SM DropFolder}\\${PCI File Name[0]}

Copy Extracted Files To VM
   put directory        ${SM DropFolder}           ${SM Destination}          recursive=True

Copy Solution Files to VM
   put directory        ${Workspace}     ${Remote Workspace}    recursive=True

Copy Smoke Tests To VM10
    put directory       ${Workspace}     ${Client Remote Workspace}      mode=0777    recursive=True

Load PCU DLLs
    create directory    ${PCU DLLs Dest}
    copy files          ${PCU DLLs Src}\\*.dll       ${PCU DLLs Dest}