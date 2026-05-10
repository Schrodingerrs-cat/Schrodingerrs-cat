# 👋 Hey, I'm Aryan

🤖 **M.S. Robotics Engineering @ Worcester Polytechnic Institute** — building the perception stack for an autonomous vehicle I call **Schrödinger's Vision**. Until you observe it, the lane is both there and not there.

I care about how robots **see, think, and move** — perception, autonomy, controls, and embedded systems. I've shipped autonomy on UAVs, satellites, manipulators, and humanoids. Currently going deeper into **physical AI** and learned-vs-classical fusion.

📍 Worcester, MA · 🎓 BTech Electronics & Communication, Nirma University · ✈️ Previously satellites + flight controllers in India

---

## 🔭 Currently Working On

- 🧠 **Schrödinger's Vision** — multi-camera autonomous driving perception (detection, tracking, depth, motion, BEV)
- 🦾 **RoboCare Lab @ WPI** — vision-based assistive perception on Pepper humanoid for dementia care
- 📚 Going deeper into physical AI, VLA models, and learned-classical fusion in robotics

---

## 🚗 Featured Projects

### 🛣️ [MultiCam Autonomous Driving Perception](https://github.com/Schrodingerrs-cat/MultiCam-AutonomousDriving-Perception)
Production-grade multi-camera perception system reproducing Tesla FSD-style visualization. Synchronized 4-camera dashcam input across 13 real-world driving sequences (night, tunnels, sunset glare, dense traffic). 15+ deep learning models integrated end-to-end: lane classification, multi-class detection, traffic light + sign recognition, pedestrian pose, brake/turn-indicator state, RAFT optical flow, monocular depth, and Blender 3D visualization with collision prediction.
> `Python` `PyTorch` `OpenCV` `Blender` `YOLO` `RAFT` `BoT-SORT`

### 🛰️ CanSat — Miniature Satellite Flight Control & Telemetry
Co-led a 4-person team building a can-sized satellite with reaction-wheel PID attitude control, 900 MHz XBee RF telemetry, and embedded sensor fusion (IMU, pressure, temp). **🥈 2nd place nationally at SMOPS 2023** — India's first InSpace CanSat competition.
> `C/C++` `PID Control` `XBee RF` `Embedded Systems`

### 🚁 Quadrotor Trajectory Tracking
Cascaded PD control stack with SO(3) attitude inner-loop and gravity-compensated outer-loop on Crazyflie 2.x. C²-continuous polynomial trajectory generators with quintic transitions, RL-tuned gains across 18+ sweeps. Achieves well-damped convergence in 3–4.5s with near-zero steady-state error.
> `Python` `PyBullet` `Control Theory` `RL`

### 👁️ Deep & Classical Visual-Inertial Odometry
PyTorch VIO fusing CNN visual encoder + LSTM inertial encoder via residual refiner. Benchmarked vision-only/IMU-only/fused on synthetic Blender data. Also implemented classical S-MSCKF (4th-order RK process model, EKF updates) on EuRoC, evaluated against Vicon ground truth.
> `PyTorch` `MSCKF` `EuRoC` `Blender`

### 🏗️ NeRF & Structure-from-Motion — *Buildings Built in Minutes*
NeRF from scratch in PyTorch (positional encoding, hierarchical sampling, volumetric rendering). Full SfM pipeline: feature matching, RANSAC, essential matrix, PnP, triangulation, bundle adjustment.
> `PyTorch` `3D Neural Rendering` `Multi-View Geometry`

### 🔧 OpenManipulator-X FK/IK & Pick-and-Place
ROS2 forward-kinematics node with explicit homogeneous transforms, analytical IK with elbow-up/down + joint-limit validation, exposed as ROS2 service. Pick-and-place client executing 7-pose Cartesian routine.
> `ROS2` `C++` `Kinematics`

### 📡 GATI — UAV LoRa Payload Deployment
Standalone embedded firmware for autonomous dual-servo payload deployment on UAV platforms. Microsecond-precision servo coordination, arming logic, fail-safe behaviors. Field-validated.
> `Embedded C++` `LoRa` `Real-Time Control`

### 🔬 FPGA Target Identification — Published @ IEEE VLSID 2025
Fine-tuned YOLOv2-Tiny on PYNQ-Z2 FPGA for real-time object detection. Profiled and optimized inference for resource-constrained hardware. Evaluated on 5,000+ COCO validation images.
> 📄 *Hardware Implementation of Target Identification on FPGA*, **IEEE VLSID 2025**

---

## 🛠️ Tech Stack

**Languages**

![C++](https://img.shields.io/badge/C++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![C](https://img.shields.io/badge/C-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)

**Robotics & Perception**

![ROS](https://img.shields.io/badge/ROS%202-22314E?style=for-the-badge&logo=ros&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![PyBullet](https://img.shields.io/badge/PyBullet-3776AB?style=for-the-badge&logoColor=white)
![Blender](https://img.shields.io/badge/Blender-%23F5792A.svg?style=for-the-badge&logo=blender&logoColor=white)

**Embedded & Flight**

![STM32](https://img.shields.io/badge/STM32-03234B?style=for-the-badge&logo=stmicroelectronics&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white)
![Arduino](https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white)
![Pixhawk](https://img.shields.io/badge/Pixhawk-000000?style=for-the-badge&logoColor=white)
![MAVLink](https://img.shields.io/badge/MAVLink-1E5CB3?style=for-the-badge&logoColor=white)

**Tools**

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![LaTeX](https://img.shields.io/badge/LaTeX-008080?style=for-the-badge&logo=latex&logoColor=white)

---

## 📜 Publications

📄 **Hardware Implementation of Target Identification on FPGA** — *IEEE VLSID 2025*
32nd International Conference on VLSI Design & 18th International Conference on Embedded Systems

---

## 🌐 Find Me Here

[![Portfolio](https://img.shields.io/badge/Portfolio-aryanshah.work-000000?style=for-the-badge&logo=googlechrome&logoColor=white)](https://aryanshah.work)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/aryan-shah-03b5b0229)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:work.aryanshah16@gmail.com)
[![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=Instagram&logoColor=white)](https://instagram.com/ar.yxnn)

---

## 📊 GitHub Stats

![](https://github-readme-stats.shion.dev/api?username=Schrodingerrs-cat&theme=dark&hide_border=true&include_all_commits=true&count_private=true)
![](https://streak-stats.demolab.com/?user=Schrodingerrs-cat&theme=dark&hide_border=true)
![](https://github-readme-stats.shion.dev/api/top-langs/?username=Schrodingerrs-cat&theme=dark&hide_border=true&include_all_commits=true&count_private=true&layout=compact)

### 🏆 Trophies

![](https://github-profile-trophy.vercel.app/?username=Schrodingerrs-cat&theme=radical&no-frame=true&no-bg=true&margin-w=4)

---

<p align="center">
  <i>"A robot that doesn't crash is a robot that observed in time."</i>
</p>

[![](https://komarev.com/ghpvc/?username=Schrodingerrs-cat&icon=0&color=0)](https://visitcount.itsvg.in)
