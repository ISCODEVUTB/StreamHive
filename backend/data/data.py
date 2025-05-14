from backend.logic.schemas.profiles import CreateProfile
from backend.logic.schemas.users import CreateUser
from backend.core.config import settings


user_test_lists = [
    CreateUser(
        full_name='Alex',
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        user_type='admin',
        birth_date='2005-09-15',
        user_gender='male'
    ),

    CreateUser(
        full_name='Ana',
        email='ana@hotmail.com',
        password='password1234',
        user_type='admin',
        birth_date='2005-09-15',
        user_gender='female'
    )
]

profile_list_test = [
    CreateProfile(
        username='alex',
        description='Amante del cine de acción, siempre buscando nuevas recomendaciones.',
        profile_role='editor'
    ),
    
    CreateProfile(
        username='ana',
        description='Amante del cine de acción, siempre buscando nuevas recomendaciones.',
        profile_role='editor'
    )
]