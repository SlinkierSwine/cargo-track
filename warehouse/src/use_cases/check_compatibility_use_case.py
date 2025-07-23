from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import structlog
from entities.cargo import Cargo
from entities.warehouse import Warehouse
from entities.compatibility import CompatibilityReport, CompatibilityCheckRequest, CompatibilityCheckResponse
from repositories.interfaces.cargo_repository import CargoRepositoryInterface
from repositories.interfaces.warehouse_repository import IWarehouseRepository
from utils.fleet_service_client import FleetServiceInterface
from shared.use_cases.base_use_case import BaseUseCase
import uuid
from datetime import datetime

logger = structlog.get_logger()


class CheckCompatibilityUseCase(BaseUseCase[CompatibilityCheckResponse]):
    def __init__(self, cargo_repository: CargoRepositoryInterface):
        self.cargo_repository = cargo_repository
        self.fleet_service = FleetServiceInterface()

    def execute(self, request: CompatibilityCheckRequest, token: str) -> CompatibilityCheckResponse:
        logger.info("Starting compatibility check", cargo_id=request.cargo_id, vehicle_id=request.vehicle_id)
        
        # Получаем информацию о грузе
        cargo = self.cargo_repository.get_by_id(request.cargo_id)
        if not cargo:
            logger.error("Cargo not found", cargo_id=request.cargo_id)
            raise ValueError(f"Cargo with id {request.cargo_id} not found")

        logger.info("Cargo found", cargo_id=cargo.id, cargo_name=cargo.name)

        # Получаем информацию о транспортном средстве из fleet сервиса
        try:
            vehicle_info = self.fleet_service.get_vehicle(request.vehicle_id, token)
            logger.info("Vehicle info retrieved", vehicle_id=request.vehicle_id, vehicle_info=vehicle_info)
        except Exception as e:
            logger.error("Failed to get vehicle info", vehicle_id=request.vehicle_id, error=str(e))
            raise ValueError(f"Vehicle with id {request.vehicle_id} not found")

        if not vehicle_info:
            logger.error("Vehicle not found", vehicle_id=request.vehicle_id)
            raise ValueError(f"Vehicle with id {request.vehicle_id} not found")

        # Проверяем совместимость
        issues = []
        recommendations = []
        compatibility_score = 100

        logger.info("Starting compatibility checks", 
                   cargo_weight=cargo.weight, 
                   cargo_volume=cargo.volume,
                   vehicle_capacity_weight=vehicle_info.get("capacity_weight"),
                   vehicle_capacity_volume=vehicle_info.get("capacity_volume"))

        # Проверка веса
        weight_compatible = cargo.weight <= vehicle_info["capacity_weight"]
        if not weight_compatible:
            issues.append(f"Cargo weight ({cargo.weight} kg) exceeds vehicle capacity ({vehicle_info['capacity_weight']} kg)")
            compatibility_score -= 30
            recommendations.append("Consider using a vehicle with higher weight capacity")

        # Проверка объема
        volume_compatible = cargo.volume <= vehicle_info["capacity_volume"]
        if not volume_compatible:
            issues.append(f"Cargo volume ({cargo.volume} m³) exceeds vehicle capacity ({vehicle_info['capacity_volume']} m³)")
            compatibility_score -= 25
            recommendations.append("Consider using a vehicle with higher volume capacity")

        # Проверка температурных требований
        temperature_compatible = not (cargo.temperature_requirements and not vehicle_info["temperature_controlled"])
        if not temperature_compatible:
            issues.append("Cargo requires temperature control, but vehicle is not temperature controlled")
            compatibility_score -= 20
            recommendations.append("Use a temperature-controlled vehicle")

        # Проверка опасных материалов
        hazardous_compatible = not (cargo.hazardous_material and not vehicle_info["hazardous_materials_certified"])
        if not hazardous_compatible:
            issues.append("Cargo contains hazardous materials, but vehicle is not certified for hazardous transport")
            compatibility_score -= 25
            recommendations.append("Use a vehicle certified for hazardous materials transport")

        # Проверка специального оборудования
        special_requirements_met = True
        if cargo.special_handling:
            required_equipment = cargo.special_handling
            available_equipment = vehicle_info["special_equipment"]
            
            missing_equipment = []
            for equipment in required_equipment:
                if equipment not in available_equipment:
                    missing_equipment.append(equipment)
            
            if missing_equipment:
                special_requirements_met = False
                issues.append(f"Vehicle missing required equipment: {', '.join(missing_equipment)}")
                compatibility_score -= 15
                recommendations.append(f"Use a vehicle with equipment: {', '.join(missing_equipment)}")

        # Определяем общую совместимость
        is_compatible = compatibility_score >= 70

        if compatibility_score < 0:
            compatibility_score = 0

        # Конвертируем в 0.0-1.0 шкалу
        score = compatibility_score / 100.0

        logger.info("Compatibility check completed", 
                   is_compatible=is_compatible, 
                   compatibility_score=compatibility_score,
                   issues_count=len(issues))

        return CompatibilityCheckResponse(
            id=str(uuid.uuid4()),
            cargo_id=request.cargo_id,
            vehicle_id=request.vehicle_id,
            is_compatible=is_compatible,
            score=score,
            weight_compatible=weight_compatible,
            volume_compatible=volume_compatible,
            temperature_compatible=temperature_compatible,
            hazardous_compatible=hazardous_compatible,
            special_requirements_met=special_requirements_met,
            risks=issues,
            recommendations=recommendations,
            created_at=datetime.utcnow()
        ) 