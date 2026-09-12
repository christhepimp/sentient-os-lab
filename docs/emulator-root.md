# Rooted Android emulator notes

Goal of this doc: pick a host where we can get a **root Linux shell** without a physical phone.

## Why an emulator first

- Snapshot / wipe if we brick userspace
- `adb` and QEMU debug stubs
- Same Linux kernel family Android uses
- Legal and safe on hardware you control

## Option A — Android Studio AVD (recommended lab default)

1. Install Android Studio + SDK + emulator.
2. Create an AVD.
   - Prefer **AOSP / Google APIs** images over **Google Play** images when you want `adb root`.
   - Play images lock `adbd` as non-root.
3. Start the AVD.
4. `adb shell id`
   - If `uid=0(root)`, Phase 0 is done.
   - If not, use Option A2.

### A2 — AERoot on Play-flavored AVDs

Project: https://github.com/quarkslab/AERoot

AERoot attaches to the emulator via the QEMU gdb stub (`emulator ... -qemu -s`) and patches process credentials in guest kernel memory so a chosen PID, process name, or `adbd` becomes root.

```text
pip install aeroot
emulator @YOUR_AVD -qemu -s
aeroot daemon     # subsequent adb shells come up root
```

Requires gdb with Python. Kernel table in AERoot README must match your AVD kernel.

Predecessor: https://github.com/airbus-seclab/android_emuroot

### A3 — Magisk on AVD (rootAVD)

Guide pattern used in security labs: patch the system/ramdisk image with Magisk so `su` exists inside the guest.

Useful when you want Magisk modules, Zygisk, or app-visible root — not only an `adbd` root shell.

Reference writeup: "Rooting an Android Emulator for Mobile Security Testing" (8kSec) using rootAVD + Magisk.

## Option B — Genymotion

Desktop VM-based Android. Some images can be rooted dynamically. Good for QA; less ideal if you want to stare at AOSP init.

## Option C — Waydroid on Linux desktop

Android (Lineage-based) in an LXC container sharing the **host** Linux kernel. Near-native. Root story depends on how you init the container. Excellent if the long-term AI OS is meant to live on a Linux desktop first.

## Option D — Bliss OS / Android-x86 in VirtualBox or QEMU

Treat Android as a full PC OS. Easier mental model: one VM, one kernel, one root account.

## Option E — Linux VM instead of Android

If the Android layer is getting in the way, run Debian/Alpine under QEMU and put Sentinel there. The kernel is still Linux. That is fine for Phase 2–3.

## What "get in the Linux code" means here

Three different layers people mix up:

| Layer | Where it lives | What we do in this lab |
| --- | --- | --- |
| Linux kernel source | kernel.org / AOSP kernel trees | Read, do not fork yet |
| Guest userspace | `/system`, `/vendor`, `/init` on the AVD | Inspect with root, replace *our* services |
| Host tools | SDK emulator, QEMU, adb | Automate in `labs/emulator` |

Replacing "Linux" starts at userspace policy (Sentinel), not by deleting `vmlinux` on day one.

## First commands after root

```bash
adb shell uname -a
adb shell cat /proc/version
adb shell getprop ro.build.version.release
adb shell ls /init* /system/bin/init 2>/dev/null
adb shell ps -A | head -40
adb shell cat /proc/1/cmdline; echo
```

PID 1 on Android is Android `init`, not systemd. Any "replace Linux" plan that assumes systemd on the phone image is already wrong.
