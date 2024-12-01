# Combined Project: SSIS Project & Campus Manager

## SSIS Project
### Prerequisites
- **Visual Studio** with SQL Server Integration Services (SSIS) extension
- **SQL Server**
- **.NET Framework 4.7.2** or later

### Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MohammedRagab00/DEPI_Final_Project.git
   cd DEPI_Final_Project

2. **Open the Project**:
   - Launch Visual Studio
   - Open the Solution File: `[Project Name].sln`
   - Ensure SSIS extension is installed in Visual Studio

3. **Configuration**:
   - Check connection strings in configuration files
   - Update database connection details as needed

### Running the Project
1. **Build the Solution**:
   - In Visual Studio, go to Build > Build Solution
   - Resolve any dependency issues

2. **Deploy SSIS Packages**:
   - Right-click on the SSIS project
   - Select "Deploy" 
   - Follow the deployment wizard to specify the target SQL Server

3. **Execute Packages**:
   - Open SQL Server Integration Services
   - Locate and run the deployed packages

### Troubleshooting
- Ensure all connection strings are correct
- Verify SQL Server permissions
- Check SSIS runtime is installed and configured

### Contributing
- Fork the repository
- Create a feature branch
- Commit your changes
- Push and create a pull request


## Campus Manager

### Overview
The Campus Manager is a comprehensive platform designed to manage various aspects of a university's academic operations. It allows users to enroll and drop sections, moderators to grade students, and administrators to manage places, departments, courses, sections, and user roles.

### Features
#### Users
- **Enroll in Sections**: Students can enroll in available sections.
- **Drop Sections**: Students can drop sections they are enrolled in.

#### Moderators
- **Grade Students**: Moderators can assign grades to students for their respective sections.

#### Administrators
- **Manage Places**: Add places within the university.
- **Manage Departments**: Add departments.
- **Manage Courses**: Add courses.
- **Manage Sections**: Add sections within courses.
- **Edit User Roles**: Assign or change user roles (e.g., student, moderator, admin).
- **Delete Users**: Remove users from the system.

### Usage
1. **User Registration**: Users can register for an account.
2. **Login**: Users can log in to access their dashboard.
3. **Enroll/Drop Sections**: Students can enroll in or drop sections from their dashboard.
4. **Grading**: Moderators can grade students from their respective section pages.
5. **Admin Panel**: Administrators can manage places, departments, courses, sections, and user roles from the admin panel.

### Contact
For any questions or suggestions, please contact [mohammed_ragab_@outlook.com](mailto:mohammed_ragab_@outlook.com).
