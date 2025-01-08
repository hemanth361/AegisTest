import os

def create_project_structure():
  """Creates the project directory structure."""

  try:
    # Create main directories
    os.makedirs("app", exist_ok=True)
    os.makedirs("tests", exist_ok=True)

    # Create subdirectories
    os.makedirs("app/__pycache__", exist_ok=True)
    os.makedirs("tests/__pycache__", exist_ok=True)

    # Create empty files
    open("app/__init__.py", "w").close()
    open("app/main.py", "w").close()
    open("app/utils.py", "w").close()
    open("tests/__init__.py", "w").close()
    open("tests/test_core.py", "w").close()
    open("requirements.txt", "w").close()
    open(".gitignore", "w").close()
    open("README.md", "w").close()

    print("Project structure created successfully!")

  except OSError as error:
    print(f"Error creating directories: {error}")

if __name__ == "__main__":
  create_project_structure()