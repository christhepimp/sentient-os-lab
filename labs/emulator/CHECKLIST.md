# Emulator lab checklist

Do these on a machine with the Android SDK. This repo cannot boot QEMU for you from GitHub.

- [ ] Android Studio + SDK + platform-tools installed
- [ ] AVD created (note API level, arch, Play vs AOSP)
- [ ] `emulator -list-avds` shows the device
- [ ] `adb devices` shows `device` not `offline`
- [ ] `adb shell id` recorded in a note
- [ ] If not root: AERoot daemon mode **or** Magisk/rootAVD **or** switch to AOSP image
- [ ] `uname -a` and `/proc/version` saved under `~/.sentient-os-lab/`
- [ ] `ps -A` snapshot saved (who is PID 1?)
- [ ] Sentinel run on the *host* first: `python3 -m sentinel status`
- [ ] Later: push Sentinel into the guest with `adb push` and run under `su`
