#include "I2Cdev.h"
#include "MPU6050.h"
#include <ESP8266WiFi.h>

#define TO_DEG 57.2957f  //константа перевода из радиан в градусы
#define TIME_OUT 10

MPU6050 accgyro;

long int t1;
const int MPU_addr = 0x68;
int agl[4];
bool flag = true;
const unsigned long *number;

// Определяем параметры сети
const char *ssid = "AndroidAPBF9F";
const char *password = "ser123456";

// Определяем адрес сервера
const char *ADDR = "192.168.11.119";

// Определяем url подключения
const char *URL = "/";
// Определяем порт
const uint16_t PORT = 2023;





void setup() {

  Serial.begin(115200);
  accgyro.initialize();
  Wire.begin();
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void loop() {

  angl_xyz(&agl[0], &agl[1], &agl[2], &agl[3]);
  delay(10);
}


void angl_xyz(int *ax, int *ay, int *az, int *t) {
  *t = millis();
  if (t1 < *t) {
    int16_t ax, ay, az, gx, gy, gz;

    accgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    //  Serial.println(gx);
    //  Serial.println(gy);
    //  Serial.println(gz);
    float g = sqrt(gx * gx + gy * gy);
    float g2 = sqrt(gx * gx + gy * gy + gz * gz);

    float cos_x = gx / g;
    float cos_y = gy / g;
    float cos_z = gz / g2;

    //получить значение в градусах (возможно убрать - 90)
    int aglx = abs(TO_DEG * acos(cos_x) - 90);
    int agly = abs(TO_DEG * acos(cos_y) - 90);
    int aglz = abs(TO_DEG * acos(cos_z) - 90);

    seeding(aglx, agly, aglz);

  }
}

void seeding(float aglx, float agly, float aglz){
  WiFiClient client;

  if (!client.connect(ADDR, PORT)) {
    delay(50);
  }
    String msg;

    msg = String(aglx) + '/' + String(agly) + '/' + String(aglz);
    Serial.println(msg);
    client.println(msg);
    client.stop();


}

