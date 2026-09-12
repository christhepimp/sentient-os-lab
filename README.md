# Sentient OS Lab

An experimental lab for building an **AI-native operating system**.

The OS is not a theme on top of Linux. The long-term target is that **the OS itself is an AI**: it plans, schedules, talks to the user, manages resources, and gradually takes over jobs that Linux daemons do today.

You cannot swap Linux out in one night. This repo treats that honestly. We start on a **rooted Android emulator** (Linux kernel + Android userspace), get a real root shell, then **replace pieces of userspace one service at a time** with an AI runtime.

Repo: https://github.com/christhepimp/sentient-os-lab

## What this is (and is not)

**This is**

- A research + engineering scaffold
- A documented path from emulator root → Linux userspace → AI supervisor → replacement of init/services
- A place to put kernel notes, emulator recipes, and a tiny AI runtime that pretends to be PID 1 for selected tasks

**This is not**

- A finished OS you can boot as your daily driver
- A drop-in Linux replacement
- A claim that we already wrote a new kernel

Replacing the Linux kernel is a multi-year systems project (boot, memory, drivers, filesystems, scheduling, security). The practical path is:

1. Keep the Linux kernel as hardware abstraction for now.
2. Own userspace (init, package manager, shell, windowing, policy).
3. Make an AI process the policy engine and eventually the init/supervisor.
4. Only later consider a custom kernel or unikernel if the AI runtime needs different primitives.

That is how real OS projects actually grow.

## Phase 0 — Host: rooted Android emulator

Android already runs a Linux kernel. A rooted emulator gives you:

- `adb` access
- root (`uid=0`)
- a full Linux-like filesystem to inspect (`/proc`, `/sys`, `/dev`)
- a sandbox that will not brick a phone

### Recommended stack (2026)

| Role | Tool | Why |
| --- | --- | --- |
| Official emulator | Android Studio AVD (Google APIs / AOSP image) | Best kernel/debug surface |
| On-the-fly root on Play images | [AERoot](https://github.com/quarkslab/AERoot) | Roots processes on Google Play AVDs via QEMU gdb stub |
| Persistent Magisk root on AVD | [rootAVD](https://github.com/newbit1/rootAVD) + Magisk | App-level root, modules, `su` |
| Fast desktop Android-on-Linux | [Waydroid](https://waydro.id) | Containerized Android sharing the host kernel |
| Full x86 Android OS in a VM | Bliss OS / Android-x86 | Easier to treat as a real machine |
| Cloud/dev farm with root option | Genymotion (selected images) | Root can be enabled on some images |

**Practical default for this lab:** Android Studio AVD with an AOSP or Google APIs image + AERoot *or* a Magisk-patched image via rootAVD.

Play Store images often block `adb root`. AERoot patches credentials in the guest kernel so `adbd` or a chosen process becomes uid 0. AOSP images from the SDK frequently already start `adbd` as root.

### Minimal AVD + root flow

```bash
# 1. Create an AVD (example: API 34 x86_64 AOSP, not Play Store if you want easy adb root)
# Android Studio → Device Manager → New Device → system image without Play if possible

# 2. Start emulator with QEMU gdb stub if you will use AERoot
emulator -avd YOUR_AVD -qemu -s

# 3. Confirm shell
adb devices
adb shell id

# If you are already uid 0, you are done for Phase 0.
# If not (Play image), use AERoot daemon mode so new adb shells are root:
#   pip install aeroot
#   aeroot daemon
```

Once rooted:

```bash
adb shell
# inside guest
uname -a
cat /proc/version
ps -A | head
ls /
mount
```

You are now *inside Linux* on the emulator: same kernel family as a phone, same procfs, same permission model.

## Phase 1 — See Linux, do not fight it yet

Map what we will replace later:

- init: Android `init` + `servicemanager` / `hwservicemanager` (not systemd)
- binder IPC instead of classic Unix dbus on the Android side
- zygote / app runtime
- `adbd`, `logd`, `vold`, `netd`, surfaceflinger

On the Linux-desktop side of the same idea (optional parallel track):

- systemd / OpenRC
- udev, dbus, NetworkManager
- a display server

Documents in `docs/` record these maps so the AI runtime knows which sockets and units it is allowed to eat.

## Phase 2 — Drop an AI supervisor into userspace

Directory `runtime/` is a small Python supervisor called **Sentinel**.

Sentinel is the first draft of "the OS is an AI":

- reads intent from a chat/CLI
- owns a allowlist of actions (inspect proc, start/stop *lab* services, write lab state)
- never claims to be the kernel
- can later sit where init would fork helpers

This is how replacement starts: **policy and orchestration first**, syscalls later.

## Phase 3 — Replace Linux *services*, not the kernel

Order of replacement (safe → dangerous):

1. Lab shell / intent interface (done as prototype in this repo)
2. Job scheduler / cron analog
3. Package / capability installer for lab modules
4. Logging and policy (what may run)
5. Network policy helper
6. A userspace init that supervises *our* daemons only
7. Optional: custom init on a dedicated VM, still on Linux kernel
8. Far future: new kernel or hypervisor guest if the AI runtime needs different primitives

Skipping to step 8 first is how projects die.

## Architecture (target)

```
+---------------------------------------------------+
|  User intent  (voice / text / app)                |
+-------------------------+-------------------------+
                          |
                          v
+---------------------------------------------------+
|  Sentinel  — AI OS runtime                        |
|  plan • policy • memory • tool use                |
+-------------------------+-------------------------+
                          |
          +---------------+---------------+
          v                               v
+---------------------+       +---------------------+
|  Lab services       |       |  Still-Linux layer  |
|  (we own these)     |       |  kernel, drivers,   |
|                     |       |  Android init,      |
|                     |       |  hardware           |
+---------------------+       +---------------------+
                          |
                          v
              rooted Android emulator / VM
```

## Repo layout

```
docs/                 research notes, emulator recipes, Linux map
runtime/sentinel/     AI supervisor prototype
labs/emulator/        scripts and checklists for AVD + root
services/             future replacements for Linux/Android daemons
LICENSE
```

## Status

- [x] Repo and vision
- [x] Emulator + root research notes
- [x] Sentinel stub (inspect host, plan actions, refuse unsafe ones)
- [ ] Real AVD automation scripts tested on a machine with the Android SDK
- [ ] Binder/init replacement experiments
- [ ] Persistent memory and tool plugins
- [ ] Custom kernel — not started (and should not be, yet)

## Safety

This lab is for **your own emulator or VM**. Do not use these notes to attack devices you do not own. Root on an emulator is a debug feature. Shipping a rooted Play image as a product is a different (and usually bad) idea.

## License

MIT. See `LICENSE`.
