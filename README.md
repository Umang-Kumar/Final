# Face_recognition_webapp, "AtEase"
 A Face detection based attendance system, made during Microsoft Engage Mentorship 2022.

 So, basically this face detection based attention system finds it's usage in traditional offline classes, where a lot of time and effort is wasted in marking attendance   of students/pupils. This web application can be used by an individual who wishes to save his time and energy, focusing on what is important to him and his pupils.
 
 To get started with this web app clone repository in your desired directory, open app.py file, if you don't have the required modules (most of them are in requirements.txt) install them after every module is installed also see the tech-stack and download MongoDB so that it can store images and csv files. If everything is going well the app will start on your localhost and rest I've described below.
 
 The tech-stack which I used in this project are:
  1. Flask (Python Framework)
  2. HTML/CSS/JS
  3. face-api.js for face recognition
  4. MongoDB
 
 Starting with a beautiful landing page, the user heads next to a login portal which is well secured thanks to the SHA-256 encryption. After successful login, Admin gets into his den which is a very simple Dashboard, three cards direct user to three different functionalities of the website.
  1. Add a student/pupil
  2. Take Attendance
  3. Gallery
 
A) The add student endpoint is a page where the admin selects a photo of student whom face is to be recognized and marked. After selecting you also see a preview in case you selected a wrong image, add his roll no. and name in the specified format and submit. That's all.

B) Take Attendance is pretty self-explanatory. This endpoint takes some time to switch on as it has to load face-api models, but after that it's smooth as butter. Switches on your webcam and takes note of students passing right past it. When you're done just submit it and a csv file of all the pupils with their state being true or false is generated in static/Attendances folder.

C) Gallery as the name suggests is an endpoint where you keep track of all your pupils.

Also , I'm still developing, so will keep improving over time, open to ideas.

Some screenshots to go through:
![Web capture_29-5-2022_18286_127 0 0 1](https://user-images.githubusercontent.com/76547661/170869873-cab125b1-aee9-41fe-bcba-b37676b521bb.jpeg)
![Web ca![Web capture_29-5-2022_183327_127 0 0 1](https://user-images.githubusercontent.com/76547661/170870162-99e5d9d0-2ef7-4eaa-bf8b-fd70bf6ca2db.jpeg)
![Web capture_29-5-2022_183327_127 0 0 1](https://user-images.githubusercontent.com/76547661/170870257-794189d2-1410-47b8-a3d7-a1e02d157730.jpeg)


Arigatōgozaimashita;)
