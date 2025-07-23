from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from entities.route_assignment import RouteAssignment, RouteAssignmentCreate, RouteAssignmentUpdate, RouteAssignmentStatus
from entities.database_models import RouteAssignment as RouteAssignmentModel
from repositories.interfaces.route_assignment_repository import IRouteAssignmentRepository


class RouteAssignmentRepository(IRouteAssignmentRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create(self, assignment: RouteAssignmentCreate) -> RouteAssignment:
        db_assignment = RouteAssignmentModel(
            route_id=assignment.route_id,
            vehicle_id=assignment.vehicle_id,
            driver_id=assignment.driver_id,
            estimated_duration_hours=assignment.estimated_duration_hours,
            notes=assignment.notes
        )
        
        self.db_session.add(db_assignment)
        self.db_session.commit()
        self.db_session.refresh(db_assignment)
        
        return RouteAssignment(
            id=db_assignment.id,
            route_id=db_assignment.route_id,
            vehicle_id=db_assignment.vehicle_id,
            driver_id=db_assignment.driver_id,
            status=db_assignment.status,
            assigned_at=db_assignment.assigned_at,
            started_at=db_assignment.started_at,
            completed_at=db_assignment.completed_at,
            estimated_duration_hours=db_assignment.estimated_duration_hours,
            actual_duration_hours=db_assignment.actual_duration_hours,
            notes=db_assignment.notes,
            created_at=db_assignment.created_at,
            updated_at=db_assignment.updated_at
        )
    
    def get_by_id(self, assignment_id: UUID) -> Optional[RouteAssignment]:
        db_assignment = self.db_session.query(RouteAssignmentModel).filter(RouteAssignmentModel.id == assignment_id).first()
        if not db_assignment:
            return None
        
        return RouteAssignment(
            id=db_assignment.id,
            route_id=db_assignment.route_id,
            vehicle_id=db_assignment.vehicle_id,
            driver_id=db_assignment.driver_id,
            status=db_assignment.status,
            assigned_at=db_assignment.assigned_at,
            started_at=db_assignment.started_at,
            completed_at=db_assignment.completed_at,
            estimated_duration_hours=db_assignment.estimated_duration_hours,
            actual_duration_hours=db_assignment.actual_duration_hours,
            notes=db_assignment.notes,
            created_at=db_assignment.created_at,
            updated_at=db_assignment.updated_at
        )
    
    def get_by_route_id(self, route_id: UUID) -> List[RouteAssignment]:
        db_assignments = self.db_session.query(RouteAssignmentModel).filter(RouteAssignmentModel.route_id == route_id).all()
        return [
            RouteAssignment(
                id=assignment.id,
                route_id=assignment.route_id,
                vehicle_id=assignment.vehicle_id,
                driver_id=assignment.driver_id,
                status=assignment.status,
                assigned_at=assignment.assigned_at,
                started_at=assignment.started_at,
                completed_at=assignment.completed_at,
                estimated_duration_hours=assignment.estimated_duration_hours,
                actual_duration_hours=assignment.actual_duration_hours,
                notes=assignment.notes,
                created_at=assignment.created_at,
                updated_at=assignment.updated_at
            )
            for assignment in db_assignments
        ]
    
    def get_by_vehicle_id(self, vehicle_id: UUID) -> List[RouteAssignment]:
        db_assignments = self.db_session.query(RouteAssignmentModel).filter(RouteAssignmentModel.vehicle_id == vehicle_id).all()
        return [
            RouteAssignment(
                id=assignment.id,
                route_id=assignment.route_id,
                vehicle_id=assignment.vehicle_id,
                driver_id=assignment.driver_id,
                status=assignment.status,
                assigned_at=assignment.assigned_at,
                started_at=assignment.started_at,
                completed_at=assignment.completed_at,
                estimated_duration_hours=assignment.estimated_duration_hours,
                actual_duration_hours=assignment.actual_duration_hours,
                notes=assignment.notes,
                created_at=assignment.created_at,
                updated_at=assignment.updated_at
            )
            for assignment in db_assignments
        ]
    
    def get_by_driver_id(self, driver_id: UUID) -> List[RouteAssignment]:
        db_assignments = self.db_session.query(RouteAssignmentModel).filter(RouteAssignmentModel.driver_id == driver_id).all()
        return [
            RouteAssignment(
                id=assignment.id,
                route_id=assignment.route_id,
                vehicle_id=assignment.vehicle_id,
                driver_id=assignment.driver_id,
                status=assignment.status,
                assigned_at=assignment.assigned_at,
                started_at=assignment.started_at,
                completed_at=assignment.completed_at,
                estimated_duration_hours=assignment.estimated_duration_hours,
                actual_duration_hours=assignment.actual_duration_hours,
                notes=assignment.notes,
                created_at=assignment.created_at,
                updated_at=assignment.updated_at
            )
            for assignment in db_assignments
        ]
    
    def update(self, assignment_id: UUID, assignment: RouteAssignmentUpdate) -> Optional[RouteAssignment]:
        db_assignment = self.db_session.query(RouteAssignmentModel).filter(RouteAssignmentModel.id == assignment_id).first()
        if not db_assignment:
            return None
        
        update_data = assignment.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_assignment, field, value)
        
        db_assignment.updated_at = datetime.utcnow()
        self.db_session.commit()
        self.db_session.refresh(db_assignment)
        
        return RouteAssignment(
            id=db_assignment.id,
            route_id=db_assignment.route_id,
            vehicle_id=db_assignment.vehicle_id,
            driver_id=db_assignment.driver_id,
            status=db_assignment.status,
            assigned_at=db_assignment.assigned_at,
            started_at=db_assignment.started_at,
            completed_at=db_assignment.completed_at,
            estimated_duration_hours=db_assignment.estimated_duration_hours,
            actual_duration_hours=db_assignment.actual_duration_hours,
            notes=db_assignment.notes,
            created_at=db_assignment.created_at,
            updated_at=db_assignment.updated_at
        )
    
    def delete(self, assignment_id: UUID) -> bool:
        db_assignment = self.db_session.query(RouteAssignmentModel).filter(RouteAssignmentModel.id == assignment_id).first()
        if not db_assignment:
            return False
        
        self.db_session.delete(db_assignment)
        self.db_session.commit()
        return True
    
    def get_all(self) -> List[RouteAssignment]:
        db_assignments = self.db_session.query(RouteAssignmentModel).all()
        return [
            RouteAssignment(
                id=assignment.id,
                route_id=assignment.route_id,
                vehicle_id=assignment.vehicle_id,
                driver_id=assignment.driver_id,
                status=assignment.status,
                assigned_at=assignment.assigned_at,
                started_at=assignment.started_at,
                completed_at=assignment.completed_at,
                estimated_duration_hours=assignment.estimated_duration_hours,
                actual_duration_hours=assignment.actual_duration_hours,
                notes=assignment.notes,
                created_at=assignment.created_at,
                updated_at=assignment.updated_at
            )
            for assignment in db_assignments
        ]
    
    def get_by_status(self, status: str) -> List[RouteAssignment]:
        db_assignments = self.db_session.query(RouteAssignmentModel).filter(RouteAssignmentModel.status == status).all()
        return [
            RouteAssignment(
                id=assignment.id,
                route_id=assignment.route_id,
                vehicle_id=assignment.vehicle_id,
                driver_id=assignment.driver_id,
                status=assignment.status,
                assigned_at=assignment.assigned_at,
                started_at=assignment.started_at,
                completed_at=assignment.completed_at,
                estimated_duration_hours=assignment.estimated_duration_hours,
                actual_duration_hours=assignment.actual_duration_hours,
                notes=assignment.notes,
                created_at=assignment.created_at,
                updated_at=assignment.updated_at
            )
            for assignment in db_assignments
        ] 