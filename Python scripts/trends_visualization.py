import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuration ---
input_filename = 'trends_with_architecture.csv'
output_filename = 'grouped_bar_chart.png'
YEAR_COLUMN = 'Year'
ARCH_COLUMN = 'LLM architecture'
COUNT_COLUMN = 'count'

try:
    # --- 1. Load and Prepare Data ---
    df = pd.read_csv(input_filename)
    # Group data to get the counts
    plot_data = df.groupby([YEAR_COLUMN, ARCH_COLUMN]).size().reset_index(name=COUNT_COLUMN)
    print("📊 Data prepared for plotting:")
    print(plot_data)

    # --- 2. Create the Visualization ---
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(14, 8))

    # Create the grouped bar chart using seaborn's catplot for ease
    g = sns.catplot(
        data=plot_data,
        kind="bar",
        x=YEAR_COLUMN,
        y=COUNT_COLUMN,
        hue=ARCH_COLUMN,
        palette="viridis",
        height=6,
        aspect=2
    )

    # --- 3. Customize the Plot ---
    g.despine(left=True)
    g.set_axis_labels("Year", "Number of Papers")
    g.legend.set_title("Architecture")
    g.fig.suptitle('LLM Architecture Trends by Year', y=1.03, fontsize=16)

    # Add labels on top of each bar
    for ax in g.axes.flat:
        for p in ax.patches:
            ax.annotate(
                f"{p.get_height():.0f}",
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',
                xytext=(0, 9),
                textcoords='offset points'
            )

    # --- 4. Save the Plot ---
    plt.savefig(output_filename, dpi=300)
    print(f"\n✅ Grouped bar chart saved as '{output_filename}'")
    plt.show()

except Exception as e:
    print(f"An error occurred: {e}")