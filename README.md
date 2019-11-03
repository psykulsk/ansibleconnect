# Ansibleinviewer - Ansible Inventory Viewer 

## SSH into all 'sshable' hosts in your inventory with one command.

Ansibleinviewer creates a bash script based on your ansible inventory.
That script will create a new tmux session and create a separate pane
for each one of your 'sshable' inventory hosts. Inside of each of the
panes an ssh connection to the pane's host will be established.

#### Setup example (on Ubuntu):
```
sudo apt install tmux
sudo apt install sshpass
git clone https://github.com/psykulsk/ansibleinviewer.git
cd ansibleinviewer
python3 -m pip install .
```

#### Example:
```
source <(ansibleinviewer -i inventory.yml)
```

