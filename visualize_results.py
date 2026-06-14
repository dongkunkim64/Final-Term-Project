import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import pandas as pd

def create_visualization():
    # Load JSON results
    data_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(data_dir, 'fhe_results.json')
    
    if not os.path.exists(json_path):
        print(f"[오류] {json_path} 파일이 존재하지 않습니다. fhe_experiment.py를 먼저 실행해 주세요.")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        results = json.load(f)
        
    # Prepare data for plotting
    plot_data = []
    for model_name, metrics in results.items():
        # Plaintext record
        plot_data.append({
            "Model": model_name,
            "Mode": "Plaintext",
            "Accuracy (%)": metrics["plain_accuracy"],
            "Latency (ms)": metrics["plain_latency_ms"]
        })
        # FHE record
        plot_data.append({
            "Model": model_name,
            "Mode": "FHE (Encrypted)",
            "Accuracy (%)": metrics["fhe_accuracy"],
            "Latency (ms)": metrics["fhe_latency_ms"]
        })
        
    df_plot = pd.DataFrame(plot_data)
    
    # Set aesthetics
    sns.set_theme(style="whitegrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 1. Accuracy Plot
    sns.barplot(data=df_plot, x="Model", y="Accuracy (%)", hue="Mode", ax=ax1, palette=["#3498db", "#2ecc71"])
    ax1.set_title('Detection Accuracy Comparison (Higher is better)', fontsize=14, pad=15)
    ax1.set_ylabel('Accuracy (%)', fontsize=12)
    ax1.set_ylim(0, 115)
    
    # Add labels on bars
    for container in ax1.containers:
        ax1.bar_label(container, fmt='%.2f%%', padding=3, fontsize=11, fontweight='bold')
        
    # 2. Latency Plot (Log Scale)
    sns.barplot(data=df_plot, x="Model", y="Latency (ms)", hue="Mode", ax=ax2, palette=["#e74c3c", "#f39c12"])
    ax2.set_title('Inference Latency per Sample (Lower is better)', fontsize=14, pad=15)
    ax2.set_ylabel('Latency (ms) - Log Scale', fontsize=12)
    ax2.set_yscale('log')
    
    # Add a red dashed line for the real-time threshold
    threshold = 100
    ax2.axhline(threshold, color='red', linestyle='--', linewidth=2, label='Real-time Threshold (100ms)')
    ax2.legend()
    
    # Add text labels manually for latency
    for container in ax2.containers:
        # Use scientific or standard float labels
        ax2.bar_label(container, fmt='%.4f ms', padding=3, fontsize=10, fontweight='bold')

    plt.suptitle("FHE vs Plaintext AI: Security & Real-time Feasibility for UGV", fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(data_dir, 'fhe_results_plot.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved successfully to: {output_path}")

if __name__ == "__main__":
    create_visualization()
