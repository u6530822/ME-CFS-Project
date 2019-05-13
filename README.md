# Tech Launcher ME-CFS-Project

# Overview

Medical centres and clinics collect abundant records on patients that can be applied to health and medical research challenges. This is certainly the case with CFS Discovery in Melbourne, who have collected detailed data on ME/CFS patients for almost 20 years. ME/CFS is a mysterious and controversial disease, where Australian scientists are making excellent progress via cross-disciplinary research.

Patient data is stored as individual records, and as such it is very time consuming to physically extract the data for spreadsheets and databases, required for machine-learning and other analyses.

The project is: To automate the extraction of valuable ME/CFS patient data into aggregated form (via spreadsheets is fine), accurately and efficiently. The successful completion of this challenge will accelerate our research efforts towards understanding ME/CFS, by contributing to the construction of anonymous patient databases for pattern recognition interrogation, as well as in support for future biobanks.

# Project Administration
## Timeline
Week 2-3: Requirement gathering and technology assessment/exploration. <br />
Week 4-5: Work on Printed text conversion to digitalized documents.<br />
Week 6-7: Work on Handwritten text conversion to digitalized documents.<br />
Week 8-9: Full round of user acceptance testing and consolidation.<br />
Week 10-12: Reflection and improvements.<br />

# Milestone Chart  
![Capture](https://github.com/u6530822/ME-CFS-Project/blob/master/milestone.PNG)

# Deliverables
•	Modular well-structured code to carry out the following:<br />
o	New process to convert and store printed patient records into PDF and excel sheets. <br />
o	New Process to convert and store hand-written records/notes into PDF and excel sheets<br />
o	Provide an easy to use and intuitive user interface. <br />
o	Allow sufficient space for scalability and further analytic needs. <br />

•	Documentation will be covered in the following:<br />
o	Well commented and modular code. <br />
o	High level documentation on code process in each iteration. <br />
o	A user guide to be handed to the stakeholders at the end of the project.<br />

[Product Backlog](https://drive.google.com/open?id=154SpNfr9QrG_j6Xw1HOSoIcJ5UUipYOH)<br />

## Version control and monitoring.<br />
All work will be tracked in github, and while the project deliverables on a high level will be constantly updated on the project wiki. <br />

# Team
|Member| UID|	Role|	Backup|	Email|
| --- | --- | --- | --- | --- |
|You Li|u6430173|Developer| 	Quality Assurance|	you.li@anu.edu.au|
|Nigel Tee|u6530834|Developer|	Quality Assurance|	nigel.tee@anu.edu.au|
|Chin Hun Young(Spokeperson)|u6530822|Quality Assurance|	Project Manager|	chin.young@anu.edu.au|
|Rufus Raja|u6275198	|Project Manager|	Developer|	rufus.raja@anu.edu.au|

Supervisor and product owner: Brett Lidbury  

## Team's Decision Making Steps
[Decision Making Document](https://drive.google.com/open?id=1iuMgKuiV72ic6ZybAdhszDJW5QMlwO6K)<br />

*Github is open to public for now, will set it to private once we start working on client sensitive materials

# Stakeholders
Our chief client is Dr. Brett Lidbury. We have a slack channel setup and will have weekly connects with him. Our secondary contact is Dr. Alice Richardson. 

# Project Artifacts
[Signed Statement of Work](https://docs.google.com/document/d/1eFEJfMPe0xbD6Jfw6KpZf4wzqcFAI8vjizMkaUJH-Dk/edit?usp=sharing)<br />
[Signed Product Backlog/Acceptance Criteria](https://drive.google.com/open?id=154SpNfr9QrG_j6Xw1HOSoIcJ5UUipYOH)<br />
[Approved DB Fields](https://drive.google.com/file/d/1NbsGXRXQ0QnQ8ItyiEVDQO5VlD8_Rv8t/view?usp=sharing)<br />
[Iteration Tracking](https://drive.google.com/drive/u/1/folders/1c-zunhc9ArRkqTRCivM0X3Kt2iIH-1Nx)<br />

# Communication 
[Slack Channel](https://mecfs-workspace.slack.com/messages/CGPA6LS90/)<br />
[Meeting Minutes](https://drive.google.com/open?id=1PdPVHMijHiBvzMBqYQPptPX4WbBsXGjE)<br />

# Quality Assurance
[Technical Specification](https://drive.google.com/file/d/1xuPRZXNygvWiQU0BOwUbPlI6k1vXGzfA/view?usp=sharing)<br />
[Issue Tracking](https://github.com/u6530822/ME-CFS-Project/issues)<br />
[Feedback Log](https://drive.google.com/open?id=15BJ5XNeOg506WVSW6oJ9KiIewVI6bu0y)<br />
[Testing Summaries](https://drive.google.com/open?id=1GlXRLAL1TPeR7_wVfNAkTnE9Sw4SnoZHDcEf3BC4tjs)<br />

# Support Documentation
[Project Documentation Folder](https://drive.google.com/open?id=1fHtWXQIDxyIFErwrestoyBETrUFVW-Yq)<br />

# Current Progress
#### [Progress Report Folder](https://drive.google.com/drive/u/1/folders/1_xgkb4bs7dScdkAQv_ZJaXaIq126nBvf)<br />
[Latest Report](https://drive.google.com/open?id=1JB9lKHz7MoSZC59oYe-F8u0W19tvWBaK)<br />

# Technical Tools and Constraints
•	Off the shelf tools<br />
  ○ Optical Character Recognition software <br />
<br />
•	implementation from scratch<br />
  ○ Hidden Markov Model<br />
  ○ Neural Network<br />
  ○ Code in Tesseract/TensorFlow<br />
<br />

•	Constraints:<br />
  ○ Training of the model is required<br />
  ○ Sensitive issue related to disclosing patients' data<br />
  
  # Risk Management
  
  ![Capture](https://github.com/u6530822/ME-CFS-Project/blob/master/risk_list.PNG)
  
### Technical Risk
#### Time for the text conversion to be longer than client’s expectation
Likelihood: Unlikely<br />
Consequence: Catastrophic<br />
Priority: High<br />
Solutions: Obtain main stakeholder’s agreement on the time required for conversion to match expectation<br />
#### Limitation of knowledge in handwritten to text conversion
Likelihood: Possible<br />
Consequence: Moderate<br />
Priority: High<br />
Solutions: Obtain main stakeholder’s agreement on the possible removal of feature<br />
#### New record types to be considered apart from existing printed document samples
Likelihood: Certain<br />
Consequence: Major<br />
Priority: High<br /> 
Solutions: Obtain main stakeholder’s agreement on working on these records in a future implementation<br />

### Ethical Risk
#### Data security breach
Likelihood: Possible<br />
Consequence: Catastrophic<br />
Priority: Extreme<br />
Solutions: Access authorisation, multilevel security model in databases & encryption<br />
##### Data Privacy issues
Likelihood: Possible<br />
Consequence: Catastrophic<br />
Priority: Extreme<br />
Solutions: Signed Ethical form, Downgrading results, stakeholder’s agreement on storage method<br />

### Resources risk
#### Members fall sick & Unavailability of members
Likelihood: Possible<br />
Consequence: Minor<br />
Priority: Medium<br />
Solutions: Shadowing teammates, Daily stand-up to update on progress<br />
#### Unforeseen accident
Likelihood: Rare<br />
Consequence: Moderate<br />
Priority: Low<br />
Solutions: Shadowing teammates, Daily stand-up to update on progress<br />



