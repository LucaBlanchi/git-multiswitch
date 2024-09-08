import subprocess
import os
import json

class CommandLauncher:
    
    def __init__(self):
        self.loop = True
        self.commands = {
            'q': self.q,
            'clear': self.clear,
            'switch': self.switch,
            'ls': self.ls,
            'save': self.save,
            'rm': self.rm
        }
        self.load_repos()

    def execute(self, command):
        method_name = command[0]
        params = command[1:]

        method = self.commands.get(method_name, None)
        if method is not None:
            return method(params)
        else:
            self.switch(command)
    
    def load_repos(self):
        self.repos_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../repos.json')
        if not os.path.exists(self.repos_file_path):
            print(f"Repository configuration file {self.repos_file_path} not found.")
            self.repos = {}
            return

        with open(self.repos_file_path, 'r') as f:
            self.repos = json.load(f)

    def q(self, params):
        self.loop = False
    
    def clear(self, params):
        subprocess.run('clear', shell=True)

    def switch(self, params):
        if len(params) != 1:
            print("Usage: switch {env}")
            return
        
        env_name = params[0]
        env_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../envs/{env_name}.json')
        
        if not os.path.exists(env_file_path):
            print(f"Configuration file {env_file_path} not found.")
            return

        with open(env_file_path, 'r') as f:
            branches = json.load(f)

        def switch_branch(repo_name, repo_path, branch):
            try:
                if not os.path.exists(repo_path):
                    print(f"Repository path for {repo_name} does not exist.")
                    return
                
                os.chdir(repo_path)
                
                subprocess.run(['git', 'checkout', branch], check=True)
                
                print(f"Successfully switched {repo_name} to branch {branch} in {repo_path}")
            except subprocess.CalledProcessError:
                print(f"Failed to switch {repo_name} to branch {branch} in {repo_path}")

        for repo_name, branch in branches.items():
            repo_path = os.path.join(self.repos.get(repo_name), repo_name)
            if repo_path:
                print(f"Switching {repo_name} to branch {branch}...")
                switch_branch(repo_name, repo_path, branch)
            else:
                print(f"Repository {repo_name} not found in repos.json.")

    def ls(self, params):
        envs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../envs')
        
        if not os.path.exists(envs_dir):
            print(f"Directory {envs_dir} not found.")
            return
        
        files = [f for f in os.listdir(envs_dir) if f.endswith('.json')]
        
        if not files:
            print("No environment files found.")
        else:
            print("Available environments:")
            for file in files:
                print(file)

    def save(self, params):
        if len(params) != 1:
            print("Usage: save {env}")
            return
        
        env_name = params[0]
        current_env_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../envs/{env_name}.json')

        branches = {}
        
        for repo_name, repo_path in self.repos.items():
            repo_path = os.path.join(repo_path, repo_name)
            if not os.path.exists(repo_path):
                print(f"Repository path for {repo_name} does not exist.")
                continue
            
            os.chdir(repo_path)
            try:
                result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True, check=True)
                current_branch = result.stdout.strip()
                branches[repo_name] = current_branch
            except subprocess.CalledProcessError:
                print(f"Failed to get the current branch for {repo_name}.")
        
        with open(current_env_file_path, 'w') as f:
            json.dump(branches, f, indent=4)
        
        print(f"Saved current branches to {current_env_file_path}")

    def rm(self, params):
        if len(params) != 1:
            print("Usage: rm {env}")
            return
        
        env_name = params[0]
        env_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../envs/{env_name}.json')

        if os.path.exists(env_file_path):
            os.remove(env_file_path)
            print(f"Removed environment file {env_file_path}")
        else:
            print(f"Environment file {env_file_path} does not exist.")

