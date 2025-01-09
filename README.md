# Magnolia Gardens by MagicalMagnolias

## Task Assignment
Nia Lam: Project Manager + Middleware  
Amanda Tan: Frontend + Backend  
Naomi Lai: Frontend + Backend  
Kishi Wijaya: Database Lead + Artwork  

## Description  
Magnolia Gardens is a game about maintaining a garden of flowers. Users may plant flower seeds– each species has slightly different growth requirements. Flowers must be watered each day to grow. Water is infinitely available in the universe of the garden. Once a flower meets the requirement for days watered, it has bloomed and may be “picked” (transferred to the user’s inventory).

Another resource, magic power, automatically makes the flower bloom and is obtained from completing minigames of basic and simple arithmetic. Magic power may also be exchanged for flower seeds in the shop page.

Points called “flower score” will be assigned based on (equal to) the number of days taken to grow the flower. As the user progresses, “flower score” unlocks more flower varieties which will appear in the shop.  The game may continue indefinitely, but the “goal” is to unlock the final “Mythical Magnolia.”

These interactions take place on a grid-based garden using JavaScript. The user’s profile displays minigame statistics and the flower score, as well as “picked” flowers. Users must be logged in to play.

## Install Guide:
  To install, go to the top of the page and click the green button that says "Code". In the dropdown that appears, click "Download Zip" at the bottom. Extract the zip from your downloads into your home directory. <br>

OR
  
  To clone the repository, go to the top of the page and click the green button that says "Code". In the dropdown that appears, choose either "HTTPS" or "SSH" under the "Clone" section and copy the provided URL. Open up your computer's terminal and type "git clone {URL HERE}"

1. Make a python virtual environment if one does not already exist

      a. Open up your device's terminal

      b. Type ```$ python3 -m venv {path name}``` or ```$ py -m venv {path name}```

  1. Ensure your virtual environment is activated

  1. Access the repository by typing ```$ cd MagicalMagnolias__nial24_amandat109_kishiw2_naomil49/```

  1. Type ```$ pip install -r requirements.txt``` to install the required modules

 - If terminal returns ```zsh: command not found: pip```, type ```$ pip3 install -r requirements.txt``` because ```$ pip``` is for python2.

## Launch Codes:
  Instructions:

  1. Activate the virtual environment by typing in one of the commands into your terminal for your specific OS

      - Linux: ```$ . {path name}/bin/activate```
    
      - Windows Command Prompt: ```> {path name}\Scripts\activate```

      - Windows PowerShell: ```> . .\{path name}\Scripts\activate```

      - MacOS: ```$ source {path name}/bin/activate```

      (If successful, the command line should display the name of your virtual environment: ```({path name})$ ```)
  
  1. Navigate to app by typing ```$ cd {path}/MagicalMagnolias__nial24_amandat109_kishiw2_naomil49/app/```
    
  1. Type ```$ python3 __init__.py``` to run the application

  1. Copy / type "http://127.0.0.1:5000" or "http://localhost" onto a browser to view the website

  1. When done, type ```$ deactivate``` to deactivate the virtual environment
