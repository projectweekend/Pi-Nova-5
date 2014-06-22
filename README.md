## Moving along...
The Raspberry Pi functionality of this project was in the process of being rewritten when I decided to move it into another project [Ar-Dock](https://github.com/projectweekend/Ar-Dock). The v1 release tag of this project encapsulates the original working project prior to the rewrite. Going forward, this repository will not be maintained.

This is the Raspberry Pi component of a system that interfaces with the [Philips HUE Wireless Lighting](http://www.meethue.com) system to automatically turn on lights when motion is detected and luminosity is below a user defined threshold. The actual motion and luminosity sensor component can be found here: [Ar-Nova-5](https://github.com/projectweekend/Ar-Nova-5).

------------------------------------------------------------------------------

### Installation

------------------------------------------------------------------------------

#### Step 1: Clone this repository

```
git clone https://github.com/projectweekend/Pi-Nova-5.git
```

#### Step 2: Run install script

From the project directory `Pi-Nova-5/`, run the following command:

```
./install.sh
```

**NOTE:** This step will probably take several minutes to complete. When the script starts to install [Upstart](http://upstart.ubuntu.com/), you will receive a warning message. It will prompt you to type the following message to confirm the installation: `Yes, do as I say!`. You must type it exactly.

#### Step 3: Reboot

```
sudo reboot
```

------------------------------------------------------------------------------

### Setup

------------------------------------------------------------------------------

Coming soon...
