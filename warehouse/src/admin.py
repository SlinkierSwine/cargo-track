from sqladmin import Admin, ModelView
from fastapi import Request
from entities.database_models import WarehouseModel, CargoModel, CompatibilityReportModel, InventoryModel
from entities.warehouse import WarehouseType, WarehouseStatus
from entities.cargo import CargoType, CargoStatus, FragilityLevel
from utils.admin_auth import get_admin_auth


class WarehouseAdmin(ModelView, model=WarehouseModel):
    """Admin interface for Warehouse model"""
    name = "Warehouse"
    name_plural = "Warehouses"
    icon = "fa-solid fa-warehouse"
    
    # Fields to display in the list view
    column_list = [
        WarehouseModel.id,
        WarehouseModel.name,
        WarehouseModel.warehouse_type,
        WarehouseModel.city,
        WarehouseModel.country,
        WarehouseModel.total_capacity_weight,
        WarehouseModel.total_capacity_volume,
        WarehouseModel.available_capacity_weight,
        WarehouseModel.available_capacity_volume,
        WarehouseModel.temperature_controlled,
        WarehouseModel.hazardous_materials_allowed,
        WarehouseModel.status,
        WarehouseModel.created_at,
    ]
    
    # Fields to display in the detail view
    column_details_list = [
        WarehouseModel.id,
        WarehouseModel.name,
        WarehouseModel.warehouse_type,
        WarehouseModel.address,
        WarehouseModel.city,
        WarehouseModel.country,
        WarehouseModel.postal_code,
        WarehouseModel.phone,
        WarehouseModel.email,
        WarehouseModel.total_capacity_weight,
        WarehouseModel.total_capacity_volume,
        WarehouseModel.available_capacity_weight,
        WarehouseModel.available_capacity_volume,
        WarehouseModel.temperature_controlled,
        WarehouseModel.hazardous_materials_allowed,
        WarehouseModel.operating_hours,
        WarehouseModel.status,
        WarehouseModel.created_at,
        WarehouseModel.updated_at,
    ]
    
    # Fields that can be edited
    form_columns = [
        WarehouseModel.name,
        WarehouseModel.warehouse_type,
        WarehouseModel.address,
        WarehouseModel.city,
        WarehouseModel.country,
        WarehouseModel.postal_code,
        WarehouseModel.phone,
        WarehouseModel.email,
        WarehouseModel.total_capacity_weight,
        WarehouseModel.total_capacity_volume,
        WarehouseModel.temperature_controlled,
        WarehouseModel.hazardous_materials_allowed,
        WarehouseModel.operating_hours,
        WarehouseModel.status,
    ]
    
    # Fields to search by
    column_searchable_list = [
        WarehouseModel.name,
        WarehouseModel.city,
        WarehouseModel.country,
        WarehouseModel.email,
    ]
    
    # Fields to filter by
    column_filters = [
        WarehouseModel.warehouse_type,
        WarehouseModel.temperature_controlled,
        WarehouseModel.hazardous_materials_allowed,
        WarehouseModel.status,
        WarehouseModel.created_at,
    ]
    
    # Customize form field options
    form_choices = {
        WarehouseModel.warehouse_type: [
            (WarehouseType.DISTRIBUTION_CENTER, "Distribution Center"),
            (WarehouseType.STORAGE_FACILITY, "Storage Facility"),
            (WarehouseType.COLD_STORAGE, "Cold Storage"),
            (WarehouseType.HAZARDOUS_MATERIALS, "Hazardous Materials"),
            (WarehouseType.GENERAL_WAREHOUSE, "General Warehouse"),
        ],
        WarehouseModel.status: [
            (WarehouseStatus.ACTIVE, "Active"),
            (WarehouseStatus.MAINTENANCE, "Maintenance"),
            (WarehouseStatus.CLOSED, "Closed"),
            (WarehouseStatus.INACTIVE, "Inactive"),
        ]
    }
    
    def is_accessible(self, request: Request) -> bool:
        # Проверяем, что пользователь аутентифицирован и имеет роль admin
        user_role = request.session.get("role")
        return user_role == "admin"


class CargoAdmin(ModelView, model=CargoModel):
    """Admin interface for Cargo model"""
    name = "Cargo"
    name_plural = "Cargo"
    icon = "fa-solid fa-box"
    
    # Fields to display in the list view
    column_list = [
        CargoModel.id,
        CargoModel.tracking_number,
        CargoModel.cargo_type,
        CargoModel.name,
        CargoModel.weight,
        CargoModel.volume,
        CargoModel.value,
        CargoModel.hazardous_material,
        CargoModel.fragility_level,
        CargoModel.status,
        CargoModel.warehouse_id,
        CargoModel.created_at,
    ]
    
    # Fields to display in the detail view
    column_details_list = [
        CargoModel.id,
        CargoModel.tracking_number,
        CargoModel.cargo_type,
        CargoModel.name,
        CargoModel.description,
        CargoModel.weight,
        CargoModel.volume,
        CargoModel.dimensions,
        CargoModel.value,
        CargoModel.insurance_amount,
        CargoModel.temperature_requirements,
        CargoModel.humidity_requirements,
        CargoModel.hazardous_material,
        CargoModel.hazardous_class,
        CargoModel.special_handling,
        CargoModel.fragility_level,
        CargoModel.storage_duration,
        CargoModel.expiration_date,
        CargoModel.status,
        CargoModel.warehouse_id,
        CargoModel.location_in_warehouse,
        CargoModel.created_at,
        CargoModel.updated_at,
    ]
    
    # Fields that can be edited
    form_columns = [
        CargoModel.tracking_number,
        CargoModel.cargo_type,
        CargoModel.name,
        CargoModel.description,
        CargoModel.weight,
        CargoModel.volume,
        CargoModel.value,
        CargoModel.insurance_amount,
        CargoModel.hazardous_material,
        CargoModel.hazardous_class,
        CargoModel.fragility_level,
        CargoModel.storage_duration,
        CargoModel.status,
        CargoModel.warehouse_id,
        CargoModel.location_in_warehouse,
    ]
    
    # Fields to search by
    column_searchable_list = [
        CargoModel.tracking_number,
        CargoModel.name,
        CargoModel.warehouse_id,
    ]
    
    # Fields to filter by
    column_filters = [
        CargoModel.cargo_type,
        CargoModel.hazardous_material,
        CargoModel.fragility_level,
        CargoModel.status,
        CargoModel.created_at,
    ]
    
    # Customize form field options
    form_choices = {
        CargoModel.cargo_type: [
            (CargoType.GENERAL, "General"),
            (CargoType.HAZARDOUS, "Hazardous"),
            (CargoType.PERISHABLE, "Perishable"),
            (CargoType.FRAGILE, "Fragile"),
            (CargoType.OVERSIZED, "Oversized"),
            (CargoType.REFRIGERATED, "Refrigerated"),
        ],
        CargoModel.fragility_level: [
            (FragilityLevel.LOW, "Low"),
            (FragilityLevel.MEDIUM, "Medium"),
            (FragilityLevel.HIGH, "High"),
            (FragilityLevel.EXTREME, "Extreme"),
        ],
        CargoModel.status: [
            (CargoStatus.RECEIVED, "Received"),
            (CargoStatus.STORED, "Stored"),
            (CargoStatus.LOADING, "Loading"),
            (CargoStatus.SHIPPED, "Shipped"),
            (CargoStatus.DELIVERED, "Delivered"),
            (CargoStatus.DAMAGED, "Damaged"),
            (CargoStatus.LOST, "Lost"),
        ]
    }
    
    def is_accessible(self, request: Request) -> bool:
        # Проверяем, что пользователь аутентифицирован и имеет роль admin
        user_role = request.session.get("role")
        return user_role == "admin"


class CompatibilityReportAdmin(ModelView, model=CompatibilityReportModel):
    """Admin interface for CompatibilityReport model"""
    name = "Compatibility Report"
    name_plural = "Compatibility Reports"
    icon = "fa-solid fa-check-circle"
    
    # Fields to display in the list view
    column_list = [
        CompatibilityReportModel.id,
        CompatibilityReportModel.cargo_id,
        CompatibilityReportModel.vehicle_id,
        CompatibilityReportModel.is_compatible,
        CompatibilityReportModel.score,
        CompatibilityReportModel.created_at,
    ]
    
    # Fields to display in the detail view
    column_details_list = [
        CompatibilityReportModel.id,
        CompatibilityReportModel.cargo_id,
        CompatibilityReportModel.vehicle_id,
        CompatibilityReportModel.is_compatible,
        CompatibilityReportModel.score,
        CompatibilityReportModel.weight_compatible,
        CompatibilityReportModel.volume_compatible,
        CompatibilityReportModel.temperature_compatible,
        CompatibilityReportModel.hazardous_compatible,
        CompatibilityReportModel.special_requirements_met,
        CompatibilityReportModel.risks,
        CompatibilityReportModel.recommendations,
        CompatibilityReportModel.created_at,
    ]
    
    # Fields that can be edited
    form_columns = [
        CompatibilityReportModel.cargo_id,
        CompatibilityReportModel.vehicle_id,
        CompatibilityReportModel.is_compatible,
        CompatibilityReportModel.score,
        CompatibilityReportModel.weight_compatible,
        CompatibilityReportModel.volume_compatible,
        CompatibilityReportModel.temperature_compatible,
        CompatibilityReportModel.hazardous_compatible,
        CompatibilityReportModel.special_requirements_met,
    ]
    
    # Fields to search by
    column_searchable_list = [
        CompatibilityReportModel.cargo_id,
        CompatibilityReportModel.vehicle_id,
    ]
    
    # Fields to filter by
    column_filters = [
        CompatibilityReportModel.is_compatible,
        CompatibilityReportModel.created_at,
    ]
    
    def is_accessible(self, request: Request) -> bool:
        # Проверяем, что пользователь аутентифицирован и имеет роль admin
        user_role = request.session.get("role")
        return user_role == "admin"


class InventoryAdmin(ModelView, model=InventoryModel):
    """Admin interface for Inventory model"""
    name = "Inventory"
    name_plural = "Inventory"
    icon = "fa-solid fa-clipboard-list"
    
    # Fields to display in the list view
    column_list = [
        InventoryModel.id,
        InventoryModel.warehouse_id,
        InventoryModel.cargo_id,
        InventoryModel.quantity,
        InventoryModel.location,
        InventoryModel.status,
        InventoryModel.received_at,
    ]
    
    # Fields to display in the detail view
    column_details_list = [
        InventoryModel.id,
        InventoryModel.warehouse_id,
        InventoryModel.cargo_id,
        InventoryModel.quantity,
        InventoryModel.location,
        InventoryModel.received_at,
        InventoryModel.expected_ship_date,
        InventoryModel.status,
        InventoryModel.created_at,
        InventoryModel.updated_at,
    ]
    
    # Fields that can be edited
    form_columns = [
        InventoryModel.warehouse_id,
        InventoryModel.cargo_id,
        InventoryModel.quantity,
        InventoryModel.location,
        InventoryModel.expected_ship_date,
        InventoryModel.status,
    ]
    
    # Fields to search by
    column_searchable_list = [
        InventoryModel.warehouse_id,
        InventoryModel.cargo_id,
        InventoryModel.location,
    ]
    
    # Fields to filter by
    column_filters = [
        InventoryModel.status,
        InventoryModel.received_at,
        InventoryModel.created_at,
    ]
    
    def is_accessible(self, request: Request) -> bool:
        # Проверяем, что пользователь аутентифицирован и имеет роль admin
        user_role = request.session.get("role")
        return user_role == "admin"


def setup_admin(app, engine):
    """Setup admin panel with authentication"""
    admin = Admin(app, engine, authentication_backend=get_admin_auth())
    admin.add_view(WarehouseAdmin)
    admin.add_view(CargoAdmin)
    admin.add_view(CompatibilityReportAdmin)
    admin.add_view(InventoryAdmin)
    return admin 