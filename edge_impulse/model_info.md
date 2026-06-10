# Edge Impulse Model Information

## Project
- **Project Name:** shaheerkhan-project-1
- **Platform:** Edge Impulse Studio
- **Target Device:** Arduino Nano 33 BLE Sense

## Model Architecture
- **Type:** Fully Connected Neural Network
- **Quantization:** INT8 (optimized for microcontroller)
- **Input:** 4 features (temperature, humidity, pressure, noise)
- **Output:** 3 classes (normal, hot, noise)

## Training Configuration
| Parameter | Value |
|-----------|-------|
| Training Cycles | 30 |
| Learning Rate | 0.05 |
| Validation Set Size | 25% |
| Training Processor | CPU |

## Performance
| Metric | Training | Validation | Test |
|--------|----------|------------|------|
| Accuracy | 97.2% | 89.1% | 87.4% |
| Precision | 96.8% | 88.7% | 86.9% |
| Recall | 97.0% | 89.3% | 87.1% |
| F1 Score | 96.9% | 89.0% | 87.0% |

## Labels
| Label | Description |
|-------|-------------|
| `normal` | Normal comfortable room conditions |
| `hot` | High temperature environment |
| `noise` | Noisy environment |

## Deployment
The model was exported as an Arduino library (.zip) from Edge Impulse and installed in Arduino IDE via **Sketch → Include Library → Add .ZIP Library**.
