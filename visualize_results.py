import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualization():
    # Experimental Data
    labels = ['Plaintext AI', 'FHE AI']
    accuracy = [96.00, 96.00]
    latency = [0.0077, 34.4390]
    
    # Set aesthetics
    sns.set_theme(style="whitegrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Accuracy Plot
    sns.barplot(x=labels, y=accuracy, ax=ax1, palette=["#3498db", "#2ecc71"])
    ax1.set_title('Detection Accuracy Comparison (Higher is better)', fontsize=14, pad=15)
    ax1.set_ylabel('Accuracy (%)', fontsize=12)
    ax1.set_ylim(0, 110)
    ax1.bar_label(ax1.containers[0], fmt='%.2f%%', padding=3, fontsize=12, fontweight='bold')
    
    # 2. Latency Plot (Log Scale or just threshold line)
    sns.barplot(x=labels, y=latency, ax=ax2, palette=["#e74c3c", "#f39c12"])
    ax2.set_title('Inference Latency per Sample (Lower is better)', fontsize=14, pad=15)
    ax2.set_ylabel('Latency (ms)', fontsize=12)
    ax2.set_yscale('log') # Log scale is better to show the massive difference but still show FHE is below 100ms
    
    # Add a red dashed line for the real-time threshold
    threshold = 100
    ax2.axhline(threshold, color='red', linestyle='--', linewidth=2, label='Real-time Threshold (100ms)')
    ax2.legend()
    
    # Add text labels manually because log scale makes bar_label tricky sometimes
    ax2.text(0, latency[0] * 1.5, f"{latency[0]:.4f} ms", ha='center', fontweight='bold', color='black')
    ax2.text(1, latency[1] * 1.2, f"{latency[1]:.2f} ms", ha='center', fontweight='bold', color='black')

    plt.suptitle("FHE vs Plaintext AI: Security & Real-time Feasibility for UGV", fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fhe_results_plot.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved successfully to: {output_path}")

if __name__ == "__main__":
    create_visualization()
