from dataclasses import dataclass
from typing import Callable, List, Union

from licenseware.config.config import Config
from licenseware.constants import alias_types as alias
from licenseware.constants.attributes_type import AttributesType
from licenseware.utils.alter_string import get_altered_strings

from .report_filter import ReportFilter
from .style_attributes import StyleAttrs


@dataclass
class NewReportComponent:
    title: str
    component_id: str
    attributes: AttributesType
    style_attributes: StyleAttrs
    get_component_data_handler: Callable[
        [
            alias.TenantId,
            alias.Authorization,
            alias.Repository,
            alias.Filters,
            alias.Limit,
            alias.Skip,
        ],
        Union[List[dict], dict],
    ]
    config: Config
    component_type: str = None
    description: str = None
    order: int = None
    filters: ReportFilter = None
    registrable: bool = True

    def __post_init__(self):

        if isinstance(self.filters, ReportFilter):  # pragma no cover
            self.filters = self.filters.metadata

        compid = get_altered_strings(self.component_id).dash

        if self.component_type is None:
            self.component_type = self.attributes.component_type

        if hasattr(self.attributes, "metadata"):
            self.attributes = self.attributes.metadata

        if hasattr(self.style_attributes, "metadata"):
            self.style_attributes = self.style_attributes.metadata

        self.url = f"/report-components/{compid}"
        self.public_url = f"/public-report-components/{compid}"
        self.snapshot_url = f"/snapshot-report-components/{compid}"

    def get_metadata(self):

        if not self.registrable:
            return

        metadata = {
            "app_id": self.config.APP_ID,
            "component_id": self.component_id,
            "description": self.description,
            "url": self.url,
            "public_url": self.public_url,
            "snapshot_url": self.snapshot_url,
            "order": self.order,
            "style_attributes": self.style_attributes,
            "attributes": self.attributes,
            "title": self.title,
            "type": self.component_type,
            "filters": self.filters,
        }

        return metadata
