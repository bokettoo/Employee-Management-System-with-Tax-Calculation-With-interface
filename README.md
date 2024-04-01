# Employee Management System

This Employee Management System is a Python application built using Tkinter for the GUI. It allows users to create and manage employee information including their basic details, type of employment, and additional information specific to their role. Employees can be of two types: Formateur and Agent, each with different attributes and salary calculation methods.

## Features

- Add new employees with their basic information such as name, date of birth, date of hire, and base salary.
- Choose between two types of employees: Formateur or Agent, each with specific attributes.
- Calculate and display employee's net salary based on their type and provided details.
- Save employee data to a JSON file for future reference.
- Load previously saved employee data from the JSON file.

## Installation

1. Clone or download the repository.
2. Install Python (if not already installed).
3. Navigate to the project directory in the terminal.
4. Run the following command to install required dependencies:

    ```
    pip install tk
    ```

5. Run the application by executing the `main.py` file:

    ```
    python main.py
    ```

## Usage

- Launch the application.
- Fill in the employee details including name, date of birth, date of hire, base salary, and select the employee type.
- Depending on the selected employee type, additional fields will appear for relevant information such as hours of overtime for Formateur or responsibility bonus for Agent.
- Click on "Create Employee" to add the employee to the system and see their details displayed.
- Optionally, click on "Save to JSON" to save the employee data to a JSON file.
- The employee data can be loaded from the JSON file by clicking on "Load Data from JSON".
