import os


def git_init():
    try:
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    except FileExistsError:
        print(f"Git directory already initialized at {os.getcwd()}")


