import unittest
import os
import tempfile
import git
import shutil
import compare_branches

class TestCompareBranches(unittest.TestCase):
    def setUp(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.repo_path = os.path.join(script_dir, "repo")
        self.branch1 = "release1"
        self.branch2 = "release2"
        self.folder2 = os.path.join(script_dir, "folder2")

        self.repo = git.Repo.init(self.repo_path)

        # Create a file in the first branch
        file_path = os.path.join(self.repo_path, "file1.txt")
        with open(file_path, "w") as file1:
            file1.write("file1 content")
        self.repo.index.add([file_path])
        self.repo.index.commit("Initial commit")
        self.repo.create_head(self.branch1).checkout()
       

        # Create another file in the second branch
        file_path = os.path.join(self.repo_path, "file2.txt")
        with open(file_path, "w") as file2:
            file2.write("file2 content")
        self.repo.index.add([file_path])
        self.repo.create_head(self.branch2).checkout()
        self.repo.index.commit("Second commit")
      

    def tearDown(self):
        # shutil.rmtree(self.repo_path)
        # shutil.rmtree(self.folder2)
        pass

    def test_compare_branches(self):
        compare_branches.compare_branches(self.repo_path, self.branch1, self.branch2, self.folder2)

        # Check that the changed and added files were copied to folder2
        # self.assertTrue(os.path.exists(os.path.join(self.folder2, "file1.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.folder2, "file2.txt")))

        # Check that the readme file was created
        readme_path = os.path.join(self.folder2, "readMe.md")
        self.assertTrue(os.path.exists(readme_path))

        # Check the contents of the readme file
        with open(readme_path) as readme:
            contents = readme.read()
            self.assertIn("Files changed in the '{}' branch compared to the '{}' branch:\n\n".format(self.branch2, self.branch1), contents)
            self.assertIn("\nFiles added in the '{}' branch:\n\n".format(self.branch2), contents)
            # self.assertIn("- file1.txt\n", contents)
            self.assertIn("- file2.txt\n", contents)

if __name__ == "__main__":
    unittest.main()
