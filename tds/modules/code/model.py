"""
TDS Code Data Model Definition.
"""
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from tds.db.base import TdsModel
from tds.db.enums import ProgrammingLanguage


class CodeFile(BaseModel):
    """
    CodeFile Data Model for individual file entries in the main Code model.
    """

    language: Optional[ProgrammingLanguage] = Field(
        description="Programming language of the file."
    )
    dynamics: Optional[str] = Field(
        None,
        description="String indicating the line numbers in the file that contain the dynamics, e.g., 'L205-L213'.",
    )


class Code(TdsModel):
    """
    Code Data Model
    """

    name: str = Field(description="Name of the code/repo.")
    description: str = Field(description="Description for code/repo.")
    files: Optional[Dict[str, CodeFile]] = Field(
        description="Dictionary of code files with file paths as keys."
    )
    repo_url: Optional[str] = Field(
        None, description="URL to the repository where the code resides."
    )
    commit: Optional[str] = Field(None, description="Commit hash or ID for the repo.")
    branch: Optional[str] = Field(None, description="Branch name of the repo.")
    metadata: Optional[dict] = Field(
        None, description="Optional metadata associated with the code."
    )

    _index = "code"

    class Config:
        """
        Code Data Model Swagger Example
        """

        schema_extra = {
            "example": {
                "name": "Example Model Code",
                "description": "Example of a Python-based code object for a model",
                "files": {
                    "path/to/test.py": {
                        "path": "path/to/test.py",
                        "language": "python",
                    },
                    "path/to/fun.py": {
                        "path": "path/to/fun.py",
                        "language": "python",
                        "dynamics": "L205-L213",
                    },
                },
                "repo_url": "https://github.com/user/repo.git",
                "commit": "abcd1234",
                "branch": "main",
            }
        }
