# SoftDesk

## Menu

* [Installation](#installation-and-execution-using-venv-and-pip)

## Installation and execution using venv and pip

⚠️ Git and Python 3.10+ must be installed first.

1. Clone this repository using `$ git clone https://github.com/Prud-homme/OC_P10.git` (you can also download the code [as a zip file](https://github.com/Prud-homme/OC_P10/archive/refs/heads/main.zip))
2. Move to the OC_P10 root folder with `$ cd OC_P10`
3. Create a virtual environment for the project with 
    * `$ python -m venv env` on windows
    * `$ python3 -m venv env` on macos or linux
4. Activate the virtual environment with 
    * `$ env\Scripts\activate` on windows
    * `$ source env/bin/activate` on macos or linux
5. Install project dependencies with `$ pip3 install -r requirements.txt`
6. Initialize database with
    * `$ python manage.py migrate` on windows
    * `$ python3 manage.py migrate` on macos or linux
7. Run the server with
    * `$ python manage.py runserver` on windows
    * `$ python3 manage.py runserver` on macos or linux

When the server is running after step 6 of the procedure, the Web App can be launch from the URL: [http://localhost:8000](http://localhost:8000 "SoftDesk API").

Steps 1-3 and 5 are only required for initial installation. For subsequent launches of the Web App, you only have to execute steps 4 and 6 from the root folder of the project.

🗒️ *Notes:*

* *To reset the database you can delete db.sqlite3 file and run `$ python manage.py migrate` to create a new empty database*
* *To disable the virtual environment, run: `$ deactivate`.*