import logging

class DatabaseLogHandler(logging.Handler):

    """
    Sending logs and exceptions to the database
    """
    def emit(self, record):

        try:
            #user = getattr(record, 'user', None)
            from django.utils.timezone import now
            from app.models import ActivityLog
            
            ActivityLog.objects.create(
                #user = user if user and hasattr(user, 'is_authenticated') and user.is_authenticated else None,
                level = record.levelname,
                action = record.levelname,
                path = getattr(record, 'path', None),
                method = getattr(record, 'method', None),
                timestamp = now(),
            )
        except Exception as e:
            print(f"Error : {e}")