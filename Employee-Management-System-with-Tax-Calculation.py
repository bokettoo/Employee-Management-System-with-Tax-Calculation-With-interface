import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path


class IR:
    tranches = [30000, 50000, 60000, 80000, 180000]
    tauxIR = [0, 10, 20, 30, 34, 38]

    @staticmethod
    def getIR(salaire):
        for i in range(len(IR.tranches)):
            if salaire <= IR.tranches[i]:
                return IR.tauxIR[i]
        return IR.tauxIR[-1]

class IEmploye(ABC):
    @abstractmethod
    def age(self):
        pass

    @abstractmethod
    def anciennete(self):
        pass

    @abstractmethod
    def dateRetraite(self, ageRetraite):
        pass

class Employe(IEmploye):
    matricule_count = 0  
    def __init__(self, nom, dateNaissance, dateEmbauche, salaireBase):
        Employe.matricule_count += 1
        self.matricule = Employe.matricule_count
        self.nom = nom
        self.dateNaissance = datetime.strptime(dateNaissance, "%Y-%m-%d").date()
        self.dateEmbauche = datetime.strptime(dateEmbauche, "%Y-%m-%d").date()
        self.salaireBase = salaireBase

        
        age_embauche = self.age()
        if age_embauche < 20:
            raise ValueError("L'âge de l'employé à la date d'embauche ne peut pas être inférieur à 20 ans.")

    @abstractmethod
    def age(self):
        today = datetime.now().date()
        return today.year - self.dateNaissance.year - ((today.month, today.day) < (self.dateNaissance.month, self.dateNaissance.day))

    @abstractmethod
    def anciennete(self):
        today = datetime.now().date()
        return today.year - self.dateEmbauche.year - ((today.month, today.day) < (self.dateEmbauche.month, self.dateEmbauche.day))

    @abstractmethod
    def dateRetraite(self, ageRetraite):
        return self.dateNaissance.year + ageRetraite

    @abstractmethod
    def salaireAPayer(self):
        pass

    def __str__(self):
        return f"{self.matricule}-{self.nom}-{self.dateNaissance}-{self.dateEmbauche}-{self.salaireBase}"

    def __eq__(self, other):
        return self.matricule == other.matricule

class Formateur(Employe):
    def __init__(self, nom, dateNaissance, dateEmbauche, salaireBase, heureSup, tarifHSup=70.00):
        super().__init__(nom, dateNaissance, dateEmbauche, salaireBase)
        self.heureSup = heureSup
        self.tarifHSup = tarifHSup

    def salaireAPayer(self):
        tauxIR = IR.getIR(self.salaireBase)
        salaire_net = (self.salaireBase + self.heureSup * self.tarifHSup) * (1 - tauxIR / 100)
        return salaire_net

    def __str__(self):
        return f"{super().__str__()}-{self.heureSup}-{self.tarifHSup}"
    
    def age(self):
        today = datetime.now().date()
        return today.year - self.dateNaissance.year - ((today.month, today.day) < (self.dateNaissance.month, self.dateNaissance.day))
    
    def anciennete(self):
        today = datetime.now().date()
        return today.year - self.dateEmbauche.year - ((today.month, today.day) < (self.dateEmbauche.month, self.dateEmbauche.day))
    
    def dateRetraite(self, ageRetraite):
        return self.dateNaissance.year + ageRetraite
    


class Agent(Employe):
    def __init__(self, nom, dateNaissance, dateEmbauche, salaireBase, primeResponsabilite):
        super().__init__(nom, dateNaissance, dateEmbauche, salaireBase)
        self.primeResponsabilite = primeResponsabilite

    def salaireAPayer(self):
        tauxIR = IR.getIR(self.salaireBase)
        salaire_net = (self.salaireBase + self.primeResponsabilite) * (1 - tauxIR / 100)
        return salaire_net
    
    def age(self):
        today = datetime.now().date()
        return today.year - self.dateNaissance.year - ((today.month, today.day) < (self.dateNaissance.month, self.dateNaissance.day))
    
    def anciennete(self):
        today = datetime.now().date()
        return today.year - self.dateEmbauche.year - ((today.month, today.day) < (self.dateEmbauche.month, self.dateEmbauche.day))
    
    def dateRetraite(self, ageRetraite):
        return self.dateNaissance.year + ageRetraite
    


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Employee Management System")
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Employee Information")
        self.label.pack(pady=10)

        self.label_name = ttk.Label(self, text="Name:")
        self.entry_name = ttk.Entry(self)
        self.label_name.pack()
        self.entry_name.pack()

        self.label_date_of_birth = ttk.Label(self, text="Date of Birth (YYYY-MM-DD):")
        self.entry_date_of_birth = ttk.Entry(self)
        self.label_date_of_birth.pack()
        self.entry_date_of_birth.pack()

        self.label_date_of_hire = ttk.Label(self, text="Date of Hire (YYYY-MM-DD):")
        self.entry_date_of_hire = ttk.Entry(self)
        self.label_date_of_hire.pack()
        self.entry_date_of_hire.pack()

        self.label_salary = ttk.Label(self, text="Base Salary:")
        self.entry_salary = ttk.Entry(self)
        self.label_salary.pack()
        self.entry_salary.pack()

        self.label_type = ttk.Label(self, text="Employee Type:")
        self.combo_type = ttk.Combobox(self, values=["Formateur", "Agent"])
        self.label_type.pack()
        self.combo_type.pack()

        # Additional widgets for Formateur
        self.label_hour_sup = ttk.Label(self, text="Hours of Overtime:")
        self.entry_hour_sup = ttk.Entry(self)
        self.entry_hour_sup.insert(0, "for formateur")
        self.label_hour_sup.pack()
        self.entry_hour_sup.pack()

        self.label_tarif_hsup = ttk.Label(self, text="Overtime Rate:")
        self.entry_tarif_hsup = ttk.Entry(self)
        self.entry_tarif_hsup.insert(0, "for formateur")
        self.label_tarif_hsup.pack()
        self.entry_tarif_hsup.pack()

        # Additional widgets for Agent
        self.label_prime_responsabilite = ttk.Label(self, text="Responsibility Bonus:")
        self.entry_prime_responsabilite = ttk.Entry(self)
        self.entry_prime_responsabilite.insert(0,"for Agent")
        self.label_prime_responsabilite.pack()
        self.entry_prime_responsabilite.pack()

        self.button_create = ttk.Button(self, text="Create Employee", command=self.create_employee)
        self.button_create.pack(pady=10)

        self.text_display = tk.Text(self, height=10, width=50)
        self.text_display.pack()

        self.button_save = ttk.Button(self, text="Save to JSON", command=self.save_to_json)
        self.button_save.pack(pady=10)
      
        self.tree = ttk.Treeview(self, columns=("Name", "Date of Birth", "Date of Hire", "Base Salary", "Employee Type", "Additional Info"), show="headings")

        
        self.tree.heading("Name", text="Name")
        self.tree.heading("Date of Birth", text="Date of Birth")
        self.tree.heading("Date of Hire", text="Date of Hire")
        self.tree.heading("Base Salary", text="Base Salary")
        self.tree.heading("Employee Type", text="Employee Type")
        self.tree.heading("Additional Info", text="Additional Info")

        for col in self.tree["columns"]:
            self.tree.column(col, width=100)

        self.tree.pack(pady=20)
        

        self.load_data_from_json("employee_data.json")
    
    
    def create_employee(self):
        name = self.entry_name.get()
        date_of_birth = self.entry_date_of_birth.get()
        date_of_hire = self.entry_date_of_hire.get()
        salary = float(self.entry_salary.get())
        employee_type = self.combo_type.get()

        if employee_type == "Formateur":
            hour_sup = float(self.entry_hour_sup.get())
            tarif_hsup = float(self.entry_tarif_hsup.get())
            employee = Formateur(name, date_of_birth, date_of_hire, salary, hour_sup, tarif_hsup)
            self.text_display.insert(tk.END, str(employee) + "\n")

        elif employee_type == "Agent":
            prime_responsabilite = float(self.entry_prime_responsabilite.get())
            employee = Agent(name, date_of_birth, date_of_hire, salary, prime_responsabilite)

            self.text_display.insert(tk.END, str(employee) + "\n")

    def save_to_json(self):
        name = self.entry_name.get()
        date_of_birth = self.entry_date_of_birth.get()
        date_of_hire = self.entry_date_of_hire.get()
        salary = float(self.entry_salary.get())
        employee_type = self.combo_type.get()

        if employee_type == "Formateur":
            hour_sup = float(self.entry_hour_sup.get())
            tarif_hsup = float(self.entry_tarif_hsup.get())
            employee = Formateur(name, date_of_birth, date_of_hire, salary, hour_sup, tarif_hsup)
            data = {
            "Name": employee.nom,
            "Date of Birth": str(employee.dateNaissance),
            "Date of Hire": str(employee.dateEmbauche),
            "Base Salary": employee.salaireBase,
            "Employee Type": employee.__class__.__name__,
            "Additional Info": employee.__str__(),
        }
            self.sub_save_to_json(data)
            


        elif employee_type == "Agent":
            prime_responsabilite = float(self.entry_prime_responsabilite.get())
            employee = Agent(name, date_of_birth, date_of_hire, salary, prime_responsabilite)

            data = {
            "Name": employee.nom,
            "Date of Birth": str(employee.dateNaissance),
            "Date of Hire": str(employee.dateEmbauche),
            "Base Salary": employee.salaireBase,
            "Employee Type": employee.__class__.__name__,
            "Additional Info": employee.__str__(),
        }
            self.sub_save_to_json(data)
            
           
    
    def sub_save_to_json(self,data):
        file_path = "employee_data.json"
            
        file_exists = Path(file_path).is_file()
        with open(file_path, 'r') as file:
            existing_data = [json.load(file)]

        existing_data.append(data)


        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=2)
        self.load_data_from_json(file_path)

       

    
    def load_data_from_json(self, json_file):
        try:
            with open(json_file, "r") as file:
                data = json.load(file)

            
            self.tree.delete(*self.tree.get_children())

           
            for entry in data:
                values = (
                    entry["Name"],
                    entry["Date of Birth"],
                    entry["Date of Hire"],
                    entry["Base Salary"],
                    entry["Employee Type"],
                    entry["Additional Info"]
                )
                self.tree.insert("", "end", values=values)

        except FileNotFoundError:
            print(f"File '{json_file}' not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file '{json_file}'.")


        

if __name__ == "__main__":
    app = Application()
    app.mainloop()
