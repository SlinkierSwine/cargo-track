# Fleet Service - Business Logic Planning

## 1. Vehicle Management Requirements

### Vehicle Registration and Information
- Vehicle registration with unique identification
- Vehicle type classification (truck, van, trailer, etc.)
- License plate number and registration details
- Vehicle specifications (capacity, dimensions, fuel type)
- Maintenance history and service records
- Insurance and registration expiration tracking
- Vehicle status (active, maintenance, retired, etc.)

### Vehicle Capacity and Capabilities
- Maximum cargo weight capacity
- Volume capacity (cubic meters)
- Special equipment (refrigeration, hazardous materials, etc.)
- Route restrictions (city center access, bridge weight limits)
- Fuel efficiency and range
- Operating costs per kilometer

## 2. Driver Management Requirements

### Driver Registration and Information
- Driver personal information (name, contact details, license)
- Driver license information and expiration
- Medical certificate and health status
- Work experience and qualifications
- Emergency contact information
- Employment status (active, on leave, terminated)

### Driver Qualifications and Certifications
- Driver license class and endorsements
- Special certifications (hazardous materials, oversized loads)
- Training records and certifications
- Language skills for international routes
- Route familiarity and experience

### Driver Availability and Scheduling
- Work schedule and availability
- Rest periods and compliance with driving regulations
- Vacation and leave management
- Emergency contact procedures
- Performance tracking and evaluation

## 3. Route Assignment Logic

### Route Planning and Optimization
- Distance calculation and route optimization
- Traffic conditions and estimated travel time
- Fuel consumption estimation
- Rest stops and driver breaks
- Border crossings and customs procedures

### Assignment Criteria
- Vehicle availability and suitability for cargo
- Driver availability and qualifications
- Route complexity and driver experience
- Vehicle capacity vs. cargo requirements
- Cost optimization (fuel, maintenance, driver costs)

### Assignment Process
- Automatic assignment based on criteria
- Manual override for special cases
- Conflict resolution for multiple assignments
- Assignment confirmation and notification
- Route modification and reassignment

## 4. API Endpoints Design

### Vehicle Management Endpoints
```
GET /fleet/vehicles
- List all vehicles
- Request: access token, filters (status, type, capacity)
- Response: list of vehicles with details

GET /fleet/vehicles/{vehicle_id}
- Get vehicle details
- Request: access token, vehicle_id
- Response: vehicle information

POST /fleet/vehicles
- Register new vehicle
- Request: access token, vehicle data
- Response: created vehicle

PUT /fleet/vehicles/{vehicle_id}
- Update vehicle information
- Request: access token, vehicle_id, updated fields
- Response: updated vehicle

DELETE /fleet/vehicles/{vehicle_id}
- Deactivate vehicle
- Request: access token, vehicle_id
- Response: success message

GET /fleet/vehicles/{vehicle_id}/maintenance
- Get vehicle maintenance history
- Request: access token, vehicle_id
- Response: maintenance records

POST /fleet/vehicles/{vehicle_id}/maintenance
- Add maintenance record
- Request: access token, vehicle_id, maintenance data
- Response: created maintenance record
```

### Driver Management Endpoints
```
GET /fleet/drivers
- List all drivers
- Request: access token, filters (status, qualifications)
- Response: list of drivers with details

GET /fleet/drivers/{driver_id}
- Get driver details
- Request: access token, driver_id
- Response: driver information

POST /fleet/drivers
- Register new driver
- Request: access token, driver data
- Response: created driver

PUT /fleet/drivers/{driver_id}
- Update driver information
- Request: access token, driver_id, updated fields
- Response: updated driver

DELETE /fleet/drivers/{driver_id}
- Deactivate driver
- Request: access token, driver_id
- Response: success message

GET /fleet/drivers/{driver_id}/schedule
- Get driver schedule
- Request: access token, driver_id, date range
- Response: schedule information

PUT /fleet/drivers/{driver_id}/availability
- Update driver availability
- Request: access token, driver_id, availability data
- Response: updated availability
```

### Route Assignment Endpoints
```
GET /fleet/assignments
- List route assignments
- Request: access token, filters (status, date range)
- Response: list of assignments

GET /fleet/assignments/{assignment_id}
- Get assignment details
- Request: access token, assignment_id
- Response: assignment information

POST /fleet/assignments
- Create new assignment
- Request: access token, assignment data (route, vehicle, driver)
- Response: created assignment

PUT /fleet/assignments/{assignment_id}
- Update assignment
- Request: access token, assignment_id, updated fields
- Response: updated assignment

DELETE /fleet/assignments/{assignment_id}
- Cancel assignment
- Request: access token, assignment_id
- Response: success message

POST /fleet/assignments/auto-assign
- Automatic assignment for route
- Request: access token, route data
- Response: suggested assignment

GET /fleet/assignments/available-vehicles
- Get available vehicles for route
- Request: access token, route requirements
- Response: list of suitable vehicles

GET /fleet/assignments/available-drivers
- Get available drivers for route
- Request: access token, route requirements
- Response: list of suitable drivers
```

### Health and Status Endpoints
```
GET /fleet/health
- Service health check
- Response: service status

GET /fleet/status
- Fleet service status
- Response: detailed service info

GET /fleet/statistics
- Fleet statistics
- Request: access token, date range
- Response: fleet performance metrics
```

## 5. Data Models

### Vehicle Model
```python
class Vehicle:
    id: UUID
    license_plate: str
    vehicle_type: VehicleType
    brand: str
    model: str
    year: int
    capacity_weight: float  # kg
    capacity_volume: float  # m³
    fuel_type: FuelType
    fuel_efficiency: float  # km/l
    status: VehicleStatus
    insurance_expiry: datetime
    registration_expiry: datetime
    created_at: datetime
    updated_at: datetime
```

### Driver Model
```python
class Driver:
    id: UUID
    user_id: UUID  # Reference to auth service
    first_name: str
    last_name: str
    license_number: str
    license_class: str
    license_expiry: datetime
    medical_certificate_expiry: datetime
    phone: str
    email: str
    emergency_contact: str
    status: DriverStatus
    qualifications: List[str]
    created_at: datetime
    updated_at: datetime
```

### Assignment Model
```python
class Assignment:
    id: UUID
    route_id: UUID  # Reference to orders service
    vehicle_id: UUID
    driver_id: UUID
    status: AssignmentStatus
    assigned_at: datetime
    start_time: datetime
    end_time: datetime
    actual_start_time: Optional[datetime]
    actual_end_time: Optional[datetime]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
```

### Maintenance Record Model
```python
class MaintenanceRecord:
    id: UUID
    vehicle_id: UUID
    maintenance_type: MaintenanceType
    description: str
    cost: float
    performed_at: datetime
    next_maintenance_date: Optional[datetime]
    service_provider: str
    created_at: datetime
```

## 6. Business Rules and Constraints

### Vehicle Assignment Rules
- Vehicle must be active and not in maintenance
- Vehicle capacity must meet cargo requirements
- Vehicle must be available for the assignment period
- Vehicle must be suitable for the route type

### Driver Assignment Rules
- Driver must be active and available
- Driver must have required qualifications for the route
- Driver must comply with rest period regulations
- Driver must be familiar with the route or have appropriate training

### Assignment Validation
- No double booking of vehicles or drivers
- Assignment must be within driver's working hours
- Route must be feasible with assigned vehicle
- Cost optimization must be considered

## 7. Integration Points

### Event Publishing
- Vehicle registered event
- Vehicle status changed event
- Driver registered event
- Driver status changed event
- Assignment created event
- Assignment status changed event
- Assignment completed event

### External Service Dependencies
- Auth service for driver authentication and user management
- Orders service for route information and cargo details
- Warehouse service for cargo compatibility validation
- Notification service for assignment notifications
- Finance service for cost calculations

## 8. Error Handling

### Vehicle Errors
- Vehicle not found
- Vehicle not available
- Vehicle capacity insufficient
- Vehicle maintenance required
- Vehicle registration expired

### Driver Errors
- Driver not found
- Driver not available
- Driver qualifications insufficient
- Driver license expired
- Driver rest period violation

### Assignment Errors
- No suitable vehicle available
- No suitable driver available
- Assignment conflicts
- Route not feasible
- Assignment validation failed

### System Errors
- Database connection issues
- External service unavailable
- Assignment algorithm failures
- Notification delivery failures 