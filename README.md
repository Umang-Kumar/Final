# Face_recognition_webapp, "AtEase"
 A Face detection based attendance system, made during Microsoft Engage Mentorship 2022.

 So, basically this face detection based attention system finds it's usage in traditional offline classes, where a lot of time and effort is wasted in marking attendance   of students/pupils. This web application can be used by an individual who wishes to save his time and energy, focusing on what is important to him and his pupils.
 
 The tech-stack which I used in this project are:
  1. Flask (Python Framework)
  2. HTML/CSS/JS
  3. face-api.js for face recognition
  4. MongoDB
 
 Starting with a beautiful landing page, the user heads next to a login portal which is well secured thanks to the SHA-256 encryption. After successful login, Admin gets into his den which is a very simple Dashboard, three cards direct user to three different functionalities of the website.
  1. Add a student/pupil
  2. Take Attendance
  3. Gallery
 
1. The add student endpoint is a page where the admin selects a photo of student whom face is to be recognized and marked. After selecting you also see a preview in case you selected a wrong image, add his roll no. and name in the specified format and submit. That's all.
2. Take Attendance is pretty self-explanatory. This endpoint takes some time to switch on as it has to load face-api models, but after that it's smooth as butter. Switches on your webcam and takes note of students passing right past it. When you're done just submit it and a csv file of all the pupils with their state being true or false is generated in static/Attendances folder.
3. Gallery as the name suggests is an endpoint where you keep track of all your pupils.
