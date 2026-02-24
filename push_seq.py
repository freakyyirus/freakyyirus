import subprocess
import time

def main():
    # Use config locally to avoid quoting issues in path names
    subprocess.run(["git", "config", "core.quotepath", "false"])

    status_out = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout
    
    files_to_push = []
    for line in status_out.splitlines():
        if len(line) > 3:
            # Strip status prefix and any surrounding quotes
            file_path = line[3:].strip('"')
            if file_path:
                files_to_push.append(file_path)

    for fp in files_to_push:
        print(f"Pushing {fp}...")
        subprocess.run(["git", "add", fp])
        subprocess.run(["git", "commit", "-m", f"update: {os.path.basename(fp) if 'os' in globals() else fp}"])
        subprocess.run(["git", "push", "origin", "main"])
        print(f"Pushed {fp}. Waiting 2 seconds...")
        time.sleep(2)

import os
if __name__ == "__main__":
    main()
