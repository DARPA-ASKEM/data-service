from pytest import fixture


@fixture()
def code_json():
    return {
        "name": "Test Code Snippet",
        "description": "A test code sample.",
        "repo_url": "",
        "language": "python",
        "filename": "test.py",
    }
