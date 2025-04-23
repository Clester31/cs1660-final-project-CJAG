# cs1660-final-project-CJAG
Final project for CS 1660

* Akshitha - Docker / GCP
* Grace - Architecture Diagram / deployment
* Christian - Frontend
* Julie - fASTAPI / python

# Link
https://attendencetracker-280595272990.us-central1.run.app/

# Architecture

![final1660 drawio](https://github.com/user-attachments/assets/c3c5d38e-37a3-4467-8ac5-cadc08879ce8)

# Project Description

* Our group created a class attendance tracker for professors to use to track class attendance on the daily basis.
* Students can access the website by scanning the QR code on the page. They can then log in through the website to have their attendance tracked/updated on the attendance log.
* Our application tracks the student's name along with the time they signed into class.
* As seen in the diagram above, we created a static UI using HTML and CSS. We used Firebase for authentication and the SDK.
* The backend had FastAPI, which handled the logic and connected the requests and data from the frontend to the backend.
* Firestore is where all of our data is collected, like name, time they signed in, and attendance.
* The JavaScript connects to some of our Google Services and to the frontend of our application through the server.
* We also used the Google ID platform and Google People API to allow students to sign in using their Google accounts.
* Our project uses GitHub Actions to automate the deployment process. It is deployed to Cloud Run on every new push.
  
# Reflection

* While we are happy with our project, if we had more time, we would have implemented functionality to allow professors with multiple classes to track them all.
* We were also thinking of adding a way to check users' identities to prevent any user from posting or altering our site.
* We also would implement funcitonality on the front end so that students that login late would be marked late or absent 
