import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualize_dataset():
    print("Loading UGV combat data for visualization...")
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ugv_combat_data.csv')
    df = pd.read_csv(data_path)
    
    # Map labels to text for better legends
    df['Status'] = df['label'].map({0: 'Normal', 1: 'Cyber Attack'})
    
    # Set aesthetics
    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(18, 5))
    
    # 1. Speed Plot
    ax1 = plt.subplot(1, 3, 1)
    sns.scatterplot(data=df, x='timestamp', y='speed_kmh', hue='Status', 
                    palette={ 'Normal': '#3498db', 'Cyber Attack': '#e74c3c'}, 
                    alpha=0.6, s=20, ax=ax1)
    ax1.set_title('Speed Anomaly (Jamming)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Time (Samples)')
    ax1.set_ylabel('Speed (km/h)')
    
    # 2. Steering Plot
    ax2 = plt.subplot(1, 3, 2)
    sns.scatterplot(data=df, x='timestamp', y='steering_angle', hue='Status', 
                    palette={ 'Normal': '#3498db', 'Cyber Attack': '#e74c3c'}, 
                    alpha=0.6, s=20, ax=ax2)
    ax2.set_title('Steering Anomaly (Takeover)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Time (Samples)')
    ax2.set_ylabel('Steering Angle (Radians)')
    
    # 3. GPS Trajectory
    ax3 = plt.subplot(1, 3, 3)
    sns.scatterplot(data=df, x='gps_long', y='gps_lat', hue='Status', 
                    palette={ 'Normal': '#2ecc71', 'Cyber Attack': '#e74c3c'}, 
                    alpha=0.7, s=30, ax=ax3)
    ax3.set_title('GPS Trajectory (Spoofing)', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Longitude')
    ax3.set_ylabel('Latitude')
    
    plt.suptitle("UGV Telemetry Data Distribution: Normal vs Cyber Attacks", fontsize=16, fontweight='bold', y=1.05)
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_distribution_plot.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Dataset visualization saved successfully to: {output_path}")

if __name__ == "__main__":
    visualize_dataset()
