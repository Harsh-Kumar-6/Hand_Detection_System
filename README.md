# Hand Distance Monitor (OpenCV)

A real-time hand distance monitoring system built using Python and OpenCV.  
The program detects a hand inside a virtual box and classifies the situation into:

- **SAFE** – Hand is far from the box  
- **WARNING** – Hand is getting close  
- **DANGER** – Hand is too close  

This project is useful for safety monitoring, gesture-based interfaces, or experimental HCI systems.

---

## 🚀 Features

- Real-time webcam processing  
- Skin detection using HSV color masking  
- Noise reduction using blur + morphological filters  
- Convex hull contour drawing  
- Hand centroid detection  
- Adjustable SAFE/WARN distances using trackbars  
- Full-screen display  
- FPS counter  
- Screenshot capture (`S` key)

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Hand-Distance-Monitor.git
cd Hand-Distance-Monitor
