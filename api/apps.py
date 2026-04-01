from django.apps import AppConfig



class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        """
        Import all models when the app is ready.
        This ensures models are registered with Django.
        Note: Add new models here when created.
        """
        import api.UserProfile
        import api.Department.model
        import api.Designation.model
        import api.AttendanceStatus.model
        
        import api.Attendance.model
        import api.Leave.model     
        import api.YearMaster.model
        import api.salary.model
        import api.Chat.model
   
     
        
        

        