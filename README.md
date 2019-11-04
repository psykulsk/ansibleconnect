# Ansibleinviewer - Ansible Inventory Viewer 

## SSH into all hosts in your inventory with one command.

Ansibleinviewer creates a bash script based on your ansible inventory.
That script will create a new tmux session and create a separate pane
for each one of your 'sshable' inventory hosts. Inside of each of the
panes an ssh connection to the pane's host will be established.

![](doc/demo.gif)

### Setup example (on Ubuntu):
```
sudo apt install tmux
sudo apt install sshpass
git clone https://github.com/psykulsk/ansibleinviewer.git
cd ansibleinviewer
python3 -m pip install .
```

### Usage example:
```
source <(ansibleinviewer -i inventory.yml)
```

### Authentication


#### ssh-agent

For authentication one can use ssh keys. `ansibleinviewer` will scan the inventory file for connection options (`ansible_ssh_common_args`, `ansible_ssh_user`, `ansible_host`). Ssh keys can be passed via them. Otherwise, one can use the `ssh-agent` tool. Environment args (`SSH_AGENT_PID` and `SSH_AUTH_SOCK`) will be passed to each one of the tmux shells.

##### ssh-agent setup example
```
eval $(ssh-agent)
ssh-add ~/.ssh/my_private_key\
```

#### sshpass

If `ansible_ssh_pass` variable is used in the inventory, one should installl the `sshpass` and make it discoverable via `PATH`. Please note that when using the sshpass, password will passed in plaintext and it will be saved in each of the tmux shells' history.
