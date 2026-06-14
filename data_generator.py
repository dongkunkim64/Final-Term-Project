import pandas as pd
import numpy as np
import os

def generate_ugv_data(num_samples=5000, attack_ratio=0.1):
    """
    Generates mock UGV (Unmanned Ground Vehicle) telemetry data.
    Includes normal tactical driving and injected cyber attack anomalies.
    """
    np.random.seed(42)
    
    # 1. Generate Normal Data
    # Speed: convoy speed around 30-50 km/h
    speed = np.random.normal(loc=40.0, scale=5.0, size=num_samples)
    speed = np.clip(speed, 0, 80)
    
    # Steering: mostly straight with minor adjustments (-0.1 to 0.1 radians)
    steering = np.random.normal(loc=0.0, scale=0.05, size=num_samples)
    steering = np.clip(steering, -1.0, 1.0)
    
    # GPS: Simulating a slow progression in latitude/longitude
    gps_lat = 37.5 + np.cumsum(np.random.normal(loc=0.0001, scale=0.00001, size=num_samples))
    gps_long = 127.0 + np.cumsum(np.random.normal(loc=0.0001, scale=0.00001, size=num_samples))
    
    # Labels: 0 for Normal
    labels = np.zeros(num_samples, dtype=int)
    
    # 2. Inject Cyber Attacks (Anomalies)
    num_attacks = int(num_samples * attack_ratio)
    attack_indices = np.random.choice(num_samples, num_attacks, replace=False)
    
    for idx in attack_indices:
        attack_type = np.random.choice(['steering_takeover', 'gps_spoofing', 'speed_jamming'])
        
        if attack_type == 'steering_takeover':
            # Hacker maximizes steering to crash the UGV
            steering[idx] = np.random.choice([-1.0, 1.0])
        elif attack_type == 'gps_spoofing':
            # GPS signal jumps entirely to a wrong coordinate
            gps_lat[idx] += np.random.uniform(1.0, 5.0)
            gps_long[idx] += np.random.uniform(1.0, 5.0)
        elif attack_type == 'speed_jamming':
            # Sudden unrealistic speed jump
            speed[idx] += np.random.uniform(50, 100)
            
        labels[idx] = 1 # Mark as attack
        
    # 3. Create DataFrame
    df = pd.DataFrame({
        'timestamp': np.arange(num_samples),
        'speed_kmh': speed,
        'steering_angle': steering,
        'gps_lat': gps_lat,
        'gps_long': gps_long,
        'label': labels
    })
    
    return df

if __name__ == "__main__":
    print("Generating mock UGV combat data...")
    df = generate_ugv_data(num_samples=5000, attack_ratio=0.1)
    
    # Create directory if it doesn't exist
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, 'ugv_combat_data.csv')
    
    df.to_csv(output_path, index=False)
    
    print(f"Data generation complete! Saved to: {output_path}")
    print(f"Total samples: {len(df)}")
    print(f"Normal samples: {len(df[df['label'] == 0])}")
    print(f"Attack samples: {len(df[df['label'] == 1])}")
