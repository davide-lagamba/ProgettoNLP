from git import Repo
from shutil import move

from training import replace_line


def main():
    # Necessary to import the model and utility scripts
    Repo.clone_from("https://github.com/chiayewken/Span-ASTE.git", "SpanASTE")
    move("SpanASTE/training_config", "./")
    replace_line("training_config/config.jsonnet", 82, "    cuda_device: -1,\n")

if __name__ == "__main__":
    main()

