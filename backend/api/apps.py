from django.apps import AppConfig



class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        import api.UserProfile
        import api.Department.model
        import api.AttendanceStatus.model
        import api.Attendance.model
        import api.Leave.model     
        import api.YearMaster.model
        import api.salary.model
   
     
        
        

        