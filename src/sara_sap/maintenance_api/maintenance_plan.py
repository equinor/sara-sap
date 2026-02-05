from loguru import logger


class MaintenancePlanController:
    def __init__(self) -> None:
        pass

    def get_maintenance_plan(self, maintenance_plan_id: str) -> dict:
        logger.info(f"Getting maintenance plan {maintenance_plan_id}")
        pass
