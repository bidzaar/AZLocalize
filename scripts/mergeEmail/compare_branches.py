import os
import git
import shutil

def compare_branches(repo_path, branch1, branch2, folder1, folder2, exceptions=['examples/emails/forks']):
    repo = git.Repo(repo_path)

    readme_path = os.path.join(repo_path, "translations/emails", "readMe.md")

    # Checkout the first branch
    repo.heads[branch1].checkout()

    # Get the list of files in the first branch
    files1 = set(f.path for f in repo.index.entries.values() if f.path.startswith(folder1) and not any(os.path.commonprefix([f.path, ex]) == ex for ex in exceptions))

    # Checkout the second branch
    repo.heads[branch2].checkout()

    # Get the list of files in the second branch
    files2 = set(f.path for f in repo.index.entries.values() if f.path.startswith(folder1) and not any(os.path.commonprefix([f.path, ex]) == ex for ex in exceptions))

    # Find the files that have been changed or added in the second branch
    added_files = files2 - files1
    changed_files = [f for f in files2 if f in files1 and repo.head.commit.tree[f].hexsha != repo.commit(branch1).tree[f].hexsha]

    # Copy the changed and added files to folder2, preserving the relative path
    for f in changed_files + list(added_files):
        src_path = os.path.join(repo_path, f)
        dst_path = os.path.join(repo_path, f.replace(f"{folder1}/", f"{folder2}/"))
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src_path, dst_path)

    # Write the readMe.md file with the report
    with open(readme_path, "w") as readme:
        readme.write("Files changed in the '{}' branch compared to the '{}' branch:\n\n".format(branch2, branch1))
        for f in sorted(changed_files, key=str.lower):
            readme.write("- {}\n".format(f.replace(f"{folder1}/", f"{folder2}/")))
        readme.write("\nFiles added in the '{}' branch:\n\n".format(branch2))
        for f in sorted(added_files, key=str.lower):
            readme.write("- {}\n".format(f.replace(f"{folder1}/", f"{folder2}/")))


if __name__ == "__main__":
    compare_branches("../..", "releasetr-3.18.2", "releasetr-4.1.1", "examples/emails/templates", "translations/emails/templates")
