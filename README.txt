Todolist is a web application for creating and tracking tasks both in a group and individually. Developed on Django Rest Framework. Uses Telegram bot to create tasks.
Frontend is developed by SkyPro and is used from an image on DockerHub.

Dependencies:
Python v3.10
Docker

Using.
You must have Python and Docker installed on your system.

1. Clone the repository
from the page:
https://github.com/Eugeny-ga/Todolist.git
or with the command:
git clone git@github.com:Eugeny-ga/Todolist .git

2. Create a .env file and put it in the root of the project.

Examples of parameters:
SECRET_KEY=<secret key for django app>
DEBUG=0
DB_ENGINE=django.db.backends.postgresql
DB_HOST=postgres
DB_PORT=5432
DB_NAME=<Postgres DB name>
DB_USER=<Postgres DB username>
DB_PASSWORD=<Postgres DB password>
VK_ID=<VK app id>
VK_KEY=<VK secret key>
TG_TOKEN=<telegram bot token>

3. Launch Docker containers with the docker-compose command
: docker-compose up -d --build

4. Go to the page http://localhost/


Functionality:
1. User registration in the usual way and via VK.
2. Users can create personal boards, goal categories, goals themselves and comments on them.
You can edit the description, deadlines, priorities, statuses for goals.
3. You can create boards that other users will have access to. Other users can edit goals, or only read them.


Telegram bot.
In the connected bot, you can get a verification code and link it to your account in your personal account. After verification, users will be able to use the bot to read and create their own and common goals.

API Schema
Swagger UI is used
http://localhost/api/schema/swagger-ui/

Testing
The tests are located in the root folder of the project in the tests folder. They are launched from the console using the command:
pytest