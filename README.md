<div align="center">

### *Facial Emotion Based Robot; An Autonomous Emotion-Driven Raspberry Pi 5 Mobile Platform*

> **A differential-drive robot that reads human emotions through Deep Learning and responds with physical movement — bridging high-level Computer Vision with low-level hardware control to exhibit genuinely "social" behavior.**

<br/>

---

</div>

<br/>

## 🧠 What It Does

The **Emotion Robot** observes your face through a camera stream, classifies your emotional state in real time using a neural network, and physically reacts:

| Detected Emotion | Robot Behavior | Reasoning |
|:---:|:---:|:---|
| 😊 **Happy** | Drive **Forward** | Engagement — move closer |
| 😢 **Sad** / 😡 **Angry** / 😨 **Fear** | Drive **Backward** | Avoidance — respect the mood |
| 😐 **Neutral** | **Hold Position** | Observation state |
| ❓ **Lost Target** | **Spin & Search** | Re-acquisition via Last Known Position |

<br/>

---

## 📌 Credits & Attribution

This project is a **hardware-integrated fork** of the [Realtime Facial Emotion Analyzer](https://github.com/susantabiswas/realtime-facial-emotion-analyzer) by **Susanta Biswas**.

<details>
<summary><strong>Project Evolution</strong></summary>

<br/>

**Original Core**
- Deep learning emotion classification pipeline using TensorFlow / Keras

**Enhancements in This Fork**
- Physical mobility via **L298N Motor Driver** integration
- Optimized for **Raspberry Pi 5** via TCP camera streaming to bypass `libcamera` lag
- **Coordinate normalization** to accurately track users across the X-axis
- **State-based search routines** using "Last Known Position" memory

</details>

<br/>

---

## 🚀 Key Features

<br/>

### Affective Behavioral Mapping
The robot's motion is directly driven by emotion — not scripted paths or obstacle maps, but live neural inference.

### Directional Memory
The robot continuously classifies your position as **Left**, **Center**, or **Right** within its field of view, maintaining spatial context even between detections.

### Intelligent Recovery
When the face is lost from frame, the robot **spins toward the last known position** rather than spinning blindly — dramatically improving re-acquisition speed.

### High-Speed Vision Pipeline
A **TCP-based video stream** (`libcamera → tcp://`) decouples capture from inference, maintaining high FPS on the Raspberry Pi 5 without the latency penalty of direct `libcamera` calls.

<br/>

---

## 🛠️ Hardware Architecture

```
┌──────────────────────────────────────────────────────┐
│                   EMOTION ROBOT                      │
│                                                      │
│  ┌─────────────┐      ┌──────────────────────────┐   │
│  │  Camera     │────▶│   Raspberry Pi 5 (8GB)    │  │
│  │  Module 3   │      │                           │  │
│  └─────────────┘      │   • TensorFlow / Keras    │  │
│                       │   • Emotion Classifier    │  │
│  ┌─────────────┐      │   • TCP Stream Client     │  │
│  │  Pi Power   │────▶│   • Motor Logic           │  │
│  │  Bank       │      └────────────┬─────────────┘   │
│  └─────────────┘                   │                 │
│                                    ▼                 │
│  ┌─────────────┐      ┌──────────────────────────┐   │
│  │  4× AA      │────▶│   L298N H-Bridge Driver   │  │
│  │  Battery    │      └────────────┬─────────────┘   │
│  └─────────────┘                   │                 │
│                                    ▼                 │
│                        ┌──────────────────────────┐  │
│                        │  2-Wheel Differential    │  │
│                        │  Drive + Swivel Caster   │  │
│                        └──────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

| Component | Specification |
|:---|:---|
| **Brain** | Raspberry Pi 5 — 8 GB |
| **Muscle** | L298N Dual H-Bridge Motor Driver |
| **Vision** | Raspberry Pi Camera Module 3 |
| **Chassis** | 2-Wheel Differential Drive + Swivel Caster |
| **Power (Logic)** | Dedicated Pi Power Bank |
| **Power (Motors)** | 4× AA Battery Pack |

<br/>

---

## ⚙️ Technical Deep-Dive

### Coordinate Normalization

Raw camera coordinates caused a persistent **"Always Left" detection bug** — the face's pixel X position was being compared against the full camera resolution, but the AI processes a resized frame (`0.3×` scale).

The fix: normalize against the **detection width**, not the camera width.

$$\text{Relative Position} = \frac{\text{Face Center} x}{\text{Detection Width}}$$

This maps position to a `[0.0 → 1.0]` range regardless of resolution or resize factor, giving accurate left/center/right classification.

<br/>

---

## 🏃 Setup & Execution

### Step 1 — Clone the repository:

```bash
git clone https://github.com/tudorrad/Facial-emotion-robot.git
cd Facial-emotion-robot
```

### Step 2 — Install Dependencies:

> It is recommended to use a virtual environment or Conda to avoid system conflicts.

```bash
pip install -r requirements.txt
```

<br/>

### Step 3 — Start the Video Stream

Open **Terminal 1** and launch the `libcamera` TCP listener:

```bash
libcamera-vid -t 0 --inline --listen -o tcp://0.0.0.0:8888
```

> `-t 0` runs indefinitely. `--listen` opens a TCP server on port `8888`.

<br/>

### Step 4 — Run the Robot Logic

Open **Terminal 2** and launch the main affective tracking script:

```bash
python video_main.py
```

The robot will begin streaming, classifying emotions, and driving accordingly.

<br/>

> **Tip:** Run `python test_stream.py` first to verify the camera TCP connection is healthy before starting the full pipeline.

<br/>

---

## 📂 Project Structure

```
emotion-robot/
│
├── video_main.py       # Main loop — AI inference + behavioral logic
├── motors.py           # Low-level GPIO control for L298N driver
├── test_stream.py      # Diagnostic tool for TCP camera stream verification
│
└── models/
    └── # Pre-trained emotion classification weights
```

<br/>

---

## 📜 License

This project inherits the **MIT License** from the original repository by Susanta Biswas.
See [`LICENSE`](LICENSE) for full copyright details and permissions.

<br/>

---
