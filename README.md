Pi-Nova-5
=========

This project is a Raspberry Pi powered sensor module that: 

* Senses motion and luminosity
* Interfaces with the [Philips HUE Wireless Lighting](http://www.meethue.com) system to automatically turn on lights when motion is detected and luminosity is below a user defined threshold.
* Logs the date/time of motion events and periodically sends that data back to [Holly](https://github.com/projectweekend/Holly) for storage in a database.
* Pulls user configurations from [Holly](https://github.com/projectweekend/Holly) at regular intervals using a cron job.

![Picture of Raspberry Pi Device](http://i.imgur.com/loscJYd.jpg)
