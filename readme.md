- Clone the repo and go to project root
- Create a .env file and copy the contents of .env.example file, assign values if necessary
- Both docker and virtualenv can be used to set up the interpreter
- To use venv
    ```python -m venv venv```(might be python3 for some), then activate the venv
- To use docker run ```docker compose up --build``` then create static_local directory, run ```python manage.py collectstatic```
- Install required packages ```pip install -r requirements.txt```
- For venv, run server with ```python manage.py runserver```
- A postman collection has been added to the repository