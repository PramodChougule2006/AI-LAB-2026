room_a = ["Clean", "Dirty", "Obstacle", "Dirty"]
room_b = ["Dirty", "Obstacle", "Clean", "Dirty"]
rooms = {"A": room_a, "B": room_b}

current_room = "A"
grid_position = 0  
direction = 1  # 1 = Right, -1 = Left

def render_map():
    # Helper to generate a clean visual string of the grid
    a_str = "".join("🤖" if (current_room == "A" and i == grid_position) else ("🚧" if v == "Obstacle" else ("·" if v == "Clean" else "✨")) for i, v in enumerate(rooms["A"]))
    b_str = "".join("🤖" if (current_room == "B" and i == grid_position) else ("🚧" if v == "Obstacle" else ("·" if v == "Clean" else "✨")) for i, v in enumerate(rooms["B"]))
    return f"[{a_str}]-[{b_str}]"

print("🤖 Vacuum Active | Legend: 🤖 Robot | ✨ Dirt | 🚧 Obstacle | · Clean\n")
print(f"Step  Location  Direction  Action Log                        House Grid")
print(f"----  --------  ---------  --------------------------------  ----------")

step = 0
max_steps = 15 

while step < max_steps:
    step += 1
    current_grid = rooms[current_room]
    action = "Moving forward"

    # 1. Action: Clean if dirty
    if current_grid[grid_position] == "Dirty":
        current_grid[grid_position] = "Clean"
        action = "Cleaning room floor"

    # 2. Movement & Collision Logic
    next_pos = grid_position + direction

    if current_room == "A" and next_pos < 0:
        direction = 1
        action = "Hit outer wall ➔ Turning Right"
    elif current_room == "B" and next_pos >= len(rooms["B"]):
        direction = -1
        action = "Hit outer wall ➔ Turning Left"
    elif 0 <= next_pos < len(current_grid) and current_grid[next_pos] == "Obstacle":
        grid_position = next_pos + direction
        action = f"Hit obstacle at [{next_pos}] ➔ Hopping over"
    elif current_room == "A" and next_pos >= len(rooms["A"]):
        current_room = "B"
        grid_position = 0
        action = "Transitioning ➔ Entering Room B"
    elif current_room == "B" and next_pos < 0:
        current_room = "A"
        grid_position = len(rooms["A"]) - 1
        action = "Transitioning ➔ Entering Room A"
    else:
        grid_position = next_pos

    # Print elegantly padded columns
    dir_str = "Right ➡️" if direction == 1 else "Left ⬅️ "
    print(f"{step:02d}    Room {current_room}[{grid_position}]   {dir_str}   {action:<32}  {render_map()}")

    # 3. Goal check
    if "Dirty" not in rooms["A"] and "Dirty" not in rooms["B"]:
        print(f"\n🎉 Success! All accessible rooms are cleaned in {step} steps.")
        break
else:
    print("\n🛑 Safety Timeout: Maximum operating steps reached.")
