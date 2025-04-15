from datetime import datetime

class User:
    def __init__(self, user_id, name, dob, gender, contact_number, email):
        self.user_id = user_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.contact_number = contact_number
        self.email = email
        self.medical_history = []

    def add_medical_history(self, condition, diagnosis_date, notes=None):
        self.medical_history.append({
            'condition': condition,
            'diagnosis_date': diagnosis_date,
            'notes': notes
        })

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self.name}"

class Doctor:
    def __init__(self, doctor_id, name, specialization, contact_number, email):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.contact_number = contact_number
        self.email = email
        self.availability = {}  # {date: [time_slots]}

    def add_availability(self, date, time_slots):
        if date not in self.availability:
            self.availability[date] = []
        self.availability[date].extend(time_slots)
        self.availability[date] = sorted(list(set(self.availability[date])))

    def __str__(self):
        return f"Doctor ID: {self.doctor_id}, Name: {self.name}, Specialization: {self.specialization}"

class Appointment:
    def __init__(self, appointment_id, patient, doctor, appointment_time, issue):
        self.appointment_id = appointment_id
        self.patient = patient
        self.doctor = doctor
        self.appointment_time = appointment_time
        self.issue = issue
        self.notes = None
        self.prescription = None

    def add_notes(self, notes):
        self.notes = notes

    def add_prescription(self, prescription):
        self.prescription = prescription

    def __str__(self):
        return f"Appointment ID: {self.appointment_id}, Patient: {self.patient.name}, Doctor: {self.doctor.name}, Time: {self.appointment_time}"

class OnlineConsultationSystem:
    def __init__(self):
        self.users = {}  # {user_id: User object}
        self.doctors = {}  # {doctor_id: Doctor object}
        self.appointments = {}  # {appointment_id: Appointment object}
        self.next_user_id = 1
        self.next_doctor_id = 1
        self.next_appointment_id = 1

    def register_user(self, name, dob, gender, contact_number, email):
        user_id = self.next_user_id
        new_user = User(user_id, name, dob, gender, contact_number, email)
        self.users[user_id] = new_user
        self.next_user_id += 1
        print(f"User registered successfully with ID: {user_id}")
        return new_user

    def register_doctor(self, name, specialization, contact_number, email):
        doctor_id = self.next_doctor_id
        new_doctor = Doctor(doctor_id, name, specialization, contact_number, email)
        self.doctors[doctor_id] = new_doctor
        self.next_doctor_id += 1
        print(f"Doctor registered successfully with ID: {doctor_id}")
        return new_doctor

    def add_doctor_availability(self, doctor_id, date_str, time_slots):
        if doctor_id not in self.doctors:
            print("Doctor not found.")
            return
        try:
            # Basic validation for date format (YYYY-MM-DD)
            datetime.strptime(date_str, '%Y-%m-%d').date()
            self.doctors[doctor_id].add_availability(date_str, time_slots)
            print(f"Availability added for Doctor {doctor_id} on {date_str}: {time_slots}")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    def view_available_doctors(self, specialization=None, date=None):
        available_doctors = []
        for doctor in self.doctors.values():
            if specialization is None or doctor.specialization.lower() == specialization.lower():
                if date:
                    if date in doctor.availability and doctor.availability[date]:
                        available_doctors.append(doctor)
                else:
                    available_doctors.append(doctor)
        if available_doctors:
            print("Available Doctors:")
            for doctor in available_doctors:
                availability_info = f" (Available on {date}: {doctor.availability[date]})" if date and date in doctor.availability else ""
                print(f"- {doctor.name} ({doctor.specialization}){availability_info}")
        else:
            print("No doctors available based on your criteria.")
        return available_doctors

    def book_appointment(self, user_id, doctor_id, appointment_time_str, issue):
        if user_id not in self.users:
            print("User not found.")
            return None
        if doctor_id not in self.doctors:
            print("Doctor not found.")
            return None

        doctor = self.doctors[doctor_id]
        try:
            appointment_time = datetime.strptime(appointment_time_str, '%Y-%m-%d %H:%M')
            appointment_date_str = appointment_time.strftime('%Y-%m-%d')
            appointment_time_only = appointment_time.strftime('%H:%M')

            if appointment_date_str in doctor.availability and appointment_time_only in doctor.availability[appointment_date_str]:
                appointment_id = self.next_appointment_id
                new_appointment = Appointment(appointment_id, self.users[user_id], doctor, appointment_time, issue)
                self.appointments[appointment_id] = new_appointment
                doctor.availability[appointment_date_str].remove(appointment_time_only)
                self.next_appointment_id += 1
                print(f"Appointment booked successfully with ID: {appointment_id} for {self.users[user_id].name} with Dr. {doctor.name} at {appointment_time_str} for issue: {issue}")
                return new_appointment
            else:
                print("Selected time slot is not available for the doctor.")
                return None
        except ValueError:
            print("Invalid appointment time format. Please use YYYY-MM-DD HH:MM.")
            return None

    def view_user_appointments(self, user_id):
        if user_id not in self.users:
            print("User not found.")
            return []
        user_appointments = [appt for appt in self.appointments.values() if appt.patient.user_id == user_id]
        if user_appointments:
            print(f"Appointments for User {self.users[user_id].name}:")
            for appt in user_appointments:
                print(appt)
        else:
            print(f"No appointments found for User {self.users[user_id].name}.")
        return user_appointments

    def view_doctor_appointments(self, doctor_id):
        if doctor_id not in self.doctors:
            print("Doctor not found.")
            return []
        doctor_appointments = [appt for appt in self.appointments.values() if appt.doctor.doctor_id == doctor_id]
        if doctor_appointments:
            print(f"Appointments for Dr. {self.doctors[doctor_id].name}:")
            for appt in doctor_appointments:
                print(appt)
        else:
            print(f"No appointments found for Dr. {self.doctors[doctor_id].name}.")
        return doctor_appointments

    def add_consultation_notes(self, appointment_id, notes):
        if appointment_id not in self.appointments:
            print("Appointment not found.")
            return
        self.appointments[appointment_id].add_notes(notes)
        print(f"Notes added to Appointment {appointment_id}.")

    def add_prescription_to_appointment(self, appointment_id, prescription):
        if appointment_id not in self.appointments:
            print("Appointment not found.")
            return
        self.appointments[appointment_id].add_prescription(prescription)
        print(f"Prescription added to Appointment {appointment_id}.")

    def view_appointment_details(self, appointment_id):
        if appointment_id not in self.appointments:
            print("Appointment not found.")
            return None
        appointment = self.appointments[appointment_id]
        print("Appointment Details:")
        print(appointment)
        if appointment.notes:
            print(f"Notes: {appointment.notes}")
        if appointment.prescription:
            print(f"Prescription: {appointment.prescription}")
        return appointment

# Example Usage
if __name__ == "__main__":
    system = OnlineConsultationSystem()

    # Register users
    user1 = system.register_user("Alice Smith", "1990-05-15", "Female", "9876543210", "alice.smith@example.com")
    user2 = system.register_user("Bob Johnson", "1985-11-20", "Male", "8765432109", "bob.johnson@example.com")

    # Register doctors
    doctor1 = system.register_doctor("Dr. Emily White", "Cardiologist", "7418529630", "emily.white@example.com")
    doctor2 = system.register_doctor("Dr. John Green", "General Physician", "9638527410", "john.green@example.com")

    # Add doctor availability
    system.add_doctor_availability(doctor1.doctor_id, "2025-04-20", ["10:00", "11:00", "14:00"])
    system.add_doctor_availability(doctor1.doctor_id, "2025-04-21", ["09:30", "15:00"])
    system.add_doctor_availability(doctor2.doctor_id, "2025-04-20", ["11:30", "16:00"])

    # View available doctors
    system.view_available_doctors()
    system.view_available_doctors(specialization="Cardiologist")
    system.view_available_doctors(date="2025-04-20")
    system.view_available_doctors(specialization="General Physician", date="2025-04-20")

    # Book appointments
    appointment1 = system.book_appointment(user1.user_id, doctor1.doctor_id, "2025-04-20 10:00", "Chest pain")
    appointment2 = system.book_appointment(user2.user_id, doctor2.doctor_id, "2025-04-20 16:00", "Fever and cough")
    system.book_appointment(user1.user_id, doctor1.doctor_id, "2025-04-20 10:00", "Follow-up") # Trying to book the same slot

    # View user and doctor appointments
    system.view_user_appointments(user1.user_id)
    system.view_doctor_appointments(doctor1.doctor_id)

    # Add consultation notes and prescription
    if appointment1:
        system.add_consultation_notes(appointment1.appointment_id, "Patient reported mild chest pain and shortness of breath.")
        system.add_prescription_to_appointment(appointment1.appointment_id, "Prescribed Aspirin 75mg once daily.")

    # View appointment details
    if appointment1:
        system.view_appointment_details(appointment1.appointment_id)
