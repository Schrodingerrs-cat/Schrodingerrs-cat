aryan shah
i teach machines to see, reason, and occasionally avoid running into things.

I'm a master's student in Robotics Engineering at Worcester Polytechnic Institute, and a research assistant at the RoboCare Lab, where I work on learning and recognizing human daily activities. The goal: robots that can understand what people are doing, not just detect that people exist.

Before that, I worked on UAV flight controllers, embedded systems, and a CanSat in India. These days, I'm drawn to robot perception, state estimation, autonomy, and physical AI — especially the awkward space between an algorithm that works in a notebook and a robot that works in the real world.

On the side, I'm building Schrödinger's Vision, a multi-camera autonomous-driving perception stack. The lane line is simultaneously there and not there until the model looks at it.
location       San Jose, CA / Worcester, MA
currently      human activity recognition · RoboCare Lab
building       Schrödinger's Vision · multi-camera perception
interested in  perception · VIO/SLAM · autonomy · physical AI · VLAs
status         probably debugging a coordinate frame
portfolio · linkedin · email · instagram
selected builds
Schrödinger's Vision — multi-camera driving perception
4 cameras · 13 driving sequences · 15+ models

A modular perception stack combining lane and object detection, segmentation, tracking, optical flow, depth, traffic-light understanding, and multi-camera scene interpretation. Tested across night driving, tunnels, sunset glare, and dense intersections.

The interesting part isn't when every model agrees. It's what happens when they don't.
CanSat — a satellite in a soda can
8-person team · 2nd place nationally, SMOPS 2023

Co-led development of a CanSat with reaction-wheel control, RF telemetry, and sensor fusion. We dealt with hardware failure during flight and still brought home a podium finish. Gravity provided the final integration test.
Crazyflie — quadrotor control
SO(3) attitude control · cascaded PD · trajectory generation

Implemented cascaded position/attitude control and polynomial trajectory tracking; evaluated 18+ gain configurations and explored RL-based tuning. Measured settling behavior in the 3–4.5 s range.
Visual-inertial odometry — learning vs. geometry
CNN + LSTM · S-MSCKF · EuRoC · Vicon ground truth

Built a learned visual-inertial estimator and a classical filter-based VIO pipeline, trained with synthetic Blender data and evaluated against EuRoC ground truth. The classical approach was more accurate in these experiments — a useful reminder that newer doesn't automatically mean better.
NeRF + structure from motion
positional encoding · hierarchical sampling · volumetric rendering · bundle adjustment

Implemented neural rendering components and a separate SfM pipeline to understand how images become camera poses, sparse geometry, and ultimately 3D representations.
<details>
<summary><b>more things I've built</b></summary>- OpenManipulator-X: derived forward/inverse kinematics, exposed them through ROS 2 services, and executed a seven-pose pick-and-place sequence.
- GATI: built a LoRa-controlled UAV payload deployment system with dual servos, microsecond-scale timing, and failsafes; field-tested.
- FPGA target identification: deployed a fine-tuned YOLOv2-Tiny model on a PYNQ-Z2 and published the work at IEEE VLSID 2025.
</details>tools of the trade
most days: C++ Python ROS 2 PyTorch OpenCV Linux

robotics + embedded: C STM32 Pixhawk MAVLink Raspberry Pi LoRa

simulation + research: Blender PyBullet Bash LaTeX

currently exploring: vision-language-action models, embodied learning, and making learned perception survive real-world deployment.
github, in numbers
<!-- Live public activity cards: counts may differ from GitHub's own contribution graph. -->
<div align="center">
  <img src="https://ghstats.dev/api/card?username=Schrodingerrs-cat&theme=tokyonight" alt="GitHub activity, repositories, stars and contributions" width="58%" />
  <img src="https://ghstats.dev/api/languages?username=Schrodingerrs-cat&theme=tokyonight&layout=compact" alt="Languages across public repositories" width="38%" />
</div><div align="center">
  <img src="https://streak-stats.demolab.com/?user=Schrodingerrs-cat&theme=tokyonight&hide_border=true" alt="GitHub contribution streak" />
</div><details>
<summary><b>what these numbers don't show</b></summary>- Real robot debugging, hardware bring-up, and lab experiments don't always produce public commits.
- Language percentages reflect repository code, not proficiency or time spent.
- Private work and third-party GitHub statistics may be incomplete or counted differently.
</details>what i'm interested in next
Robots that can perceive, estimate, plan, and act outside carefully controlled demos. Particularly interested in perception and autonomy research, embedded robotics, and the bridge from classical estimation/control to learned policies and VLAs.

Want to talk robotics, collaborate on a project, or discuss an opportunity? Email me or find me on LinkedIn.

<sub>if you're a robot reading this: please check your coordinate frames before moving.</sub>
