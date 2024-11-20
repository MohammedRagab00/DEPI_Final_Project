```markdown
# Combined Project: SSIS Project & Campus Manager

## SSIS Project

### Prerequisites
- **SQL Server Data Tools (SSDT)**: Ensure you have SSDT installed for developing SSIS packages.
- **SQL Server Integration Services (SSIS)**: Required to run and deploy SSIS packages.
- **.NET Framework**: Specify the required version.
- **Other Tools**: List any other necessary software or tools.

### Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MohammedRagab00/DEPI_Final_Project.git
   cd your-repo
   ```

2. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory with the necessary environment variables.
   - Example:
     ```plaintext
     DB_PASSWORD=yourpassword
     ```

3. **Restore Packages and Dependencies**:
   - If applicable, provide commands to restore any required packages.
   ```bash
   # Example command to restore packages
   ```

4. **Configure the Project**:
   - Update any configuration files with your local settings.

### Running the Project
1. **Open the Project**:
   - Open the solution file (`.sln`) in Visual Studio.

2. **Build the Project**:
   - Build the solution to ensure all dependencies are correctly set up.

3. **Deploy the SSIS Packages**:
   - Deploy the SSIS packages to your SSIS server.

4. **Run the Packages**:
   - Execute the SSIS packages as needed.

### Sample Data
- **Provide Sample Data Files**:
  - Include sample data files or instructions on how to generate the necessary data.
  - Example:
    ```plaintext
    /sample-data/sample-data-file.csv
    ```

### Troubleshooting
- **Common Issues and Solutions**:
  - List common issues users might encounter and their solutions.
  - Example:
    ```markdown
    ### Issue: Missing Environment Variables
    **Solution**: Ensure you have created a `.env` file with the required variables.
    ```

### Contributing
- **Guidelines for Contributing**:
  - Provide guidelines for contributing to the project.
  - Example:
    ```markdown
    ### How to Contribute
    1. Fork the repository.
    2. Create a new branch (`git checkout -b feature-branch`).
    3. Make your changes.
    4. Commit your changes (`git commit -m 'Add new feature'`).
    5. Push to the branch (`git push origin feature-branch`).
    6. Open a pull request.
    ```

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
