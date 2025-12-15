import subprocess
import sys
import os

SCENARIOS = [
    {
        "name": "Quick Test (Development/CI)",
        "users": 10,
        "spawn_rate": 5,
        "run_time": "1m"
    },
    {
        "name": "Gradual Load Increase",
        "users": 20,
        "spawn_rate": 1,
        "run_time": "5m"
    },
    {
        "name": "Spike Test",
        "users": 50,
        "spawn_rate": 10,
        "run_time": "2m"
    },
    {
        "name": "Sustained Load (15m)",
        "users": 30,
        "spawn_rate": 2,
        "run_time": "15m"
    },
    {
        "name": "Stress Test",
        "users": 100,
        "spawn_rate": 10,
        "run_time": "5m"
    },
    {
        "name": "Soak Test (30m)",
        "users": 25,
        "spawn_rate": 1,
        "run_time": "30m"
    },
    {
        "name": "Chaos Test",
        "users": 75,
        "spawn_rate": 5,
        "run_time": "10m"
    },
    {
        "name": "Breakpoint Test",
        "users": 200,
        "spawn_rate": 5,
        "run_time": "30m"
    }
]

def print_menu():
    print("\nFalLab Stress Test Scenarios\n")
    for i, s in enumerate(SCENARIOS, 1):
        print(f"{i}. {s['name']}")
    print("0. Exit")

def run_scenario(idx):
    s = SCENARIOS[idx]
    cmd = [
        "locust",
        "-f", "locustfile.py",
        f"--users={s['users']}",
        f"--spawn-rate={s['spawn_rate']}",
        f"--run-time={s['run_time']}",
        "--host=http://localhost:8000",
        "--stop-timeout=60"
    ]
    print(f"\nRunning: {s['name']}")
    print(" ".join(cmd))
    subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        idx = int(sys.argv[1]) - 1
        if 0 <= idx < len(SCENARIOS):
            run_scenario(idx)
        else:
            print("Invalid scenario number.")
    else:
        while True:
            print_menu()
            choice = input("Select scenario (0 to exit): ").strip()
            if choice == "0":
                break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(SCENARIOS):
                    run_scenario(idx)
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")
