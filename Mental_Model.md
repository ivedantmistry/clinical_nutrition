## Users:

### 1. Patients
### 2. Doctors
### 3. Admin
### 4. Organization Head (OH)
### 5. Staff

## The Flow:

### 1. Anyone who creates a superuser account automatically becomes an Admin
### 2. Admin can create as many organizations and create and assign OH user and link to any org
### 3. Admin and OH can create user accounts and assign doctor and patient, staff roles, OH can't create Admin users but admin can create OH users
### 4. Patients are linked to Doctors/Clinicians in an org
### 5. staff can manage patients and doctors linking or etc, export data, read data
### 6. Admin can access all organizations in the system
### 7. OH can only manage OH they're assigned to
### 8. manages all the organizations throughout the system
### 9. OH, staff and doctor can adjust daily limits
### 10. staff and doctor can't change roles
### 11. doctor cannot create patient accounts
### 12. satff can only create patient accounts
### 13. Oh can create staff, doctor and patient accounts
### 14. only admin can create OH accounts for respective org
### 15. staff cannot change patient or dcotor roles, only can crate patient and link to dcotor
### 16. all stats like total patients, doctors, can be seen my staff and Oh and admin, doctor and patient can't


## Role Based Permissions
### 1. Patients
### 2. Doctors
### 3. Staff - All Permissions except assigning OH and admin roles
### 4. Admin - All permissions
### 5. OH - All permissions exlcuding creating organizations, and can't see other organizations, can't create Admin users, 


### Important Note: System will be master item info agnostic, respective admin will need to load the data with corrrect schema; we might provide detailed curated dataset to system work otherwise user won't be able to do that