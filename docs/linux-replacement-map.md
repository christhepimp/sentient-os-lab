# Replacement map

The OS we want: **an AI that is the operating system** — it receives intent, holds policy, schedules work, and talks to hardware through the thinnest possible substrate.

Linux today is that substrate. We peel it, we do not nuke it.

## Keep for a long time

- CPU / interrupt / SMP bring-up
- Virtual memory and page tables
- Device drivers (GPU, storage, net, input)
- Filesystems or a VFS over a simpler store
- Syscall or hypercall boundary

Replacing these is writing a kernel. Out of scope until Sentinel actually needs different primitives.

## Replace first (userspace)

| Linux / Android piece | AI-OS analog |
| --- | --- |
| Shell + rc scripts | Sentinel intent loop |
| cron / job scheduler | Sentinel planner |
| systemd units / Android init `.rc` | Sentinel service graph |
| package manager | capability / skill installer |
| syslog / logd | Sentinel episode log |
| policy / SELinux labels (lab only) | Sentinel allowlist |
| settings / getprop | Sentinel world state |

## Replace later

| Piece | Why later |
| --- | --- |
| PID 1 | If Sentinel dies, the machine dies. Need a tiny watchdog first. |
| Binder / dbus | IPC rewrite |
| SurfaceFlinger / compositor | Only if the AI OS owns UI |
| Zygote / ART | Android app compat is a product, not the OS core |

## Hard rule

Sentinel may only control processes and files under `labs/` state and explicitly allowlisted guest paths. No "chmod 777 /system" experiments in default scripts.
