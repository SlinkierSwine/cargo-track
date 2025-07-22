from sqladmin import Admin, ModelView
from entities.database_models import UserModel
from entities.user import UserRole


class UserAdmin(ModelView, model=UserModel):
    """Admin interface for User model"""
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-users"
    
    # Fields to display in the list view
    column_list = [
        UserModel.id,
        UserModel.email,
        UserModel.username,
        UserModel.role,
        UserModel.is_active,
        UserModel.first_name,
        UserModel.last_name,
        UserModel.created_at,
        UserModel.updated_at,
    ]
    
    # Fields to display in the detail view
    column_details_list = [
        UserModel.id,
        UserModel.email,
        UserModel.username,
        UserModel.role,
        UserModel.is_active,
        UserModel.first_name,
        UserModel.last_name,
        UserModel.created_at,
        UserModel.updated_at,
    ]
    
    # Fields that can be edited
    form_columns = [
        UserModel.email,
        UserModel.username,
        UserModel.role,
        UserModel.is_active,
        UserModel.first_name,
        UserModel.last_name,
    ]
    
    # Fields to search by
    column_searchable_list = [
        UserModel.email,
        UserModel.username,
        UserModel.first_name,
        UserModel.last_name,
    ]
    
    # Fields to filter by
    column_filters = [
        UserModel.role,
        UserModel.is_active,
        UserModel.created_at,
    ]
    
    # Customize form field options
    form_choices = {
        UserModel.role: [
            (UserRole.ADMIN, "Admin"),
            (UserRole.DISPATCHER, "Dispatcher"),
            (UserRole.DRIVER, "Driver"),
            (UserRole.CLIENT, "Client"),
        ]
    }


def setup_admin(app, engine):
    """Setup admin panel"""
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    return admin 