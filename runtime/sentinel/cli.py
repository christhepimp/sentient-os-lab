"""Command line for the Sentinel supervisor.

This is userspace. It does not replace the kernel.
It is the first place policy lives so we can grow an AI OS around it.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path

ALLOWED_INTENTS = {
    "status": "Describe this host and Sentinel's role.",
    "inspect": "Read safe host facts (os, cpu, pid, hostname).",
    "plan": "Turn a user goal into a staged replacement plan.",
    "remember": "Write a note into lab state.",
}


def lab_state_dir() -> Path:
    root = Path(os.environ.get("SENTINEL_STATE", Path.home() / ".sentient-os-lab"))
    root.mkdir(parents=True, exist_ok=True)
    return root


def host_facts() -> dict:
    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "python": sys.version.split()[0],
        "pid": os.getpid(),
        "uid": getattr(os, "getuid", lambda: None)(),
        "cwd": os.getcwd(),
        "time": datetime.now(timezone.utc).isoformat(),
        "role": "userspace-supervisor",
        "kernel_owned_by_sentinel": False,
    }


def plan_for(goal: str) -> dict:
    return {
        "goal": goal,
        "honest_scope": "AI OS runtime in userspace; Linux kernel stays",
        "stages": [
            "Run on a rooted Android emulator or a Linux VM",
            "Inspect init, procfs, and running services — do not delete them",
            "Let Sentinel own lab jobs and policy",
            "Replace one daemon at a time with a Sentinel plugin",
            "Only after that consider a custom init",
            "A new kernel is a later project, not this commit",
        ],
    }


def remember(note: str) -> Path:
    path = lab_state_dir() / "memory.jsonl"
    rec = {"t": datetime.now(timezone.utc).isoformat(), "note": note}
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sentinel", description="AI-native OS supervisor stub")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status")
    sub.add_parser("inspect")
    p_plan = sub.add_parser("plan")
    p_plan.add_argument("goal", nargs="+", help="what you want the OS to become")
    p_mem = sub.add_parser("remember")
    p_mem.add_argument("note", nargs="+")
    sub.add_parser("intents")

    args = parser.parse_args(argv)

    if args.cmd == "status":
        print(json.dumps({"sentinel": "0.1.0", "intents": ALLOWED_INTENTS, "host": host_facts()}, indent=2))
        return 0
    if args.cmd == "inspect":
        print(json.dumps(host_facts(), indent=2))
        return 0
    if args.cmd == "plan":
        print(json.dumps(plan_for(" ".join(args.goal)), indent=2))
        return 0
    if args.cmd == "remember":
        path = remember(" ".join(args.note))
        print(json.dumps({"wrote": str(path)}, indent=2))
        return 0
    if args.cmd == "intents":
        print(json.dumps(ALLOWED_INTENTS, indent=2))
        return 0
    return 1
