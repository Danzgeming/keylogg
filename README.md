# Program objectives
This is a KeyLogger, use it for testing purposes only.
You will gather keyboard strokes, mouse movements, screenshots and microphone input.
All the collected keyboard strokes and mouse clicks info will be sent via email every defined time interval.
All the collected images and audio files will be sent via Dropbox integration to the defined Dropbox account.

## Program phases

### Imports

Note: to install everything you need you should run
```python
pip install -r requirements.txt
```

### Configuration

Define email details for sending logs.
For this project, I created an email account using [mailtrap](https://mailtrap.io).
Create and use API key for Dropbox service.
Specify the interval for sending reports (SEND_REPORT_EVERY) and some other variables.

### KeyLogger Class

- Collects system information (hostname, IP address, processor, system, machine).
- Collects system geo-location
- Monitors keyboard strokes.
- Records mouse movements, clicks, and scrolls - but only log clicks to reduce the quantity of logs.
- Take screenshots at every click.
- Capture microphone input.
- Saves the logged data to a string (self.log).
- Sends email reports with logged data.
- Upload image and audio files to Dropbox.
- Clean the data.
- The run method starts the KeyLogger by setting up keyboard, mouse, screenshot and microphone listeners.

### Execution

Creates an instance of the KeyLogger class with the needed variables.
Calls the run method to start the KeyLogger.
The first action, based on the operating system, deletes the .env file. In this way, the target cannot see your sensitive data.
Write the magic word (if set) to break the loop.

### TODO
- Add an optional parameter to copy the Python script somewhere and creates a scheduled task to execute it
- Create a USB key that runs upon it's plugged in a PC
- Improve the remove_env_file function to remove the .env file only when somebody tries to check the file content
- Add the Dropbox token renewal, otherwise it will last for 4 hours
