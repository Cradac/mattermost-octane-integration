# Mattermost-Octane-Client

The Mattermost-Ocatane-Client creates an integration for the communication platform Mattermost to post defects from the lifecycle management tool ALM Octane.

## Delivery

The Client gets delivered as a plain python repository. You need to install some libraries vie PyPi or pip so the server can run. 
You may either use a [Virtual Env](https://docs.python-guide.org/dev/virtualenvs/) which you can install with pip or any container.\
The packages to install are:
- markdownify
- flask

and all the side packages that come with it.


## Deployment

The app should be deployed to a production WSGI server instead of running on the default development server.
To get more information on how to do this go [here](http://flask.pocoo.org/docs/1.0/deploying/). 


## Setup Mattermost Webhooks

1. `Main Menu` or the three lines next to your name
2. Press `Integrations`
3. In the center of the screen click `Incoming Webhooks`
4. Add a new webhook by clicking on `Add Incoming Webhook`
5. Copy the URL and set it as `mm_webhook_url` in [Settings.py](settings.py)
6. You may also change the appearance of the Client and the target channel in this file


## Setup Octane Webhooks

To Setup ALM Octane Webhooks you need to follow these steps:
1. Start the client by running `python app.py` 
2. Under Settings (Cog-Wheel) Click on `Spaces` in the `Administration` category.
3. Select The Workspace you want to setup the Webhooks for.
4. Under the `Entities` Category select `Defect`.
5. Press the `+` button to add a rule.
6. Set up the Webhook
- Status: On
- Action: Trigger Webhook
- Submission Mode: New, Update, Delete (or your choice of the three)
- URL: The URL set in settings.py / which was shown in the console on client startup

**Don't forget to pass the security token set in settings.py/shown on startup**
- Credentials: Empty
    Feel free to test the connection if the client is running
- Fields:
`Author`, `Blocked`, `Blocked reason`, `Closed on`, `Creation time`, `Defect Type`, `Description`, `Detected by`, `Last modified`, `Name`, `Owner`, `Tags`
- **Leave the rest as is**
- Press `OK`
- Leave settings and **save**


## Run the application

If you have installed all packages, set all necessary variables in [Settings.py](settings.py) and setup Mattermost as well as ALM Octane for the Webhooks you can execute the client by typing `python app.py` in the console window.
