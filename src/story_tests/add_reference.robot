*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References



*** Test Cases ***
Single Article Reference Should Be Added
    Add Article Reference   ${AUTHOR}  ${TITLE}  ${YEAR}  ${JOURNAL}
    Click Button  All references
    Verify Article Reference   ${AUTHOR}  ${TITLE}  ${JOURNAL}  ${YEAR}

Two Article References Should Be Added
    Add Article Reference   ${AUTHOR}  ${TITLE}  ${YEAR}  ${JOURNAL}
    Add Article Reference   ${AUTHOR}  Parempi Artikkeli  2022  ${JOURNAL}
    Click Button  All references
    Verify Article Reference   ${AUTHOR}  ${TITLE}  ${JOURNAL}  ${YEAR}
    Verify Article Reference   ${AUTHOR}  Parempi Artikkeli  ${JOURNAL}  2022
    Page Should Not Contain  vol.
    Page Should Not Contain  no.
    Page Should Not Contain  page(s)
    Page Should Not Contain  month:
    Page Should Not Contain  notes:

Article Reference With Voluntary Info Should Be Added
    Add Article Reference   ${AUTHOR}  Paras Artikkeli  2022  ${JOURNAL}  3  2  142  5  Muistiin
    Click Button  All references
    Verify Article Reference   ${AUTHOR}  Paras Artikkeli  ${JOURNAL}  2022  3  2  142  5  Muistiin

Single Book Reference Should Be Added
    Add Book Reference   ${AUTHOR}  ${EDITOR}  Latexin ritarien tarinoita   ${PUBLISHER}  ${YEAR}  
    Click Button  All references
    Verify Book Reference   ${AUTHOR}  ${EDITOR}  Latexin ritarien tarinoita   ${PUBLISHER}  ${YEAR} 

Two Book References Should Be Added
    Add Book Reference   ${AUTHOR}  ${EDITOR}  Latexin ritarien klassikot  ${PUBLISHER}  ${YEAR} 
    Add Book Reference   ${AUTHOR}  ${EDITOR}  Latexin ritarien tarinoita  ${PUBLISHER}  2022 
    Click Button  All references
    Verify Book Reference   ${AUTHOR}  ${EDITOR}  Latexin ritarien klassikot  ${PUBLISHER}  ${YEAR} 
    Verify Book Reference   ${AUTHOR}  ${EDITOR}  Latexin ritarien tarinoita  ${PUBLISHER}  2022 
    Page Should Not Contain  vol.
    Page Should Not Contain  no.
    Page Should Not Contain  page(s)
    Page Should Not Contain  month:
    Page Should Not Contain  notes:

Book Reference With Voluntary Info Should Be Added
    Add Book Reference   ${AUTHOR}  ${EDITOR}  Latexin ritarien klassikot  ${PUBLISHER}  2022  3  2  142  5  Muista tämä
    Click Button  All references
    Verify Book Reference   ${AUTHOR}  ${EDITOR}  Latexin ritarien klassikot  ${PUBLISHER}  2022  3  2  142  5  Muista tämä

Reference can be added with DOI
    Add DOI   ${DOI}
    Click Button  All references
    Verify Article Reference   Alex Gaudeul  Do Open Source Developers Respond to Competition? The LATEX Case Study  Review of Network Economics  2007  6  2  None  1