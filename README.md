# Installation Guide

Before running the project, you need to install all required dependencies from `requirements.txt`.  
There are **two ways** to do this:  

---

## **🔹 Option 1: Install Dependencies Globally**
If you want to install the dependencies **globally** on your system, follow these steps:

1. Open **PyCharm** and navigate to the **Terminal** (`View → Tool Windows → Terminal`).
2. Run the following command to install the required packages:
   ```sh
   pip install -r requirements.txt
   ```
3. This will install all dependencies in your **system-wide Python environment**.

👉 You’re done! Now you can run the project.

---

## **🔹 Option 2: Install Dependencies Using a Virtual Environment (Recommended)**
Using a **virtual environment** keeps dependencies isolated, preventing conflicts with other projects.

### **Step 1: Create a Virtual Environment**
- Open the **Terminal** in PyCharm and run:
  ```sh
  python -m venv venv
  ```
- This will create a virtual environment named `venv` inside your project folder.

### **Step 2: Activate the Virtual Environment**
- **On Windows (Command Prompt):**
  ```sh
  venv\Scripts\activate
  ```
- **On Windows (PowerShell):**
  ```sh
  .\venv\Scripts\Activate
  ```
- **On macOS/Linux:**
  ```sh
  source venv/bin/activate
  ```

### **Step 3: Install Dependencies in the Virtual Environment**
- After activation, install the dependencies by running:
  ```sh
  pip install -r requirements.txt
  ```

### **Step 4 (Optional): Deactivate the Virtual Environment**
- When you're done working, deactivate the virtual environment:
  ```sh
  deactivate
  ```

---
