"""
TDS Code Data Model Definition.
"""
from typing import Dict, Optional

from pydantic import BaseModel, Field

from tds.db.base import TdsModel


class Dynamics(BaseModel):
    """
    Dynamics Data Model for capturing dynamics within a CodeFile.
    """

    name: Optional[str] = Field(description="Name of the dynamics section.")
    description: Optional[str] = Field(description="Description of the dynamics.")
    block: List[str] = Field(
        description="A list containing strings indicating the line numbers in the file that contain the dynamics, e.g., ['L205-L213', 'L225-L230']."
    )


class CodeFile(BaseModel):
    """
    CodeFile Data Model for individual file entries in the main Code model.
    """

    language: Optional[str] = Field(description="Programming language of the file.")
    dynamics: Optional[Dynamics] = Field(
        description="Dynamics details associated with the file."
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
                        "language": "python",
                    },
                    "path/to/fun.py": {
                        "language": "python",
                        "dynamics": {
                            "name": "Main Dynamics",
                            "description": "Dynamics section for the ODE.",
                            "block": "[`L205-L213`, `L225-L230`]",
                        },
                    },
                },
                "repo_url": "https://github.com/user/repo.git",
                "commit": "abcd1234",
                "branch": "main",
            }
        }
