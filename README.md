# labmonitor_collector

## Cloud 9 Setup ##

git clone https://github.com/tommy1008/FYP.git

cd FYP/  
chmod +x *.sh  
./setup.sh  

after that you may need to run  
source venv/bin/activate  
if you found that you are not under the Python 3 Virtual Environment.

## Setup Python Auto Formatting after save ##
Setup Python Autoformting in Cloud9. yapf has installed at setup.sh.
Go to Preferences -> Python Support -> Custom Code Formatter:
yapf --in-place --aggressive "$file"  
