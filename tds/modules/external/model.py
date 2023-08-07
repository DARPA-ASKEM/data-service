"""
TDS External Data Model Definition.
"""
from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy import func

from tds.db.base import Base


class Publication(Base):
    """
    External Publication Data Model.
    """

    __tablename__ = "publication"

    id = sa.Column(sa.Integer(), primary_key=True)
    xdd_uri = sa.Column(sa.String(), nullable=False)
    title = sa.Column(sa.String(), nullable=False)
    publication_data = sa.Column(sa.JSON, nullable=True)


class PublicationPayload(BaseModel):
    """
    External PublicationPayload Model.
    """

    id: Optional[int] = None
    xdd_uri: str
    title: str
    publication_data: Optional[dict]


class Software(Base):
    """
    External Software Data Model.
    """

    __tablename__ = "software"

    id = sa.Column(sa.Integer(), primary_key=True)
    timestamp = sa.Column(sa.DateTime(), nullable=False, server_default=func.now())
    source = sa.Column(sa.String(), nullable=False)
    storage_uri = sa.Column(sa.String(), nullable=False)


class SoftwarePayload(BaseModel):
    """
    External SoftwarePayload Model.
    """

    id: Optional[int] = None
    timestamp: datetime = datetime.now()
    source: str
    storage_uri: str
