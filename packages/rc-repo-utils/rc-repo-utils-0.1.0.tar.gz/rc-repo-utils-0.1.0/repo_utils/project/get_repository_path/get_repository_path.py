import os
import git
import inspect


def get_repository_path(starting_path: str=None):
    """
    Args:
        - starting_path (str): File location from which to find the containing git repository.
            If not provided, will use the file location of the calling Python file.
            When calling from the command line, the current working directory is used.

    Returns:
        - path (str): The path of the root directory of this repository.
            If not found, returns None.
    """
    if starting_path is None:
        previous_frame = inspect.currentframe().f_back
        previous_previous_frame = previous_frame.f_back
        (starting_path, line_number, function_name, lines, index) = inspect.getframeinfo(previous_previous_frame)
        if "<frozen" in starting_path or 'site-packages' in starting_path:
            (starting_path, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)
        if 'repo_utils' in starting_path:
            # When using the repo_utils command line, use repository of the current working directory.
            starting_path = os.getcwd()
    try:
        repo = git.Repo(starting_path, search_parent_directories=True)
        repo_root = repo.working_tree_dir
        return repo_root
    except git.exc.InvalidGitRepositoryError:
        print(f'Could not find git repository root for the filepath {starting_path}')
        return None
