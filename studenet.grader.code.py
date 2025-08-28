class VacuumCleaner:
    def __init__(self, shape):
        self.shape = shape
        self.state = "stopped"

    def start(self):
        self.state = "running"
        print(f"{self.shape} vacuum started cleaning.")

    def stop(self):
        self.state = "stopped"
        print(f"{self.shape} vacuum stopped cleaning.")

    def left(self):
        if self.state == "running":
            print(f"{self.shape} vacuum turned left.")
        else:
            print(f"{self.shape} vacuum must be started first.")

    def right(self):
        if self.state == "running":
            print(f"{self.shape} vacuum turned right.")
        else:
            print(f"{self.shape} vacuum must be started first.")

    def dock(self):
        self.state = "docked"
        print(f"{self.shape} vacuum returned to dock.")


# Available vacuum shapes
shapes = {
    "1": "Circle",
    "2": "Square",
    "3": "Triangle",
    "4": "Hexagon"
}

print("Choose a Vacuum Cleaner Shape:")
for key, value in shapes.items():
    print(f"{key}. {value}")

choice = input("Enter your choice (1-4): ")

if choice in shapes:
    vac = VacuumCleaner(shapes[choice])
    print(f"\nYou chose {shapes[choice]} Vacuum Cleaner.\n")

    while True:
        command = input("Enter command (start/stop/left/right/dock/exit): ").lower()
        
        if command == "start":
            vac.start()
        elif command == "stop":
            vac.stop()
        elif command == "left":
            vac.left()
        elif command == "right":
            vac.right()
        elif command == "dock":
            vac.dock()
        elif command == "exit":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid command. Try again.")
else:
    print("Invalid choice. Please run again.")
