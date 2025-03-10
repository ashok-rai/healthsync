# Patient-Doctor Appointment Booking System

## Background
The Patient-Doctor Appointment Booking System is designed to streamline the process of scheduling medical appointments. This application allows patients to book consultations with doctors based on their availability while enabling doctors to manage their schedules efficiently. Admin staff will oversee user management and system maintenance.

### Key Functionalities:
- **Booking Appointments**: Patients can book, reschedule, or cancel appointments.
- **Doctor Availability Management**: Doctors can set and update their available slots.
- **Patient Records**: Maintain a history of appointments and medical notes.
- **Payments**: Integration of online payments for consultations using Stripe.
- **Notifications**: SMS alerts for appointment confirmations and reminders via Twilio.
- **Patient PDF Report**: Generate and download reports for patient history and prescriptions.

## Requirements
### Must-Have
- User authentication and role-based access (Patients, Doctors, Admin)
- Appointment booking and management (Create, Reschedule, Cancel)
- Doctor availability management
- Patient medical records storage
- Notification system (SMS via Twilio for appointment reminders)
- Secure payment integration with Stripe
- Patient PDF report generation  

### Should-Have
- Doctor profile with specialization details
- Dashboard for doctors and admin to track appointments
- Search and filter functionality for doctors and available slots
- Basic analytics (e.g., total appointments, revenue tracking)

### Could-Have
- Telemedicine (Video consultation integration)
- AI-powered doctor recommendations based on symptoms
- Multi-language support for better accessibility

### Won't-Have (for now)
- AI-based health diagnostics
- Deep integration with hospital management systems
- Blockchain-based medical record storage

## Method

### System Architecture
The system follows a **three-tier architecture**:
- **Frontend**: HTML, Bootstrap 5, JavaScript
- **Backend**: Django (Django REST Framework for API support)
- **Database**: PostgreSQL
- **External Services**:  
  - **Stripe**: Payment processing  
  - **Twilio**: SMS notifications  
  - **Google/Facebook OAuth2**: Social login authentication  

### Components:
1. **Authentication Service**
   - Handles user authentication using Django’s built-in authentication system.
   - Supports email/password login and OAuth2-based Google/Facebook login.

2. **Appointment Service**
   - Patients can book, reschedule, or cancel appointments.
   - Doctors can manage their available time slots.
   - Admins can oversee and manage all appointments.

3. **Payments Service**
   - Integrates **Stripe** for secure payment processing.
   - Tracks payment status (Paid, Unpaid).

4. **Notification Service**
   - Sends appointment confirmations and reminders using Twilio (SMS).

### Database Schema

#### 1. Users Table (`auth_user`)
- `id` (Primary Key)
- `username` (Unique)
- `email`
- `password` (Hashed)
- `role` (`Patient`, `Doctor`, `Admin`)
- `social_auth_id` _(Nullable, for Google/Facebook login)_

#### 2. Doctors Table
- `id` (Primary Key)
- `user_id` (Foreign Key → `auth_user`)
- `specialization` (Text)
- `availability` (JSON storing available slots)

#### 3. Patients Table
- `id` (Primary Key)
- `user_id` (Foreign Key → `auth_user`)
- `medical_history` (Text)

#### 4. Appointments Table
- `id` (Primary Key)
- `patient_id` (Foreign Key → `Patients`)
- `doctor_id` (Foreign Key → `Doctors`)
- `appointment_date` (Datetime)
- `status` (`Pending`, `Confirmed`, `Completed`, `Cancelled`)
- `payment_status` (`Paid`, `Unpaid`)

#### 5. Payments Table
- `id` (Primary Key)
- `appointment_id` (Foreign Key → `Appointments`)
- `amount` (Decimal)
- `payment_status` (`Paid`, `Failed`, `Pending`)
- `transaction_id` (Stripe reference)

#### 6. Notifications Table
- `id` (Primary Key)
- `user_id` (Foreign Key → `auth_user`)
- `message` (Text)
- `status` (`Sent`, `Pending`)

