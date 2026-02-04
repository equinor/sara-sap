from enum import Enum


class RelationshipType(str, Enum):
    TAGS = "tags"
    EQUIPMENT = "equipment"
    MEASURING_POINTS = "measuring-points"
    MAINTENANCE_RECORDS = "maintenance-records"
    MATERIALS = "materials"
