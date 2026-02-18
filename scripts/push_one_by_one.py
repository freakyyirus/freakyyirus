import os
import subprocess
import time

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(e.stderr)
        return None

def main():
    # Configuration
    DELAY_SECONDS = 30
    REMOTE_NAME = "origin"
    BRANCH_NAME = "main"

    # Check if git is initialized
    if not os.path.exists(".git"):
        print("Error: Not a git repository. Run 'git init' first.")
        return

    # Check if remote is configured
    remote_check = run_command(f"git remote get-url {REMOTE_NAME}")
    if not remote_check:
        print(f"Error: Remote '{REMOTE_NAME}' not configured. Please add the remote repository URL.")
        return

    # List all files (skipping .git and ignored files)
    # We'll use git status to identify untracked/modified files to adhere to .gitignore
    status_output = run_command("git status --porcelain")
    if not status_output:
        print("No changes to commit.")
        return

    files_to_process = []
    for line in status_output.splitlines():
        # status codes can be ' M', '??', 'A ', etc.
        # extraction depends on the format. '??' is untracked.
        # We want the file path which is after the status code (first 2 chars + space)
        file_path = line[3:]
        files_to_process.append(file_path)

    print(f"Found {len(files_to_process)} files to process.")

    for i, file_path in enumerate(files_to_process):
        print(f"[{i+1}/{len(files_to_process)}] Processing: {file_path}")
        
        # Add file
        run_command(f'git add "{file_path}"')
        
        # Commit
        commit_message = f"Add file: {os.path.basename(file_path)}"
        run_command(f'git commit -m "{commit_message}"')
        
        # Push
        print(f"Pushing to {REMOTE_NAME}/{BRANCH_NAME}...")
        push_result = run_command(f"git push {REMOTE_NAME} {BRANCH_NAME}")
        
        if push_result is not None:
            print("Push successful.")
        else:
            print("Push failed. Creating a backup plan or continuing?")
        
        if i < len(files_to_process) - 1:
            print(f"Waiting {DELAY_SECONDS} seconds...")
            time.sleep(DELAY_SECONDS)

if __name__ == "__main__":
    main()
