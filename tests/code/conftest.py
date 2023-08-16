from pytest import fixture


@fixture()
def code_json():
    return {
        "name": "Test Code Snippet",
        "description": "A test code sample.",
        "language": "python",
        "filename": "test.py",
    }
