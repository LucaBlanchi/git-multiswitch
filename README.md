# What it is
git-multiswitch is a command line utility for switching branch in multiple git repositories with a single command. Calling a combination of branches for the relevant repositories an "env", one can save envs, switch back to them, list and remove them.

# How to configure it
Edit repos.json to store the relevant repositories: the keys are the name of the repo folders, and the values are the absolute paths to the folder holding them (repos do no have to share the same path).
Envs can be added throgh the command line utility (recommended), or manually following /envs/example.json

# How to use it
Launch `main.py` as a python script. You have now access to the following commands:

- switch {env_name}, or simply {env_name}: switch to the env (combination of branches) stored in /envs/{env_name}
- save {env_name}: save the current env to a corresponding {env_name}.json file
- ls: list the current envs
- rm: {env_name}: remove {env_name}.json env
- clear: clear console, as in bash
- q: close the program

# Create a Bash script (Linux)
To launch the script as a command, without referencing its path, create a .sh file (suggested name gms.sh) containing
`python3 {path-to-main.py}`
and move it to a folder in $PATH (echo $PATH to list them, usually `/usr/local/bin`).
The script can now be executed in the terminal with `{script-name}.sh`.
