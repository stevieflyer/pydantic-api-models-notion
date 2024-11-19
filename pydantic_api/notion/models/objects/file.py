"""
Reference: 

- https://developers.notion.com/reference/file-object
- https://developers.notion.com/reference/page-property-values#files
"""

from datetime import datetime
from typing import Literal, Optional, Annotated, Union

from pydantic import Field, HttpUrl

from pydantic_api.base import BaseModel


FileObjectTypeLiteral = Literal["external", "file"]


class _FileExternal(BaseModel):
    """The `external` field of a `ExternalFileObject`."""

    url: HttpUrl


class _FileUploaded(BaseModel):
    """The `file` field of a `UploadedFileObject`."""

    url: HttpUrl
    expiry_time: Optional[datetime] = None


class _BaseFileObject(BaseModel):
    type: FileObjectTypeLiteral
    name: Optional[str] = Field(
        None, description="The name of the file to discriminate it."
    )
    """`name` field is not mentioned in https://developers.notion.com/reference/file-object, but mentioned in: https://developers.notion.com/reference/page-property-values#files"""


class ExternalFileObject(_BaseFileObject):
    """A file object corresponding to an external file that has been linked to in Notion"""

    type: Literal["external"] = "external"
    external: _FileExternal

    @classmethod
    def new(cls, url: HttpUrl):
        """
        Args:
            url (str): The URL of the external file.

        Returns:
            ExternalFileObject: An instance of ExternalFileObject.
        """
        return cls(external=_FileExternal(url=url))


class UploadedFileObject(_BaseFileObject):
    """A file object corresponding to a file that has been uploaded to Notion"""

    type: Literal["file"] = "file"
    file: _FileUploaded

    @classmethod
    def new(cls, url: HttpUrl, expire_time: Optional[datetime] = None):
        """
        Args:
            url (str): The URL of the uploaded file.
            expire_time (datetime, optional): The time at which the file will expire. Defaults to None.

        Returns:
            UploadedFileObject: An instance of UploadedFileObject
        """
        return cls(file=_FileUploaded(url=url, expiry_time=expire_time))


FileObject = Annotated[
    Union[ExternalFileObject, UploadedFileObject], Field(discriminator="type")
]
"""FileObject. Reference: https://developers.notion.com/reference/file-object"""


class FileObjectFactory:
    @classmethod
    def new_external(cls, url: HttpUrl) -> ExternalFileObject:
        """
        Create a new External File Object

        Args:
            url (str): The URL of the external file.

        Returns:
            ExternalFileObject: An instance of ExternalFileObject.
        """
        return ExternalFileObject.new(url=url)

    @classmethod
    def new_uploaded(
        cls, url: HttpUrl, expire_time: Optional[datetime] = None
    ) -> UploadedFileObject:
        """
        Create a new Uploaded File Object

        Args:
            url (str): The URL of the uploaded file.
            expire_time (datetime, optional): The time at which the file will expire. Defaults to None.

        Returns:
            UploadedFileObject: An instance of UploadedFileObject
        """
        return UploadedFileObject.new(url=url, expire_time=expire_time)


__all__ = [
    "FileObjectTypeLiteral",
    "ExternalFileObject",
    "UploadedFileObject",
    "FileObject",
    "FileObjectFactory",
]