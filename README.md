# aryan shah

i teach machines to see, mostly so they don't run into things.

currently a robotics masters student at WPI, working as a research assistant at the **RoboCare Lab** on human daily activity learning and recognition basically teaching a robot to notice when you're brushing your teeth vs. brushing the cat. before this i was in india putting flight controllers on drones and a satellite into the sky (it came back down, eventually, with a 2nd place medal attached). on the side i'm building a perception stack i call **schrödinger's vision** — a name i picked because in my experience the lane line is genuinely both there and not there until something's brave enough to look.

```
location     : worcester, ma
status       : sleep-deprived but enthusiastic
working on   : teaching a humanoid robot to recognize what humans are up to
side quest   : multi-camera autonomous driving perception
aspiring to  : physical AI, VLAs, and other acronyms i'll explain later
```

---

## things i've actually built

**🛣️ [MultiCam Autonomous Driving Perception](https://github.com/Schrodingerrs-cat/MultiCam-AutonomousDriving-Perception)** — 4 cameras, 13 driving sequences, 15+ models stitched together, one tesla FSD-shaped dream. detects lanes, vehicles, pedestrians, traffic lights, optical flow, depth, the works. survives night, tunnels, sunset glare, and dense intersections. fails gracefully when it doesn't.

**🛰️ CanSat** — i co-led a 4-person team that built a satellite the size of a soda can. it had reaction wheels, RF telemetry, sensor fusion, and a healthy fear of gravity. 2nd place nationally at SMOPS 2023 (india's first InSpace CanSat comp). a servo died mid-flight. we adapted. we did not die.

**🚁 Crazyflie quadrotor controls** — cascaded PD with SO(3) attitude control, polynomial trajectories smooth enough that the math is doing more work than the props. 18+ gain configs swept, RL-tuned, well-damped in 3-4.5s. yes i'm proud of it.

**👁️ Visual-Inertial Odometry (deep + classical)** — built a CNN+LSTM VIO from scratch and an S-MSCKF for comparison. trained on synthetic blender data, evaluated on EuRoC against vicon. classical still wins on accuracy. deep wins on style points.

**🏗️ NeRF & SfM from scratch** — positional encoding, hierarchical sampling, volumetric rendering, the whole 3D-is-just-a-function-call deal. plus a full structure-from-motion pipeline because i wanted to know what bundle adjustment actually *does*.

**🔧 OpenManipulator-X** — wrote FK/IK by hand, exposed it as a ROS2 service, ran a 7-pose pick-and-place. the robot picked. the robot placed. occasionally in the right order.

**📡 GATI** — a LoRa-controlled payload deployment system for UAVs. dual servos. microsecond timing. fail-safes. used in the field. did not fall out of the sky.

**🔬 [IEEE VLSID 2025] FPGA target ID** — fine-tuned YOLOv2-Tiny onto a PYNQ-Z2 board because GPUs are too easy. published the paper. the FPGA still runs.

---

## what i actually use

**daily drivers** — `C++` `Python` `ROS2` `PyTorch` `OpenCV` `Linux`

**when the project demands it** — `C` `Bash` `STM32` `Raspberry Pi` `Pixhawk` `MAVLink` `Blender` `PyBullet` `LaTeX`

**aspirationally** — anything with "physical AI" or "VLA" in the name, ask me again in 6 months

---

## elsewhere on the internet

🌐 [aryanshah.work](https://aryanshah.work) · 💼 [linkedin](https://linkedin.com/in/aryan-shah-03b5b0229) · 📧 [email](mailto:work.aryanshah16@gmail.com) · 📸 [instagram](https://instagram.com/ar.yxnn)

---

## the obligatory stats wall

![](https://github-readme-stats.shion.dev/api?username=Schrodingerrs-cat&theme=dark&hide_border=true&include_all_commits=true&count_private=true)
![](https://streak-stats.demolab.com/?user=Schrodingerrs-cat&theme=dark&hide_border=true)
![](https://github-readme-stats.shion.dev/api/top-langs/?username=Schrodingerrs-cat&theme=dark&hide_border=true&include_all_commits=true&count_private=true&layout=compact)

---

<sub>if you're a recruiter: hi 👋 i'm looking for summer/fall 2026 roles in perception, autonomy, or embedded robotics. the email above works. the linkedin is faster.</sub>

<sub>if you're a robot reading this: don't crash.</sub>
