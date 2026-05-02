# 🌱 Plant Stress & Disease Prediction System (IoT + Custom ML Model)

## 📌 Project Overview

This project presents an intelligent plant monitoring and disease prediction system that combines **IoT hardware** and a **custom-built machine learning model**. It collects real-time environmental data using sensors and predicts whether a plant is under stress or likely to develop a disease.

The system is designed to support **precision agriculture**, enabling early detection of unfavorable conditions and improving plant health management.

---

## 🎯 Objectives

* Monitor environmental parameters affecting plant health
* Detect plant stress conditions in real time
* Predict disease likelihood using a custom ML model
* Store and visualize data using cloud platforms

---

## 🧰 Hardware Components

* ESP8266 – Microcontroller with built-in WiFi
* DHT11 – Measures temperature and humidity
* Soil Moisture Sensor – Measures soil water content
* Rain Sensor – Detects rainfall presence
* Jumper Wires – For circuit connections
* Breadboard – For prototyping

---

## ⚙️ Software & Tools

* Python (Data processing & model development)
* Google Sheets (Data collection & storage)
* Arduino IDE (ESP8266 programming)
* Blynk (optional for visualization)
* Libraries:

  * NumPy
  * Pandas
  * Scikit-learn

---

## 📊 Dataset Description

The dataset consists of real-time and augmented sensor readings:

| Feature       | Description                                     |
| ------------- | ----------------------------------------------- |
| Temperature   | Ambient temperature (°C)                        |
| Humidity      | Relative humidity (%)                           |
| Soil Moisture | Soil condition (analog value)                   |
| Rain          | Rain presence (0/1)                             |
| Stress        | Target variable (0 = Healthy, 1 = Disease Risk) |

* Total dataset size: ~300+ rows
* Balanced distribution between stress and non-stress conditions
* Includes both real sensor data and synthetic augmentation

---

## 🧠 Custom Machine Learning Model

### 🌟 E.L.S.A Model

**Environmental Learning with Stress Attention**

This project introduces a **custom-built model** that:

* Applies **dynamic attention** to environmental features
* Uses **cost-sensitive learning** to prioritize disease detection
* Implements **momentum-based optimization** for stable training
* Produces predictions using a sigmoid activation function

### Key Features:

* Adaptive feature importance
* Focus on high-stress conditions
* Improved recall for disease prediction
* Fully self-implemented (no pre-built ML model used)

---

## 🔄 System Workflow

1. Sensors collect environmental data
2. ESP8266 transmits data
3. Data stored in Google Sheets
4. Dataset prepared and cleaned
5. Custom ML model trained
6. Model predicts plant stress/disease
7. Results analyzed and visualized

---

## 📈 Model Evaluation Metrics

* Accuracy
* Precision
* Recall
* F1 Score

These metrics ensure reliable performance in detecting plant stress conditions.

---

## 🚀 How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/plant-stress-detector.git
cd plant-stress-detector
```

### 2. Install Dependencies

```bash
pip install numpy pandas scikit-learn
```

### 3. Run the Model

```bash
python model.py
```

---

## 💾 Output

* Model predictions (0/1)
* Accuracy and performance metrics
* Saved model file (`elsa_model.pkl`)

---

## 🌿 Applications

* Smart agriculture
* Automated irrigation systems
* Greenhouse monitoring
* Early disease detection

---

## 🔮 Future Enhancements

* Add more sensors (light, pH, CO₂)
* Deploy real-time dashboard
* Improve model with temporal data
* Mobile app integration

---

## 🎓 Conclusion

This project demonstrates how **IoT and custom machine learning** can be combined to create an intelligent system for plant health monitoring. The proposed model provides a unique, explainable, and effective approach to predicting plant stress and disease.

---

## 📬 Author

Priya Jenita

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!

