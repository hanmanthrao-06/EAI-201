import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from queue import PriorityQueue
import numpy as np

# Updated campus graph based on actual Chanakya University map
campus_graph = {
    "Sports Area": [("Food Court", 150), ("Hostel Block", 400)],
    "Food Court": [("Sports Area", 150), ("Academic Block 2 (B)", 120), ("Canteen", 180)],
    "Academic Block 2 (B)": [("Food Court", 120), ("Academic Block 1", 200), ("Library", 150)],
    "Hostel Block": [("Sports Area", 400), ("Academic Block 1", 200), ("Library", 250)],
    "Academic Block 1": [("Academic Block 2 (B)", 200), ("Hostel Block", 200), ("Library", 100), ("Admin Block", 120)],
    "Library": [("Academic Block 2 (B)", 150), ("Academic Block 1", 100), ("Hostel Block", 250), ("Admin Block", 80), ("Canteen", 150)],
    "Admin Block": [("Academic Block 1", 120), ("Library", 80), ("Canteen", 100), ("Medical Centre", 120), ("Second Gate", 150)],
    "Canteen": [("Food Court", 180), ("Library", 150), ("Admin Block", 100), ("Medical Centre", 90)],
    "Medical Centre": [("Canteen", 90), ("Admin Block", 120), ("Auditorium", 100)],
    "Auditorium": [("Medical Centre", 100), ("Second Gate", 180)],
    "Second Gate": [("Admin Block", 150), ("Auditorium", 180), ("Main Gate", 60)],
    "Main Gate": [("Second Gate", 60)],
}

# Real campus coordinates based on your map analysis
campus_coordinates = {
    "Sports Area": (-300, 200),
    "Food Court": (-200, 100),
    "Academic Block 2 (B)": (-100, 50),
    "Hostel Block": (250, 150),
    "Academic Block 1": (150, 0),
    "Library": (100, -50),
    "Admin Block": (50, -80),
    "Canteen": (-50, -30),
    "Medical Centre": (-120, -80),
    "Auditorium": (-200, -150),
    "Second Gate": (0, -200),
    "Main Gate": (0, -250),
}

# Building timings
building_timings = {
    "Library": "8:30 AM – 9:00 PM",
    "Canteen": "8:00 AM – 4:45 PM",
    "Medical Centre": "24/7",
    "Sports Area": "6:00 AM – 7:30 PM",
    "Admin Block": "9:00 AM – 5:00 PM",
    "Auditorium": "10:00 AM – 5:00 PM",
    "Academic Block 1": "7:00 AM – 8:00 PM",
    "Academic Block 2 (B)": "7:00 AM – 8:00 PM",
    "Food Court": "8:00 AM – 9:00 PM",
    "Hostel Block": "24/7 (Residents only)",
}

# Staff Directory
staff_directory = [
    {"Name": "Prof. Yashavantha Dongre", "Profession": "Vice-Chancellor", "Contact": "08031233107"},
    {"Name": "Prof. H.S. Subramanya", "Profession": "Pro Vice-Chancellor, Prof. & Dean (Biosciences & Math)", "Contact": "08031233107"},
    {"Name": "Prof. Sushant T. Joshi", "Profession": "Registrar & Professor of Management", "Contact": "08031233107"},
    {"Name": "Prof. Sandeep Nair", "Profession": "Prof. & Dean (Arts, Humanities & Social Sciences)", "Contact": "08031233107"},
    {"Name": "Prof. Shrinivas S. Balli", "Profession": "Dean, Student Affairs", "Contact": "08031233107"},
    {"Name": "Prof. Vineeth Paleri", "Profession": "Professor & Director Academics (Engineering)", "Contact": "08031233107"},
    {"Name": "Prof. H. S. Ashok", "Profession": "Professor of Psychology", "Contact": "08031233107"},
    {"Name": "Prof. Chetan Basavaraj", "Profession": "Prof. & Dean (Law, Governance, and Public Policy)", "Contact": "08031233107"},
    {"Name": "Prof. Ashwin Kumar A. P.", "Profession": "Dean, Academics", "Contact": "08031233107"},
    {"Name": "Prof. Anilkumar G. Garag", "Profession": "Professor of Management", "Contact": "08031233107"},
    {"Name": "Prof. Bhavani M. R.", "Profession": "Registrar Evaluation and Professor", "Contact": "08031233107"},
    {"Name": "Dr. Priyadarshan Kinatukara", "Profession": "Assistant Professor, Biosciences", "Contact": "08031233107"},
    {"Name": "Dr. Shubhada Hegde", "Profession": "Associate Professor, Biosciences", "Contact": "08031233107"},
    {"Name": "Dr. Sumi S.", "Profession": "Associate Professor, Biosciences", "Contact": "08031233107"},
    {"Name": "Dr. Sanjukta Mukherjee", "Profession": "Associate Professor, Biosciences", "Contact": "08031233107"},
    {"Name": "Dr. Meenakshi Iyer", "Profession": "Assistant Professor, Biosciences", "Contact": "08031233107"},
    {"Name": "Dr. Deepthi Hebbale", "Profession": "Assistant Professor, Biosciences", "Contact": "08031233107"},
]

def create_real_campus_map(path=None, start_node=None, end_node=None, save_path="chanakya_campus_navigation.png"):
    """
    Creates visual campus map based on actual Chanakya University layout
    """
    fig, ax = plt.subplots(1, 1, figsize=(18, 14))
    
    # Set up the plot to match actual campus
    ax.set_xlim(-400, 400)
    ax.set_ylim(-300, 300)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2, linestyle='--')
    ax.set_title('🎓 Chanakya University Campus Navigator - Live Map', 
                fontsize=20, fontweight='bold', pad=30)
    
    # Add campus background
    campus_oval = patches.Ellipse((0, -50), 600, 400, linewidth=3, 
                                 edgecolor='#2E8B57', facecolor='#F0FFF0', alpha=0.3)
    ax.add_patch(campus_oval)
    
    # Draw all pathways
    for location, connections in campus_graph.items():
        if location in campus_coordinates:
            x1, y1 = campus_coordinates[location]
            for connected_location, distance in connections:
                if connected_location in campus_coordinates:
                    x2, y2 = campus_coordinates[connected_location]
                    ax.plot([x1, x2], [y1, y2], '#8FBC8F', linewidth=3, alpha=0.7, zorder=2)
                    
                    # Distance labels
                    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                    ax.text(mid_x, mid_y, f'{distance}m', fontsize=8, 
                           bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8),
                           ha='center', va='center', zorder=3)
    
    # Highlight navigation path
    if path and len(path) > 1:
        total_distance = 0
        for i in range(len(path) - 1):
            if path[i] in campus_coordinates and path[i+1] in campus_coordinates:
                x1, y1 = campus_coordinates[path[i]]
                x2, y2 = campus_coordinates[path[i+1]]
                
                # Find distance
                for connected_location, distance in campus_graph.get(path[i], []):
                    if connected_location == path[i+1]:
                        total_distance += distance
                        break
                
                # Draw highlighted path
                ax.plot([x1, x2], [y1, y2], '#FF4500', linewidth=8, alpha=0.8, zorder=5)
                ax.plot([x1, x2], [y1, y2], '#FFD700', linewidth=4, alpha=0.9, zorder=6)
                
                # Direction arrows
                dx, dy = x2 - x1, y2 - y1
                length = np.sqrt(dx**2 + dy**2)
                if length > 0:
                    ax.annotate('', xy=(x2 - 0.1*dx, y2 - 0.1*dy), xytext=(x1 + 0.1*dx, y1 + 0.1*dy),
                               arrowprops=dict(arrowstyle='->', color='#FF4500', lw=4), zorder=7)
        
        # Path info box
        walking_time = total_distance / 1.25 / 60
        path_info = f"🎯 ROUTE NAVIGATION\n"
        path_info += f"━━━━━━━━━━━━━━━━━━━━\n"
        path_info += f"🚶 Path: {' → '.join(path)}\n"
        path_info += f"📏 Distance: {total_distance}m\n"
        path_info += f"⏱️ Time: {walking_time:.1f} min\n"
        path_info += f"🎓 Chanakya University"
        
        ax.text(0.02, 0.98, path_info, transform=ax.transAxes, fontsize=11,
               verticalalignment='top', fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='#E6F3FF', 
                        edgecolor='#4169E1', alpha=0.95), zorder=10)
    
    # Draw building nodes with emojis
    for location, (x, y) in campus_coordinates.items():
        # Node styling
        if location == start_node:
            color, size, marker, symbol = '#32CD32', 400, '^', '🚩'
        elif location == end_node:
            color, size, marker, symbol = '#FF4500', 400, 's', '🎯'
        elif path and location in path:
            color, size, marker, symbol = '#FFD700', 300, 'o', '📍'
        else:
            # Building-specific colors and emojis
            building_styles = {
                'Academic': ('#4169E1', '📚'),
                'Library': ('#8B4513', '📖'),
                'Hostel': ('#9370DB', '🏠'),
                'Food': ('#FF6347', '🍽️'),
                'Sports': ('#00CED1', '⚽'),
                'Medical': ('#FF69B4', '🏥'),
                'Admin': ('#2F4F4F', '🏢'),
            }
            
            color, symbol = '#17a2b8', '🏛️'  # Default
            for key, (col, sym) in building_styles.items():
                if key in location or key.lower() in location.lower():
                    color, symbol = col, sym
                    break
            
            size, marker = 250, 'o'
        
        # Draw with shadow
        ax.scatter(x+3, y-3, c='gray', s=size, marker=marker, alpha=0.3, zorder=3)
        ax.scatter(x, y, c=color, s=size, marker=marker, 
                  edgecolors='white', linewidth=3, alpha=0.9, zorder=8)
        
        # Labels with emojis
        label_text = f"{symbol} {location}"
        bbox_props = dict(boxstyle='round,pad=0.4', facecolor='white', 
                         edgecolor=color, linewidth=2, alpha=0.95)
        ax.annotate(label_text, (x, y), xytext=(10, 10), textcoords='offset points',
                   fontsize=10, fontweight='bold', color=color,
                   bbox=bbox_props, zorder=9)
    
    # Legend
    legend_elements = [
        plt.Line2D([0], [0], color='#8FBC8F', linewidth=3, label='🛤️ Campus Paths'),
        plt.Line2D([0], [0], color='#FF4500', linewidth=6, label='🗺️ Your Route'),
        plt.scatter([], [], c='#32CD32', s=150, marker='^', label='🚩 Start'),
        plt.scatter([], [], c='#FF4500', s=150, marker='s', label='🎯 Destination'),
        plt.scatter([], [], c='#FFD700', s=150, marker='o', label='📍 Route Points'),
        plt.scatter([], [], c='#4169E1', s=150, marker='o', label='🏢 Buildings')
    ]
    
    ax.legend(handles=legend_elements, loc='lower right', 
             bbox_to_anchor=(0.98, 0.02), fontsize=11,
             framealpha=0.95, shadow=True, fancybox=True)
    
    # Campus info
    campus_info = "🎓 CHANAKYA UNIVERSITY\n📍 Bengaluru, Karnataka\n🤖 BotBrain Navigator"
    ax.text(0.98, 0.98, campus_info, transform=ax.transAxes, 
           ha='right', va='top', fontsize=10, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0F8FF', alpha=0.9))
    
    # Compass
    ax.text(0.05, 0.95, '🧭', transform=ax.transAxes, fontsize=25, ha='center')
    ax.text(0.05, 0.90, 'N', transform=ax.transAxes, fontsize=14, ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"🗺️ Campus navigation map saved: {save_path}")
    plt.show()
    return save_path

def show_staff_directory():
    print("\n" + "="*110)
    print("👥 CHANAKYA UNIVERSITY STAFF DIRECTORY")
    print("="*110)
    print(f"{'Name':<32} | {'Profession':<55} | {'Contact':<12}")
    print("-" * 110)
    for staff in staff_directory:
        print(f"{staff['Name']:<32} | {staff['Profession']:<55} | {staff['Contact']:<12}")
    print("="*110)

# Heuristic function
def euclidean_heuristic(node1, node2):
    x1, y1 = campus_coordinates[node1]
    x2, y2 = campus_coordinates[node2]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# A* Search algorithm
def a_star(start, goal):
    visited = set()
    pq = PriorityQueue()
    pq.put((euclidean_heuristic(start, goal), 0, start, [start]))
    explored_nodes = []
    
    while not pq.empty():
        f_score, cost, current, path = pq.get()
        explored_nodes.append(current)
        
        if current == goal:
            return path, cost, explored_nodes
            
        if current not in visited:
            visited.add(current)
            for neighbor, weight in campus_graph.get(current, []):
                if neighbor not in visited:
                    g = cost + weight
                    h = euclidean_heuristic(neighbor, goal)
                    pq.put((g + h, g, neighbor, path + [neighbor]))
                    
    return None, math.inf, explored_nodes

# Enhanced navigation display
def display_result(start, goal):
    path, dist, explored = a_star(start, goal)
    if path is None:
        return f"❌ No path found from {start} to {goal}."
    
    walking_time = dist / 1.25 / 60  # minutes
    
    print(f"\n🗺️ Generating real-time campus navigation map...")
    map_file = create_real_campus_map(path=path, start_node=start, end_node=goal)
    
    result = f"\n🎯 CHANAKYA UNIVERSITY NAVIGATION\n"
    result += "="*60 + "\n"
    result += f"🚩 Starting Point: {start}\n"
    result += f"🎯 Destination: {goal}\n"
    result += f"🛤️ Optimal Route: {' → '.join(path)}\n"
    result += f"📏 Total Distance: {dist} meters\n"
    result += f"🚶 Walking Time: {walking_time:.2f} minutes\n"
    
    if goal in building_timings:
        result += f"🕒 {goal} Hours: {building_timings[goal]}\n"
    
    result += f"🔍 Locations Explored: {len(explored)}\n"
    result += f"📸 Navigation Map: {map_file}\n"
    result += "="*60
    
    return result

def show_locations():
    print("\n🏢 CHANAKYA UNIVERSITY CAMPUS LOCATIONS")
    print("="*70)
    for i, location in enumerate(campus_graph.keys(), 1):
        timing = building_timings.get(location, "Always accessible")
        print(f"{i:2d}. {location:<25} | {timing}")
    print("="*70)
    return list(campus_graph.keys())

def main():
    print("🎓" + "="*80)
    print("    🤖 BotBrain - Chanakya University Campus Navigator")
    print("         🗺️ Real Campus Map Integration System")
    print("="*83)
    
    while True:
        print("\n📋 NAVIGATION MENU")
        print("-" * 40)
        print("1. 🗺️ Campus Navigation with Live Map")
        print("2. 👥 University Staff Directory")
        print("3. 🏢 View All Campus Locations")
        print("4. 🕒 Building Operating Hours")
        print("0. 🚪 Exit Navigator")
        print("-" * 40)
        
        choice = input("🎯 Select option: ")

        if choice == "0":
            print("\n🎓 Thank you for using BotBrain Campus Navigator!")
            print("📍 Navigate Chanakya University with confidence!")
            break
        elif choice == "1":
            locations = show_locations()
            try:
                print(f"\n📍 Select from {len(locations)} campus locations:")
                print("-" * 50)
                start_index = int(input("🚩 Enter starting location number: "))
                goal_index = int(input("🎯 Enter destination number: "))
                
                if 1 <= start_index <= len(locations) and 1 <= goal_index <= len(locations):
                    start = locations[start_index - 1]
                    goal = locations[goal_index - 1]
                    print(display_result(start, goal))
                else:
                    print("❌ Invalid location numbers. Please try again.")
            except ValueError:
                print("❌ Please enter valid numbers only.")
                
        elif choice == "2":
            show_staff_directory()
        elif choice == "3":
            show_locations()
        elif choice == "4":
            print("\n🕒 CAMPUS BUILDING HOURS")
            print("="*60)
            for building, hours in building_timings.items():
                print(f"🏢 {building:<25} | {hours}")
            print("="*60)
        else:
            print("❌ Invalid option. Please select 0-4.")
        
        print("\n" + "="*80)

if __name__ == "__main__":
    main()
