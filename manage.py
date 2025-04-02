import subprocess
import sys


def run_command(command):
    command_map = {
        "create_admins": "app.management.commands.create_admins",
    }

    if command in command_map:
        module_name = command_map[command]
        subprocess.run([sys.executable, "-m", module_name, *sys.argv[2:]])
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: manage.py <command> [args]")
    else:
        run_command(sys.argv[1])
