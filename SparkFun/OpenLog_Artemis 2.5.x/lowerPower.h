#ifndef __LOWER_POWER__
#define __LOWER_POWER__

void checkBattery(void);

void powerDownOLA(void);

void resetArtemis(void);

void wakeFromSleep();

void stopLogging(void);

void waitForQwiicBusPowerDelay();

void qwiicPowerOn();

void qwiicPowerOff();

void microSDPowerOn();

void microSDPowerOff();

void imuPowerOn();

void imuPowerOff();

void powerLEDOn();

void powerLEDOff();

uint64_t rtcMillis();

int calculateDayOfYear(int day, int month, int year);

#endif