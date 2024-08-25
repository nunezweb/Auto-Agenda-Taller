"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, Blueprint
from api.models import db, User, Role, Car, Appointment, Service, Comment, Setting, TokenBlockList
from api.utils import generate_sitemap, APIException
from flask import Flask
from flask_cors import CORS
from datetime import datetime, timedelta, timezone
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from api.commands import insert_test_data


app = Flask(__name__)
bcrypt = Bcrypt(app)

api = Blueprint('api', __name__)
CORS(api)


# ///////////////////////////////////////////////////////////////////////////////////////////// post en /create users from admin
@api.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phone_number = data.get('phone_number')
    role_id = data.get('role_id')

    if not email or not password or not name or not phone_number or not role_id:
        return jsonify({"error": "All fields are required"}), 400
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password, name=name, phone_number=phone_number, role_id=role_id)
    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "user": new_user.serialize(),
    }
    return jsonify(response_body), 201

# ///////////////////////////////////////////////////////////////////////////////////////////// post en /signup
@api.route('/signupuser', methods=['POST'])
def create_signupusers():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phone_number = data.get('phone_number')

    if not email or not password or not name or not phone_number:
        return jsonify({"error": "All fields are required"}), 400
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password, name=name, phone_number=phone_number, role_id=3)
    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name,
        "phone_number": new_user.phone_number,
    }
    return jsonify(response_body), 201


# ///////////////////////////////////////////////////////////////////////////////////////////// post en /login
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    role = Role.query.filter_by(id=user.role_id).first()
    access_token = create_access_token(identity=user.id, additional_claims={"role_id": role.id})
    return jsonify(access_token=access_token, role_id=role.id, user_id=user.id), 200
# @api.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     if not data or not data.get('email') or not data.get('password'):
#         return jsonify({"error": "Email and password are required"}), 400

#     email = data.get('email')
#     password = data.get('password')

#     user = User.query.filter_by(email=email).first()
#     if not user or not bcrypt.check_password_hash(user.password, password):
#         # Incrementar el contador de intentos fallidos
#         # user.failed_login_attempts += 1
#         # if user.failed_login_attempts >= 5:
#         #     # Bloquear la cuenta temporalmente
#         #     user.is_blocked = True
#         #     db.session.commit()
#         #     return jsonify({"error": "Account blocked due to excessive login attempts"}), 401
#         # return jsonify({"error": "Invalid credentials"}), 401

#     role = Role.query.filter_by(id=user.role_id).first()
#     if not role:
#         return jsonify({"error": "Invalid role"}), 401

#     access_token = create_access_token(identity=user.id, additional_claims={"role_id": role.id})
#     # access_token = create_access_token(identity=user.id, additional_claims={"role_id": role.id}, expires_in=3600)
#     return jsonify(access_token=access_token, role_id=role.id, user_id=user.id), 200

# ///////////////////////////////////////////////////////////////////////////////////////////// post en /ping user
@api.route('/pinguser', methods=['GET'])
@jwt_required()
def ping_user():
    print("Iniciando ping_user")
    current_user_id = get_jwt_identity()
    payload = get_jwt()
    
    print("current_user_id:", current_user_id)
    print("JWT Payload:", payload)
    
    if "role_id" not in payload:
        print("Role ID no encontrado en el token")
        return jsonify({"error": "Role ID not found in token"}), 400
    
    role_id = payload["role_id"]
    print("Role ID:", role_id)

    response = jsonify({"message": "User is authenticated", "user_id": current_user_id, "role_id": role_id})
    print("Respuesta enviada:", response)
    
    return response, 200


# ///////////////////////////////////////////////////////////////////////////////////////////// post en /logout
@api.route('/logout', methods=['POST'])
@jwt_required()
def user_logout():
    jti = get_jwt()["jti"]
    token_blocked = TokenBlockList(jti=jti)
    db.session.add(token_blocked)
    db.session.commit()
    return jsonify({"msg": "Logout successful"})

# ///////////////////////////////////////////////////////////////////////////////////////////// get a /users con id
@api.route('/users/<int:user_id>', methods=['GET'])
# @jwt_required()
def get_user(user_id):
    user_query = User.query.filter_by(id=user_id).first()
    if user_query:
        response_body = {
            "msg": "Resultado exitoso", 
            "result": user_query.serialize()
        }
        return jsonify(response_body), 200
    else:
        response_body = {
           "msg": "No existe" 
        }
        return jsonify(response_body), 404
    
# ///////////////////////////////////////////////////////////////////////////////////////////// DELETE a /users con id
@api.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user: 
        return jsonify({"error": "User not found"}), 404

    appointments = Appointment.query.filter_by(user_id=user_id).all()
    if not appointments:
        return jsonify({"error": "No appointments found for this user"}), 404

    for appointment in appointments:
        comments = Comment.query.filter_by(appointment_id=appointment.id).all()
        for comment in comments:
            db.session.delete(comment)
        db.session.delete(appointment)

    cars = Car.query.filter_by(owner_id=user_id).all()
    if not cars:
        return jsonify({"error": "No cars found for this user"}), 404

    for car in cars:
        db.session.delete(car)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User and related data deleted successfully"}), 200

   
# ///////////////////////////////////////////////////////////////////////////////////////////// get a /services con id
@api.route('/services/<int:services_id>', methods=['GET'])
@jwt_required()
def get_service(services_id):
    service_query = Service.query.filter_by(id=services_id).first()
    if service_query:
        response_body = {
            "msg": "Resultado exitoso", 
            "result": service_query.serialize()
        }
        return jsonify(response_body), 200
    else:
        response_body = {
           "msg": "Service no exist" 
        }
        return jsonify(response_body), 404

# ///////////////////////////////////////////////////////////////////////////////////////////// GET a /cars 
@api.route('/cars', methods=['GET'])
@jwt_required()
def get_all_cars():
    cars = Car.query.all()
    car_list = [car.serialize() for car in cars]
    return jsonify(car_list), 200

    
# ///////////////////////////////////////////////////////////////////////////////////////////// get a /cars con id
@api.route('/cars/<int:car_id>', methods=['GET'])
@jwt_required()
def get_cars(car_id):
    car_query = Car.query.filter_by(id=car_id).first()
    if car_query:
        response_body = {
            "msg": "Resultado exitoso", 
            "result": car_query.serialize()
        }
        return jsonify(response_body), 200
    else:
        response_body = {
           "msg": "Car no exist" 
        }
        return jsonify(response_body), 404
    

# ///////////////////////////////////////////////////////////////////////////////////////////// get a /cars/user con id del user
@api.route('/cars/user/<int:owner_id>', methods=['GET'])
@jwt_required()
def get_user_cars(owner_id):
    cars_query = Car.query.filter_by(owner_id=owner_id).all()
    if cars_query:
        response_body = {
            "msg": "Resultado exitoso", 
            "result": [car.serialize() for car in cars_query]
        }
        return jsonify(response_body), 200
    else:
        response_body = {
           "msg": "No cars found for this user" 
        }
        return jsonify(response_body), 404

# ///////////////////////////////////////////////////////////////////////////////////////////// post a /cars 
@api.route('/cars', methods=['POST'])
@jwt_required()
def create_car():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    car_model = data.get('car_model')
    license_plate = data.get('license_plate')
    user_id = data.get('user_id')
    if not car_model or not license_plate or not user_id:
        return jsonify({"error": "Car model, license plate, and user ID are required"}), 400
    existing_user = User.query.filter_by(id=user_id).first()
    if not existing_user:
        return jsonify({"error": "Bad user_id"}), 400

    new_car = Car(car_model=car_model, license_plate=license_plate, owner_id=user_id)
    db.session.add(new_car)
    db.session.commit()

    response_body = new_car.serialize()
    return jsonify(response_body), 201

# ///////////////////////////////////////////////////////////////////////////////////////////// PATCH a /cars + id 
@api.route('/cars/<int:car_id>', methods=['PATCH'])
@jwt_required()
def update_car(car_id):
    car = Car.query.get(car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404

    data = request.get_json()
    car_model = data.get('car_model')
    license_plate = data.get('license_plate')

    if car_model:
        car.car_model = car_model
    if license_plate:
        car.license_plate = license_plate

    db.session.commit()
    return jsonify(car.serialize()), 200

# ///////////////////////////////////////////////////////////////////////////////////////////// DELETE a /cars + id 
@api.route('/cars/<int:car_id>', methods=['DELETE'])
@jwt_required()
def delete_car(car_id):
    car = Car.query.get(car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404

    associated_appointments = Appointment.query.filter_by(car_id=car_id).all()
    if associated_appointments:
        return jsonify({"error": "Cannot delete car because it is associated with an appointment"}), 400

    db.session.delete(car)
    db.session.commit()
    return jsonify({"message": "Car deleted successfully"}), 200


# ///////////////////////////////////////////////////////////////////////////////////////////// GET a /comments?appointment_id=
@api.route('/comments', methods=['GET'])
@jwt_required()
def get_comments():
    appointment_id = request.args.get('appointment_id')
    if appointment_id:
        comments_query = Comment.query.filter_by(appointment_id=appointment_id).all()
        comments_list = list(map(lambda comment: comment.serialize(), comments_query))
        return jsonify(comments_list), 200
    else:
        return jsonify({"msg": "No appointment_id provided"}), 400


# ///////////////////////////////////////////////////////////////////////////////////////////// post a /comments 
@api.route('/comments', methods=['POST'])
@jwt_required()
def create_comment():
    data = request.get_json()
    comment_content = data.get('comment')
    user_id = data.get('user_id')
    appointment_id = data.get('appointment_id')
    is_mechanic = data.get('is_mechanic', False) 

    if not comment_content or not user_id or not appointment_id:
        return jsonify({"error": "Comment, user ID, and appointment ID are required"}), 400

    new_comment = Comment(
        content=comment_content,
        author_id=user_id,
        appointment_id=appointment_id,
        is_mechanic=is_mechanic
    )
    db.session.add(new_comment)
    db.session.commit()

    response_body = new_comment.serialize()
    return jsonify(response_body), 201



# ///////////////////////////////////////////////////////////////////////////////////////////// post a /services 
@api.route('/services', methods=['POST'])
@jwt_required()
def create_service():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    name = data.get('name')
    description = data.get('description')
    duration = data.get('duration')
    slots_required = data.get('slots_required')
    if not name or not description or not duration or not slots_required:
        return jsonify({"error": "Name, description,slots_required and duration are required"}), 400

    new_service = Service(name=name, description=description, duration=duration, slots_required=slots_required)
    db.session.add(new_service)
    db.session.commit()

    response_body = new_service.serialize()
    return jsonify(response_body), 201

# ///////////////////////////////////////////////////////////////////////////////////////////// get a /services 
@api.route('/services', methods=['GET'])
def get_services():
    services_query = Service.query.all()
    services_list = list(map(lambda service: service.serialize(), services_query))
    return jsonify(services_list), 200


# ///////////////////////////////////////////////////////////////////////////////////////////// post a /settings 
@api.route('/settings', methods=['POST'])
@jwt_required()
def create_setting():
    data = request.get_json()
    max_appointments_per_hour = data.get('max_appointments_per_hour')
    if max_appointments_per_hour is None:
        return jsonify({"error": "Max appointments per hour is required"}), 400

    setting = Setting.query.first()
    if setting:
        setting.max_appointments_per_hour = max_appointments_per_hour
    else:
        setting = Setting(max_appointments_per_hour=max_appointments_per_hour)
        db.session.add(setting)
    db.session.commit()

    response_body = setting.serialize()
    return jsonify(response_body), 201


# ///////////////////////////////////////////////////////////////////////////////////////////// get a /settings 
@api.route('/settings', methods=['GET'])
@jwt_required()
def get_setting():
    setting = Setting.query.first()
    if setting:
        response_body = setting.serialize()
        return jsonify(response_body), 200
    else:
        return jsonify({"msg": "Settings not configured"}), 404
    
# ///////////////////////////////////////////////////////////////////////////////////////////// get a /users 
@api.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users_query = User.query.all()
    users_list = list(map(lambda user: user.serialize(), users_query))
    return jsonify(users_list), 200

# ///////////////////////////////////////////////////////////////////////////////////////////// post a /appointments 
@api.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    date = data.get('date')
    user_id = data.get('user_id')
    car_id = data.get('car_id')
    service_id = data.get('service_id')
    comment = data.get('comment')
    
    if not date or not user_id or not car_id or not service_id:
        return jsonify({"error": "Date, user ID, car ID, and service ID are required"}), 400
    
    existing_user = User.query.filter_by(id=user_id).first()
    if not existing_user:
        return jsonify({"error": "Bad user_id"}), 400

    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    max_appointments_per_hour = Setting.query.first().max_appointments_per_hour   

    # Verificar citas existentes en la misma hora
    start_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    start_time = start_time.replace(tzinfo=timezone.utc)
    end_time = start_time + timedelta(hours=1)
    appointments_in_hour = Appointment.query.filter(  
        Appointment.date >= start_time,  
        Appointment.date < end_time  
    ).all()

    total_slots_booked = sum([app.service.slots_required for app in appointments_in_hour])  

    if (total_slots_booked + service.slots_required) <= max_appointments_per_hour:  
        new_appointment = Appointment(
            date=start_time,
            user_id=user_id,
            car_id=car_id,
            service_id=service_id,
            status="pending"
        )
        db.session.add(new_appointment)
        db.session.commit()

        if comment:
            new_comment = Comment(
                content=comment,
                author_id=user_id,
                appointment_id=new_appointment.id,
                is_mechanic=False
            )
            db.session.add(new_comment)
            db.session.commit()

        response_body = new_appointment.serialize()
        return jsonify(response_body), 201
    else:
        return jsonify({"error": "No available slots for this time"}), 400

# ///////////////////////////////////////////////////////////////////////////////////////////// PATCH a /appointments con id
@api.route('/appointments/<int:appointment_id>', methods=['PATCH'])
@jwt_required()
def update_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    data = request.get_json()
    status = data.get('status')
    if status:
        appointment.status = status

    db.session.commit()
    return jsonify({"msg": "Appointment updated successfully"}), 200

# ///////////////////////////////////////////////////////////////////////////////////////////// get a /appointments con id
@api.route('/appointments/<int:appointment_id>', methods=['GET'])
@jwt_required()
def get_appointment(appointment_id):
    appointment_query = Appointment.query.filter_by(id=appointment_id).first()
    if appointment_query:
        response_body = {
            "msg": "Resultado exitoso",
            "result": appointment_query.serialize()
        }
        return jsonify(response_body), 200
    else:
        response_body = {
           "msg": "No existe"
        }
        return jsonify(response_body), 404

# ///////////////////////////////////////////////////////////////////////////////////////////// delete a /appointments con id
@api.route('/appointments/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Cita no encontrada"}), 404
    
    comments = Comment.query.filter_by(appointment_id=appointment_id).all()
    for comment in comments:
        db.session.delete(comment)
    db.session.delete(appointment)
    db.session.commit()

    return jsonify({"msg": "Cita cancelada exitosamente"}), 200

# ///////////////////////////////////////////////////////////////////////////////////////////// get a /appointments
@api.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    appointments_query = Appointment.query.all()
    
    appointments_list = []
    for appointment in appointments_query:
        appointment_data = appointment.serialize()
        
        user = User.query.get(appointment.user_id)
        car = Car.query.get(appointment.car_id)
        service = Service.query.get(appointment.service_id)
        
        # Obtener comentarios asociados a la cita
        comments = Comment.query.filter_by(appointment_id=appointment.id).all()
        comments_data = [comment.serialize() for comment in comments]

        # Agregar los datos adicionales a appointment_data
        appointment_data['user'] = user.serialize() if user else None
        appointment_data['car'] = car.serialize() if car else None
        appointment_data['service'] = service.serialize() if service else None
        appointment_data['comments'] = comments_data 

        appointments_list.append(appointment_data)
    
    return jsonify(appointments_list), 200


# ///////////////////////////////////////////////////////////////////////////////////////////// get a /appointmentsuser
@api.route('/appointmentsuser/<int:user_id>', methods=['GET'])
@jwt_required()
def get_appointmentsuser(user_id):
    appointments_query  = Appointment.query.filter_by(user_id=user_id).all()

    if not appointments_query:
        return jsonify({"error": "No appointments found for this user"}), 404
    
    appointments_list = []
    for appointment in appointments_query:
        appointment_data = appointment.serialize()
        
        user = User.query.get(appointment.user_id)
        car = Car.query.get(appointment.car_id)
        service = Service.query.get(appointment.service_id)
        
        comments = Comment.query.filter_by(appointment_id=appointment.id).all()
        comments_data = [comment.serialize() for comment in comments]

        appointment_data['user'] = user.serialize() if user else None
        appointment_data['car'] = car.serialize() if car else None
        appointment_data['service'] = service.serialize() if service else None
        appointment_data['comments'] = comments_data 

        appointments_list.append(appointment_data)
    
    return jsonify(appointments_list), 200

# ///////////////////////////////////////////////////////////////////////////////////////////// GET a /cars/count
@api.route('/totalcount', methods=['GET'])
@jwt_required()
def total_count():
    total_appointments = Appointment.query.count()
    total_clients = User.query.filter_by(role_id=3).count()
    total_services = Service.query.count()
    total_cars = Car.query.count()
    return jsonify({'total_clients': total_clients, 'total_appointments': total_appointments, 'total_cars': total_cars, 'total_services': total_services}), 200

# ///////////////////////////////////////////////////////////////////////////////////////////// GET /slots-taken
@api.route('/slots-taken', methods=['GET'])
def get_slots_taken():
    now = datetime.now()
    end_date = now + timedelta(days=30) 

    appointments = Appointment.query.filter(
        Appointment.date >= now,
        Appointment.date <= end_date
    ).all()

    slots = [
        {
            'date': app.date.strftime('%Y-%m-%d'),
            'start_time': app.date.strftime('%H:%M:%S'),
            'end_time': (app.date + timedelta(hours=1)).strftime('%H:%M:%S'),
        } for app in appointments
    ]

    return jsonify(slots), 200


# ///////////////////////////////////////////////////////////////////////////////////////////// PATCH a /update_profile
@api.route('/update_profile', methods=['PATCH'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phoneNumber')
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')

    user = User.query.get(user_id)
    
    if not user or not bcrypt.check_password_hash(user.password, current_password):
        return jsonify({"error": "Invalid current password"}), 401

    if name:
        user.name = name
    if email:
        user.email = email
    if phone_number:
        user.phone_number = phone_number
    if new_password:
        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')

    db.session.commit()
    return jsonify({"msg": "Profile updated successfully", "email": user.email}), 200

@api.route('/run-insert-test-data', methods=['POST'])
def run_insert_test_data():
    try:
        # Llama a la función que ejecuta el comando
        insert_test_data()
        return jsonify({"message": "Test data inserted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
