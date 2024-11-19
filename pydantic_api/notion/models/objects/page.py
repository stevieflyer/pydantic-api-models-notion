from datetime import datetime
from typing import Optional, Literal, Union, Dict, Any, Annotated

from uuid import UUID
from pydantic import Field

from pydantic_api.base import BaseModel
from .user import PartialUser
from .common import IconObject, CoverObject
from .parent import DatabaseParentObject, PageParentObject, WorkspaceParentObject


ParentOfPage = Annotated[
    Union[DatabaseParentObject, PageParentObject, WorkspaceParentObject],
    Field(discriminator="type"),
]
"""
The type of the parent of a page. It could be a `DatabaseParentObject`, `PageParentObject` or `WorkspaceParentObject`. (Reference: https://developers.notion.com/reference/page)

Note: Until Nov 2024, only `DatabaseParentObject` and `PageParentObject` are supported as page's parent. (Reference: https://developers.notion.com/reference/post-page It writes the following as the description of param `parent` when creating a page: 'The parent page or database where the new page is inserted, represented as a JSON object with a page_id or database_id key, and the corresponding ID.')
"""


class Page(BaseModel):
    """Reference: https://developers.notion.com/reference/page"""

    object: Literal["page"] = "page"
    id: UUID
    created_time: datetime
    created_by: PartialUser
    last_edited_time: datetime
    last_edited_by: PartialUser
    archived: bool
    in_trash: bool
    icon: Optional[IconObject] = Field(None)
    cover: Optional[CoverObject] = Field(None)
    properties: Dict[str, Any] = Field(default_factory=dict)
    parent: ParentOfPage
    url: str
    public_url: Optional[str] = Field(None)

    @property
    def title_property(self) -> dict:
        return self.properties.get("title")


__all__ = [
    "ParentOfPage",
    "Page",
]