import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

def create_animation():
    print("Loading UGV combat data for animation...")
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ugv_combat_data.csv')
    df = pd.read_csv(data_path)
    
    # Select an interesting slice of data (e.g., 200 frames containing both normal and attack)
    # Let's find an index where an attack happens to center our animation around it
    attack_indices = df.index[df['label'] == 1].tolist()
    if not attack_indices:
        print("No attacks found!")
        return
        
    start_idx = max(0, attack_indices[0] - 50)
    end_idx = min(len(df), start_idx + 150)
    
    df_slice = df.iloc[start_idx:end_idx].reset_index(drop=True)
    
    fig = plt.figure(figsize=(10, 6))
    fig.suptitle("UGV Real-time Cyber Attack Detection Simulator", fontsize=14, fontweight='bold')
    
    # Setup subplots
    ax_gps = plt.subplot2grid((2, 2), (0, 0), rowspan=2)
    ax_speed = plt.subplot2grid((2, 2), (0, 1))
    ax_steer = plt.subplot2grid((2, 2), (1, 1))
    
    # GPS Plot
    ax_gps.set_xlim(df_slice['gps_long'].min() - 0.001, df_slice['gps_long'].max() + 0.001)
    ax_gps.set_ylim(df_slice['gps_lat'].min() - 0.001, df_slice['gps_lat'].max() + 0.001)
    ax_gps.set_title("GPS Trajectory")
    ax_gps.set_xlabel("Longitude")
    ax_gps.set_ylabel("Latitude")
    gps_line, = ax_gps.plot([], [], 'o-', color='green', markersize=4, alpha=0.5)
    ugv_dot, = ax_gps.plot([], [], 'o', color='blue', markersize=10)
    status_text = ax_gps.text(0.05, 0.95, '', transform=ax_gps.transAxes, fontsize=12, fontweight='bold', verticalalignment='top')
    
    # Speed Plot
    ax_speed.set_xlim(0, 150)
    ax_speed.set_ylim(-0.5, 0.5)
    ax_speed.set_title("Speed (km/h)")
    ax_speed.set_yticks([])
    speed_bar = ax_speed.barh([0], [0], color='blue', height=0.5)
    
    # Steering Plot
    ax_steer.set_xlim(-1.5, 1.5)
    ax_steer.set_ylim(-0.5, 0.5)
    ax_steer.set_title("Steering Angle (Rad)")
    ax_steer.set_yticks([])
    ax_steer.axvline(0, color='black', linestyle='--')
    steer_bar = ax_steer.barh([0], [0], color='blue', height=0.5)
    
    plt.tight_layout()

    def update(frame):
        # Update GPS
        current_data = df_slice.iloc[:frame+1]
        gps_line.set_data(current_data['gps_long'], current_data['gps_lat'])
        ugv_dot.set_data([df_slice.iloc[frame]['gps_long']], [df_slice.iloc[frame]['gps_lat']])
        
        # Check status
        is_attack = df_slice.iloc[frame]['label'] == 1
        
        if is_attack:
            status_text.set_text("⚠️ WARNING: CYBER ATTACK DETECTED!")
            status_text.set_color('red')
            ugv_dot.set_color('red')
            speed_bar[0].set_color('red')
            steer_bar[0].set_color('red')
        else:
            status_text.set_text("✅ STATUS: NORMAL")
            status_text.set_color('green')
            ugv_dot.set_color('blue')
            speed_bar[0].set_color('blue')
            steer_bar[0].set_color('blue')
            
        # Update Speed
        speed = df_slice.iloc[frame]['speed_kmh']
        speed_bar[0].set_width(speed)
        
        # Update Steering
        steer = df_slice.iloc[frame]['steering_angle']
        steer_bar[0].set_width(steer)
        
        return gps_line, ugv_dot, status_text, speed_bar[0], steer_bar[0]

    print("Generating GIF animation (this may take a minute)...")
    ani = animation.FuncAnimation(fig, update, frames=len(df_slice), interval=100, blit=False)
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ugv_simulation.gif')
    # Save as GIF using pillow writer (no ffmpeg required)
    ani.save(output_path, writer='pillow', fps=10)
    print(f"Animation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_animation()
