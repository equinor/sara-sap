from enum import Enum


class WorkOrderRelationship(str, Enum):
    ObjectList = "ObjectList"
    TechnicalFeedback = "TechnicalFeedback"


class ActivityReportStatus(str, Enum):
    NOCO = "NOCO"  # Notification completed
    CANC = "CANC"  # Cancelled
    EVCO = "EVCO"  # Evaluation Complete
    RECO = "RECO"  # Results Recording Complete
    NOPR = "NOPR"  # Notification in process
