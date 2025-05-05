from sqlmodel import SQLModel, Session
from backend.logic.controllers import profiles, users
from backend.logic.schemas.profiles import CreateProfile
from backend.logic.schemas.users import CreateUser
from backend.core.config import settings


user_test_lists = [CreateUser(
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
    ),

    CreateUser(
        full_name='Juan Pérez',
        email='juan.perez@example.com', 
        password='password_1',
        birth_date='1990-05-15',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Maria García',
        email='maria.garcia@example.com', 
        password='password_2',
        birth_date='1985-07-22',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Carlos López',
        email='carlos.lopez@example.com', 
        password='password_3',
        birth_date='1992-10-30',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Laura Martínez',
        email='laura.martinez@example.com', 
        password='password_4',
        birth_date='1988-02-13',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Pedro Rodríguez',
        email='pedro.rodriguez@example.com', 
        password='password_5',
        birth_date='1995-04-02',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Ana Fernández',
        email='ana.fernandez@example.com', 
        password='password_6',
        birth_date='1993-12-09',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Luis González',
        email='luis.gonzalez@example.com', 
        password='password_7',
        birth_date='1990-03-25',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Sofía Hernández',
        email='sofia.hernandez@example.com', 
        password='password_8',
        birth_date='1994-08-17',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='David Pérez',
        email='david.perez@example.com', 
        password='password_9',
        birth_date='1991-06-30',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Patricia Díaz',
        email='patricia.diaz@example.com', 
        password='password_10',
        birth_date='1987-11-14',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Javier Torres',
        email='javier.torres@example.com', 
        password='password_11',
        birth_date='1997-03-04',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Elena Ruiz',
        email='elena.ruiz@example.com', 
        password='password_12',
        birth_date='1992-09-16',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Gabriel Sánchez',
        email='gabriel.sanchez@example.com', 
        password='password_13',
        birth_date='1989-01-05',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Marta Pérez',
        email='marta.perez@example.com', 
        password='password_14',
        birth_date='1996-05-25',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Antonio Gómez',
        email='antonio.gomez@example.com', 
        password='password_15',
        birth_date='1984-07-30',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Carmen López',
        email='carmen.lopez@example.com', 
        password='password_16',
        birth_date='1999-04-19',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Fernando Ramírez',
        email='fernando.ramirez@example.com', 
        password='password_17',
        birth_date='1991-11-10',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Isabel Martínez',
        email='isabel.martinez@example.com', 
        password='password_18',
        birth_date='1986-12-20',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Raúl Gómez',
        email='raul.gomez@example.com', 
        password='password_19',
        birth_date='1994-03-03',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Sandra Rodríguez',
        email='sandra.rodriguez@example.com', 
        password='password_20',
        birth_date='1990-08-18',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Héctor Sánchez',
        email='hector.sanchez@example.com', 
        password='password_21',
        birth_date='1988-10-22',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Verónica Fernández',
        email='veronica.fernandez@example.com', 
        password='password_22',
        birth_date='1995-09-12',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Juanita Díaz',
        email='juanita.diaz@example.com', 
        password='password_23',
        birth_date='1992-01-07',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Marco González',
        email='marco.gonzalez@example.com', 
        password='password_24',
        birth_date='1989-11-23',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Cristina Torres',
        email='cristina.torres@example.com', 
        password='password_25',
        birth_date='1996-06-11',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Raquel Sánchez',
        email='raquel.sanchez@example.com', 
        password='password_26',
        birth_date='1991-04-14',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Carlos Ruiz',
        email='carlos.ruiz@example.com', 
        password='password_27',
        birth_date='1987-02-28',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Patricia Gómez',
        email='patricia.gomez@example.com', 
        password='password_28',
        birth_date='1993-10-05',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Victor Hernández',
        email='victor.hernandez@example.com', 
        password='password_29',
        birth_date='1990-09-19',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Sofía Díaz',
        email='sofia.diaz@example.com', 
        password='password_30',
        birth_date='1994-07-13',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Miguel Fernández',
        email='miguel.fernandez@example.com', 
        password='password_31',
        birth_date='1986-03-24',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Martín Rodríguez',
        email='martin.rodriguez@example.com', 
        password='password_32',
        birth_date='1995-02-16',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Rosa Ramírez',
        email='rosa.ramirez@example.com', 
        password='password_33',
        birth_date='1988-05-09',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Oscar Martínez',
        email='oscar.martinez@example.com', 
        password='password_34',
        birth_date='1993-08-23',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Juliana López',
        email='juliana.lopez@example.com', 
        password='password_35',
        birth_date='1990-11-17',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Joaquín Pérez',
        email='joaquin.perez@example.com', 
        password='password_36',
        birth_date='1997-05-07',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Lidia Sánchez',
        email='lidia.sanchez@example.com', 
        password='password_37',
        birth_date='1992-01-24',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Víctor Gómez',
        email='victor.gomez@example.com', 
        password='password_38',
        birth_date='1991-08-11',
        user_gender='male',
        user_type='external'
    ),

    CreateUser(
        full_name='Eva Torres',
        email='eva.torres@example.com', 
        password='password_39',
        birth_date='1994-09-04',
        user_gender='female',
        user_type='external'
    ),

    CreateUser(
        full_name='Manuel Ruiz',
        email='manuel.ruiz@example.com', 
        password='password_40',
        birth_date='1985-12-27',
        user_gender='male',
        user_type='external'
    ),
]

profile_list_test = [CreateProfile(
        username='alex',
        description='Amante del cine de acción, siempre buscando nuevas recomendaciones.',
        profile_role='editor'
    ),
    
    CreateProfile(
        username='ana',
        description='Amante del cine de acción, siempre buscando nuevas recomendaciones.',
        profile_role='editor'
    ),

    CreateProfile(
        username='juanperez',
        description='Amante del cine de acción, siempre buscando nuevas recomendaciones.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='mariagarcia',
        description='Fascinada por los clásicos, mis noches siempre son de películas.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='carloslopez',
        description='Fanático de las películas de suspenso y terror, siempre en busca del siguiente thriller.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='lauramartinez',
        description='Soy la reina de las comedias románticas, ¡nada mejor que reír y enamorarse al mismo tiempo!',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='pedrorodriguez',
        description='Cineasta en potencia, me encanta explorar diferentes géneros cinematográficos.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='anafernandez',
        description='Mi pasión son las películas de aventuras, ¡me encanta vivir grandes historias desde el sofá!',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='luisgonzalez',
        description='Amante de los superhéroes, nunca me pierdo una película de Marvel.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='sofiahernandez',
        description='Mis fines de semana son para maratones de películas de ciencia ficción y fantasía.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='davidperez',
        description='Me encanta el cine independiente, siempre en busca de nuevas joyas del séptimo arte.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='patriciadiaz',
        description='Feliz de ver todo tipo de películas, pero las de acción siempre ganan.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='javiertorres',
        description='Disfruto de las películas nostálgicas de los años 80s y 90s, ¡las mejores décadas del cine!',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='elenaruiz',
        description='Las películas animadas siempre me emocionan, soy un fan de los grandes estudios de animación.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='gabrielsanchez',
        description='Me encanta descubrir películas raras y de culto, esas que pocos conocen pero todos deberían ver.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='martaperez',
        description='Siempre estoy buscando la próxima película que me haga reír hasta llorar.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='antoniogomez',
        description='Adicto a las películas de ciencia ficción, siempre quiero ver lo que vendrá en el futuro del cine.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='carmenlopez',
        description='Fan de los musicales, siempre me encuentro cantando las canciones de mis películas favoritas.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='fernandoramirez',
        description='El cine europeo tiene algo especial, siempre me pierdo en sus historias profundas.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='isabelmartinez',
        description='Adoro las películas de misterio y siempre trato de resolver el enigma antes de que termine el film.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='raulgomez',
        description='Las películas históricas me hacen viajar al pasado, ¡me encantan las historias basadas en hechos reales!',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='sandrarodriguez',
        description='Siempre estoy buscando nuevas películas para ver con mi familia, ¡el cine en compañía es lo mejor!',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='hectorsanchez',
        description='Disfruto del cine internacional, me encanta ver películas de diferentes culturas.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='veronicafernandez',
        description='Mis películas favoritas son las de terror psicológico, ¡me encanta sentir ese escalofrío!',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='juanita_diaz',
        description='Mi vida no es la misma sin una buena comedia, siempre tengo que reírme un rato.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='marcogonzalez',
        description='Cine de autor, siempre buscando lo diferente y lo interesante en cada película.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='cristinatorres',
        description='Las películas de acción son mi pasión, siempre buscando las más intensas.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='raquelsanchez',
        description='El cine fantástico me transporta a mundos increíbles, ¡me encanta escapar de la realidad!',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='carlosruiz',
        description='Me gustan las películas de aventuras, siempre estoy en busca de una nueva travesía épica.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='patriciagomez',
        description='Cine de autor y documentales, me gusta ver historias reales contadas de una forma única.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='victorhernandez',
        description='El cine de superhéroes es mi debilidad, ¡me encanta ver a los héroes salvar el mundo!',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='sofiadiaz',
        description='Siempre busco la película perfecta para ver en una noche tranquila, ¡me encanta el cine en casa!',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='miguelfernandez',
        description='Las películas de terror clásico siempre logran ponerme los pelos de punta.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='martinrodriguez',
        description='Me encanta el cine de aventuras épicas, siempre soñando con ser el héroe de una historia.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='rosaramirez',
        description='Disfruto de las comedias, ¡nada mejor que reírme mientras veo una película!',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='oscar_martinez',
        description='Adicto a las películas de ciencia ficción y todo lo relacionado con el futuro.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='julianalopez',
        description='Mis días no están completos sin una película de drama que me haga reflexionar.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='joaquinperez',
        description='Soy fan de los documentales sobre la naturaleza, ¡me encanta aprender sobre el mundo natural!',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='lidiasanchez',
        description='Siempre estoy buscando la próxima gran historia de fantasía que me haga volar la imaginación.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='victorgomez',
        description='Las películas sobre el espacio y los planetas son mi verdadera pasión.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='evatorres',
        description='Me encanta ver películas de romance y perderme en historias de amor épicas.',
        profile_role='subscriber'
    ),

    CreateProfile(
        username='manuelruiz',
        description='Las películas de acción son mi debilidad, siempre busco adrenalina y emoción.',
        profile_role='subscriber'
    )
]