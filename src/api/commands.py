
# import click
# from api.models import db, User

# """
# In this file, you can add as many commands as you want using the @app.cli.command decorator
# Flask commands are usefull to run cronjobs or tasks outside of the API but sill in integration 
# with youy database, for example: Import the price of bitcoin every night as 12am
# """
# def setup_commands(app):
    
#     """ 
#     This is an example command "insert-test-users" that you can run from the command line
#     by typing: $ flask insert-test-users 5
#     Note: 5 is the number of users to add
#     """
#     @app.cli.command("insert-test-users") # name of our command
#     @click.argument("count") # argument of out command
#     def insert_test_users(count):
#         print("Creating test users")
#         for x in range(1, int(count) + 1):
#             user = User()
#             user.email = "test_user" + str(x) + "@test.com"
#             user.password = "123456"
#             user.is_active = True
#             db.session.add(user)
#             db.session.commit()
#             print("User: ", user.email, " created.")

#         print("All test users created")

#     @app.cli.command("insert-test-data")
#     def insert_test_data():
#         pass

import click
from api.models import db, Role, User, Car, Service, Appointment, Comment, Setting
from flask_bcrypt import Bcrypt
from datetime import datetime

def setup_commands(app):
    bcrypt = Bcrypt(app)

    @app.cli.command("insert-test-data")
    def insert_test_data():
        # Agregar roles
        roles = ['Admin', 'Mechanic', 'User']
        for idx, role_name in enumerate(roles, start=1):
            role = Role(id=idx, role_name=role_name)
            db.session.add(role)

        db.session.commit()

        # Agregar usuarios
        users = [
            {"email": "user1@example.com", "password": "123123", "name": "User One", "phone_number": "1234567890", "role_id": 3},
            {"email": "user2@example.com", "password": "password2", "name": "User Two", "phone_number": "0987654321", "role_id": 3},
            {"email": "user3@example.com", "password": "password3", "name": "User Three", "phone_number": "1122334455", "role_id": 3},
            {"email": "user4@example.com", "password": "password4", "name": "User Four", "phone_number": "2233445566", "role_id": 3},
            {"email": "user5@example.com", "password": "password5", "name": "User Five", "phone_number": "3344556677", "role_id": 3},
            {"email": "user6@example.com", "password": "password6", "name": "User Six", "phone_number": "4455667788", "role_id": 3},
            {"email": "user7@example.com", "password": "password7", "name": "User Seven", "phone_number": "5566778899", "role_id": 3},
            {"email": "user8@example.com", "password": "password8", "name": "User Eight", "phone_number": "6677889900", "role_id": 3},
            {"email": "user9@example.com", "password": "password9", "name": "User Nine", "phone_number": "7788990011", "role_id": 3},
            {"email": "user10@example.com", "password": "password10", "name": "User Ten", "phone_number": "8899001122", "role_id": 3},
            {"email": "user11@example.com", "password": "password11", "name": "User Eleven", "phone_number": "9900112233", "role_id": 3},
            {"email": "user12@example.com", "password": "password12", "name": "User Twelve", "phone_number": "1234567890", "role_id": 3},
            {"email": "user13@example.com", "password": "password13", "name": "User Thirteen", "phone_number": "0987654321", "role_id": 3},
            {"email": "user14@example.com", "password": "password14", "name": "User Fourteen", "phone_number": "1122334455", "role_id": 3},
            {"email": "user15@example.com", "password": "password15", "name": "User Fifteen", "phone_number": "2233445566", "role_id": 3},
            {"email": "admin@example.com", "password": "123123", "name": "Admin User", "phone_number": "1231231234", "role_id": 1},
            {"email": "mechanic@example.com", "password": "123123", "name": "Mechanic User", "phone_number": "3213214321", "role_id": 2}
        ]
        user_objects = []
        for user_data in users:
            hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            user = User(
                email=user_data['email'],
                password=hashed_password,
                name=user_data['name'],
                phone_number=user_data['phone_number'],
                role_id=user_data['role_id']
            )
            db.session.add(user)
            user_objects.append(user)

        db.session.commit()

        # Agregar servicios
        services = [
            {"name": "Oil Change", "description": "Standard oil change service", "duration": 1, "slots_required": 1},
            {"name": "Brake Inspection", "description": "Comprehensive brake system inspection", "duration": 1.5, "slots_required": 1},
            {"name": "Tire Rotation", "description": "Rotation of all four tires", "duration": 1, "slots_required": 1}
        ]
        for service_data in services:
            service = Service(
                name=service_data['name'],
                description=service_data['description'],
                duration=service_data['duration'],
                slots_required=service_data['slots_required']
            )
            db.session.add(service)

        db.session.commit()

        # Agregar configuraciones
        setting = Setting(max_appointments_per_hour=4)
        db.session.add(setting)
        db.session.commit()

        # Agregar autos
        cars = [
            {"car_model": "Toyota Corolla", "license_plate": "ABC123", "owner_id": user_objects[0].id},
            {"car_model": "Honda Civic", "license_plate": "XYZ789", "owner_id": user_objects[1].id},
            {"car_model": "Ford Focus", "license_plate": "DEF456", "owner_id": user_objects[2].id},
            {"car_model": "Chevy Malibu", "license_plate": "GHI101", "owner_id": user_objects[3].id},
            {"car_model": "Nissan Altima", "license_plate": "JKL234", "owner_id": user_objects[4].id},
            {"car_model": "BMW 3 Series", "license_plate": "MNO567", "owner_id": user_objects[5].id},
            {"car_model": "Mercedes-Benz C-Class", "license_plate": "PQR890", "owner_id": user_objects[6].id},
            {"car_model": "Audi A4", "license_plate": "STU123", "owner_id": user_objects[7].id},
            {"car_model": "Lexus IS", "license_plate": "VWX456", "owner_id": user_objects[8].id},
            {"car_model": "Hyundai Sonata", "license_plate": "YZA789", "owner_id": user_objects[9].id},
            {"car_model": "Kia Optima", "license_plate": "BCD012", "owner_id": user_objects[10].id},
            {"car_model": "Mazda 3", "license_plate": "EFG345", "owner_id": user_objects[11].id},
            {"car_model": "Subaru Impreza", "license_plate": "HIJ678", "owner_id": user_objects[12].id},
            {"car_model": "Volkswagen Golf", "license_plate": "KLM901", "owner_id": user_objects[13].id},
            {"car_model": "Tesla Model 3", "license_plate": "NOP234", "owner_id": user_objects[14].id},
            # Añadimos más coches para algunos usuarios
            {"car_model": "Ford Fiesta", "license_plate": "FGH567", "owner_id": user_objects[1].id},
            {"car_model": "Chevrolet Camaro", "license_plate": "UVW345", "owner_id": user_objects[2].id},
            {"car_model": "Toyota Camry", "license_plate": "QWE123", "owner_id": user_objects[3].id},
            {"car_model": "Honda Accord", "license_plate": "ASD234", "owner_id": user_objects[4].id},
        ]
        for car_data in cars:
            car = Car(
                car_model=car_data['car_model'],
                license_plate=car_data['license_plate'],
                owner_id=car_data['owner_id']
            )
            db.session.add(car)

        db.session.commit()

        # Agregar citas
        appointments = [
            {"date": "2024-08-10 10:00:00", "user_id": user_objects[0].id, "car_id": 1, "service_id": 1, "status": "pending"},
            {"date": "2024-08-11 11:00:00", "user_id": user_objects[1].id, "car_id": 2, "service_id": 2, "status": "completed"},
            {"date": "2024-08-12 12:00:00", "user_id": user_objects[2].id, "car_id": 3, "service_id": 3, "status": "pending"},
            {"date": "2024-08-13 13:00:00", "user_id": user_objects[3].id, "car_id": 4, "service_id": 1, "status": "cancelled"},
            {"date": "2024-08-14 14:00:00", "user_id": user_objects[4].id, "car_id": 5, "service_id": 2, "status": "completed"},
            {"date": "2024-08-15 15:00:00", "user_id": user_objects[5].id, "car_id": 6, "service_id": 3, "status": "pending"},
            {"date": "2024-08-16 16:00:00", "user_id": user_objects[6].id, "car_id": 7, "service_id": 1, "status": "completed"},
            {"date": "2024-08-17 17:00:00", "user_id": user_objects[7].id, "car_id": 8, "service_id": 2, "status": "pending"},
            {"date": "2024-08-18 18:00:00", "user_id": user_objects[8].id, "car_id": 9, "service_id": 3, "status": "cancelled"},
            {"date": "2024-08-19 19:00:00", "user_id": user_objects[9].id, "car_id": 10, "service_id": 1, "status": "pending"},
            {"date": "2024-08-20 20:00:00", "user_id": user_objects[10].id, "car_id": 11, "service_id": 2, "status": "completed"},
            {"date": "2024-08-21 21:00:00", "user_id": user_objects[11].id, "car_id": 12, "service_id": 1, "status": "pending"},
            {"date": "2024-08-22 22:00:00", "user_id": user_objects[12].id, "car_id": 13, "service_id": 2, "status": "completed"},
            {"date": "2024-08-23 23:00:00", "user_id": user_objects[13].id, "car_id": 14, "service_id": 3, "status": "pending"},
            {"date": "2024-08-24 09:00:00", "user_id": user_objects[14].id, "car_id": 15, "service_id": 1, "status": "cancelled"},
            # Añadimos más citas para mayor variedad
            {"date": "2024-08-24 10:00:00", "user_id": user_objects[1].id, "car_id": 16, "service_id": 1, "status": "pending"},
            {"date": "2024-08-25 11:00:00", "user_id": user_objects[2].id, "car_id": 17, "service_id": 2, "status": "completed"},
            {"date": "2024-08-26 12:00:00", "user_id": user_objects[3].id, "car_id": 18, "service_id": 3, "status": "pending"},
            {"date": "2024-08-27 13:00:00", "user_id": user_objects[4].id, "car_id": 19, "service_id": 1, "status": "cancelled"},
        ]
        for appointment_data in appointments:
            appointment = Appointment(
                date=datetime.strptime(appointment_data['date'], '%Y-%m-%d %H:%M:%S'),
                user_id=appointment_data['user_id'],
                car_id=appointment_data['car_id'],
                service_id=appointment_data['service_id'],
                status=appointment_data['status']
            )
            db.session.add(appointment)

        db.session.commit()

        # Agregar comentarios
        comments = [
            {"content": "Great service!", "author_id": user_objects[0].id, "appointment_id": 1, "is_mechanic": False},
            {"content": "Brake pads replaced.", "author_id": user_objects[1].id, "appointment_id": 2, "is_mechanic": True},
            {"content": "Tire pressure adjusted.", "author_id": user_objects[2].id, "appointment_id": 3, "is_mechanic": True},
            {"content": "Oil change done perfectly.", "author_id": user_objects[3].id, "appointment_id": 4, "is_mechanic": False},
            {"content": "Friendly staff.", "author_id": user_objects[4].id, "appointment_id": 5, "is_mechanic": False},
            {"content": "Great service as always.", "author_id": user_objects[5].id, "appointment_id": 6, "is_mechanic": False},
            {"content": "Quick and efficient.", "author_id": user_objects[6].id, "appointment_id": 7, "is_mechanic": False},
            {"content": "Highly recommend.", "author_id": user_objects[7].id, "appointment_id": 8, "is_mechanic": False},
            {"content": "Very professional.", "author_id": user_objects[8].id, "appointment_id": 9, "is_mechanic": False},
            {"content": "Exceptional service.", "author_id": user_objects[9].id, "appointment_id": 10, "is_mechanic": False},
            {"content": "Best workshop in town.", "author_id": user_objects[10].id, "appointment_id": 11, "is_mechanic": False},
            {"content": "Satisfied with the tire rotation.", "author_id": user_objects[11].id, "appointment_id": 12, "is_mechanic": False},
            {"content": "Brakes feel great.", "author_id": user_objects[12].id, "appointment_id": 13, "is_mechanic": False},
            {"content": "Smooth ride after service.", "author_id": user_objects[13].id, "appointment_id": 14, "is_mechanic": False},
            {"content": "Very efficient.", "author_id": user_objects[14].id, "appointment_id": 15, "is_mechanic": False},
            # Añadimos más comentarios para mayor variedad
            {"content": "Excellent service!", "author_id": user_objects[1].id, "appointment_id": 16, "is_mechanic": False},
            {"content": "Prompt and courteous.", "author_id": user_objects[2].id, "appointment_id": 17, "is_mechanic": False},
            {"content": "Work done well.", "author_id": user_objects[3].id, "appointment_id": 18, "is_mechanic": False},
            {"content": "Had a great experience.", "author_id": user_objects[4].id, "appointment_id": 19, "is_mechanic": False},
            # Comentarios del mecánico
            {"content": "Everything looks good after inspection.", "author_id": user_objects[-1].id, "appointment_id": 1, "is_mechanic": True},
            {"content": "Brake pads replaced.", "author_id": user_objects[-1].id, "appointment_id": 2, "is_mechanic": True},
            {"content": "Tire pressure adjusted.", "author_id": user_objects[-1].id, "appointment_id": 3, "is_mechanic": True},
            {"content": "Oil change completed.", "author_id": user_objects[-1].id, "appointment_id": 4, "is_mechanic": True},
            {"content": "Brake system functioning properly.", "author_id": user_objects[-1].id, "appointment_id": 5, "is_mechanic": True},
        ]
        for comment_data in comments:
            comment = Comment(
                content=comment_data['content'],
                author_id=comment_data['author_id'],
                appointment_id=comment_data['appointment_id'],
                is_mechanic=comment_data['is_mechanic']
            )
            db.session.add(comment)

        db.session.commit()

        print("Test data added successfully")
