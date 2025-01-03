First install DJANGO 

![image](https://github.com/user-attachments/assets/ab7b47cf-a7c2-44d4-81ac-4edd5f58301b)

then

enter the following directory and run this command
![image](https://github.com/user-attachments/assets/c8bf52ea-7942-4d18-8540-7ad6fdc0dc96)

this will start the app

urls.py : calls the function in views.py file upon hitting the url like in this case "http://127.0.0.1:8000/all_emp/" it calls all_emp function in views.py
views.py : it manages and manipulate the B-tree, in project2.py file, views.py also serialize and deserialize the data
tree.txt : it stores the data in the form of text, data is serialized into and deserialize from it using views.py
project2.py : it contains the b-tree, backbone of the project
