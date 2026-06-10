#include <Arduino_HS300x.h>
#include <Arduino_LPS22HB.h>
#include <PDM.h>
#include <shaheerkhan-project-1_inferencing.h>

// Noise detection
short sampleBuffer[256];
volatile int samplesRead;

void onPDMdata() {
  int bytesAvailable = PDM.available();
  PDM.read(sampleBuffer, bytesAvailable);
  samplesRead = bytesAvailable / 2;
}

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!HS300x.begin()) {
    Serial.println("Failed to init HS300x!");
    while (1);
  }

  if (!BARO.begin()) {
    Serial.println("Failed to init LPS22HB!");
    while (1);
  }

  PDM.onReceive(onPDMdata);
  if (!PDM.begin(1, 16000)) {
    Serial.println("Failed to init PDM!");
    while (1);
  }

  Serial.println("=== Environment Monitor ===");
  Serial.println("System Ready!");
}

void loop() {
  // Read environmental sensors
  float temperature = HS300x.readTemperature();
  float humidity    = HS300x.readHumidity();
  float pressure    = BARO.readPressure();

  // Read noise level
  float noise = 0;
  if (samplesRead) {
    for (int i = 0; i < samplesRead; i++) {
      noise += abs(sampleBuffer[i]);
    }
    noise = noise / samplesRead;
    samplesRead = 0;
  }

  // Prepare features for model
  float features[] = {temperature, humidity, pressure};
  size_t features_size = 3;

  // Run model
  ei_impulse_result_t result;
  signal_t signal;
  int err = numpy::signal_from_buffer(features, features_size, &signal);
  if (err != 0) {
    Serial.println("Signal error!");
    return;
  }

  EI_IMPULSE_ERROR res = run_classifier(&signal, &result, false);
  if (res != EI_IMPULSE_OK) {
    Serial.println("Classifier error!");
    return;
  }

  // Get best prediction
  const char* prediction = "";
  float max_val = 0;
  for (int i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++) {
    if (result.classification[i].value > max_val) {
      max_val = result.classification[i].value;
      prediction = result.classification[i].label;
    }
  }

  // Print sensor data
  Serial.println("=== Reading ===");
  Serial.print("Temp:       "); Serial.print(temperature); Serial.println(" C");
  Serial.print("Humidity:   "); Serial.print(humidity);    Serial.println(" %");
  Serial.print("Pressure:   "); Serial.print(pressure);    Serial.println(" kPa");
  Serial.print("Noise:      "); Serial.println(noise);
  Serial.print("Model:      "); Serial.println(prediction);
  Serial.print("Confidence: "); Serial.println(max_val);

  // Final work quality decision
  Serial.println("--- RESULT ---");
  if (noise > 1000) {
    Serial.println("Environment: BAD for work!");
    Serial.println("Reason: Too Noisy");
  } else if (strcmp(prediction, "hot") == 0 && max_val > 0.7) {
    Serial.println("Environment: BAD for work!");
    Serial.println("Reason: Too Hot");
  } else if (strcmp(prediction, "noise") == 0 && max_val > 0.7) {
    Serial.println("Environment: BAD for work!");
    Serial.println("Reason: Too Noisy");
  } else if (strcmp(prediction, "normal") == 0 && max_val > 0.7) {
    Serial.println("Environment: GOOD for work!");
    Serial.println("Reason: Normal conditions");
  } else {
    Serial.println("Environment: MODERATE for work");
    Serial.println("Reason: Uncertain conditions");
  }
  Serial.println("==============");
  delay(2000);
}
