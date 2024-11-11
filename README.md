Ransomware Simulation - Testing Environment and Instructions
_________________________________________________________________________________________________________________

This guide provides step-by-step instructions on how to set up and run the simulated ransomware on a Windows testing environment. Please read carefully to ensure the simulation executes correctly.

Author : Bemnet Merkebu


Prerequisites
_________________________________________________________________________________________________________________

Operating System: Windows (Windows Defender disabled).
Python: Ensure Python is installed and added to the system PATH.
Macros Enabled: Ensure Excel macros are enabled for this simulation.
Monitoring Script: monitor.py script running in the background to observe activity.



Setup Steps

Install Required Python Packages
_________________________________________________________________________________________________________________

- Open a terminal and navigate to the directory where requirements.txt is located.

- Install the required packages by running:

pip install -r requirements.txt

- If errors show up down in the line make sure to install the package needed.



Prepare the Testing Environment
_________________________________________________________________________________________________________________

- Disable Windows Defender or set exceptions for the files used in this simulation (to prevent interruptions from anti-malware).
- Unzip the provided archive and locate the dummy test directory. This directory contains sample files meant to simulate target files for encryption.
- Copy the dummy test directory to the following location:

C:\Users\Public\Downloads

- This directory will serve as the target for encryption.


Open the Excel Macro File
_________________________________________________________________________________________________________________

- Open the .xlsm file provided in the archive. This file mimics a phishing attachment in a real-world scenario.
Office_Assignment_Fall_2024.xlsm

- Ensure that macros are enabled when prompted. This will allow the VBA macro to run and execute the ransomware simulation.


Running the Simulation
_________________________________________________________________________________________________________________

- Once the .xlsm file is open and macros are enabled, the macro will begin encrypting the contents of the dummy test directory located in C:\Users\Public\Downloads.
- Make sure the monitor.py script is running during this process to capture and log activity. This script will provide warnings and insights on file activity within the target directory.


Encryption Process
_________________________________________________________________________________________________________________

- The macro will encrypt all files within the dummy test directory. During encryption, each file will be replaced with an encrypted version, and the original file will be deleted.
- A secret key for decryption is generated and saved in a hidden file named .secret_key in the C:\Users\Public\Downloads directory.

- In the case that the macro is not executing prioperly, you can just test the encryption by using the command below
python encrypt.py


Observing Activity with monitor.py
_________________________________________________________________________________________________________________

- The monitor.py script will log activities within the target directory, specifically noting when new encrypted files are created.
- This script simulates a monitoring tool that can detect unusual activity, providing an opportunity to intercept the ransomware process.


Decryption Process
_________________________________________________________________________________________________________________

- To decrypt the files, locate the decrypt.py script in the same directory.
- Run the script from the command line:

python decrypt.py

- You will be prompted to enter the decryption key. The key can be found in the .secret_key file, saved as a hexadecimal string.
- Copy the hexadecimal key and enter it when prompted to decrypt the files. Successful decryption will restore the original files in the dummy test directory.


Testing the Mitigation Script
_________________________________________________________________________________________________________________

- The mitigation.py script can be run to simulate suspending or killing the encryption process.
- Start mitigation.py during the encryption process if the target directory is large, as this will allow you more time to observe and interrupt the encryption.



Notes
_________________________________________________________________________________________________________________

- This simulation is scoped to a specific directory (C:\Users\Public\Downloads\test directory). In a real-world scenario, ransomware would potentially target entire drives or critical system directories.

*****************************************************************************************************************
Disclaimer: This simulation is intended for educational purposes only. Do not attempt to replicate or distribute real ransomware.
*****************************************************************************************************************