# Poppy Robot – Raspberry Pi + Dynamixel Capstone Project

## Overview
This project connects the **Poppy humanoid robot** to a **Raspberry Pi 5** with an **AI Hat** and Dynamixel motor controller. Students will extend Poppy’s abilities to take **external input** (voice, vision, sensors) and produce expressive **motor outputs** (poses, gestures, animations).  

Examples of possible interactions:
- Wave at Poppy → she waves back
- Ask Poppy a question → she turns her head and responds
- Command Poppy to dance → she shows off her moves

This project is both **hardware** (Dynamixel motors, Pi, sensors) and **software** (Python, AI/ML, motor control). The capstone challenge is to **expand her interactivity** while keeping the system robust and fault-tolerant.

---

## Repo Structure
- `poppy_motors.py` → Core motor control functions (connect, move, relax, poses, animations)
- `poppy_pi_interface.py` → Placeholder for Raspberry Pi I/O expansion (mic, camera, sensors)  
- `poppy_pi_testing.py` → Testing scripts for Pi integration  

---

## Hardware Setup
- **Robot**: Poppy torso with Dynamixel XL-series motors  
- **Controller**: USB2Dynamixel adapter  
- **Compute**: Raspberry Pi 5 + AI Hat  
- **New Inputs**: USB mic, Pi camera, touchscreen, external sensors (TODO)

Update the `PORT` in `poppy_motors.py` if your USB adapter shows up differently (`/dev/ttyUSB0` on Linux or `COMx` on Windows).

---

## Installation

1. Clone this repo onto your Raspberry Pi  
   ```
   git clone https://github.com/YOUR_ORG/poppy-project.git
   cd poppy-project
   ```

2. (Optional but recommended) Create and activate a virtual environment:  
   ```
   python3 -m venv venv
   source venv/bin/activate   # On Linux / Mac
   venv\Scripts\activate      # On Windows
   ```

3. Install dependencies from `requirements.txt`:  
   ```
   pip install -r requirements.txt
   ```

4. Connect the USB2Dynamixel adapter to the Raspberry Pi.  

5. Test the setup by running the motor test UI:  
   ```
   python3 poppy_motor_test_ui.py
   ```


---

## Usage
### Touchscreen UI
Launch a simple control panel:  
```
python3 poppy_pi_interface.py
```

### Motor Test UI
Test individual motors, see live positions, and set/release torque:  
```
python3 poppy_pi_testing.py
```

### Code Control
In Python:
```
import poppy_motors as pm
pm.wave_poppy(duration=2)
pm.drive(duration=2)
pm.relax_arms()
```

---

## Development Roadmap
Capstone students are expected to **expand the system** by adding hardware + software, as defined in their project scope. Examples include:
- **Microphone input**: speech commands → mapped to poses/animations  
- **Camera input**: detect faces, waving hands, etc. → trigger actions  
- **AI integration**: use Pi AI Hat to classify input or generate responses  
- **Remote control**: web or mobile interface to trigger Poppy’s behaviors  
- **Safety/fault tolerance**: watchdog timers, torque relaxation, stop button  

---

## Troubleshooting
- If motors don’t move: check `PORT`, motor connections, and power supply  
- Use `poppy_motor_test_ui.py` to confirm each motor is responding  
- If GUI won’t open: make sure `python3-tk` is installed  
- Always use `STOP` if Poppy behaves unexpectedly (sets a global stop flag)  

---

## Contribution Guidelines
- Document code changes in comments and README  
- Use Git branches for new features  
- When stuck, use debugging strategies: print statements, “source of truth” checkpoints, and Google/ChatGPT with clear problem descriptions  
- Communicate blockers early to the team  

## Resources & Acknowledgements

### Documentation & References
- [Poppy Project – Getting Started](https://docs.poppy-project.org/en/getting-started/)  
- [Pypot Motor Library (Herborist)](https://poppy-project.github.io/pypot/herborist.html)  
- [Robotis U2D2 USB Adapter Manual](https://emanual.robotis.com/docs/en/parts/interface/u2d2/)  
- [Addressing Dynamixel Motors (Poppy Torso Guide)](https://docs.poppy-project.org/en/assembly-guides/poppy-torso/addressing_dynamixel)  

### Collaboration
This project is a joint initiative between:  
- **Southeast College – Centre of Sustainable Innovation (CSI)** 
- **University of Regina – Electrical Systems Engineering Capstone Project**   
- **Southeast Techhub (SETH)**
- **Estevan Comprehensive High School – Robot Club**