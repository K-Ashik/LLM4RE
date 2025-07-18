import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuration ---
input_filename = 'LLM related RE dataset.csv'
output_filename = 'data_handling_trends_final.png'
processed_data_filename = 'processed_dataset_final.csv'

# --- 1. Tailored Data Categorization Function (Updated Logic) ---

def categorize_dataset(technique):
    """
    Categorizes every dataset into one of the four main labels,
    using educated defaults for ambiguous cases.
    """
    if not isinstance(technique, str):
        # Default for blank entries
        return 'Collected dataset'
    
    technique_lower = technique.lower()

    # --- Priority 1: Explicit Categories based on specific keywords ---
    if 'industrial' in technique_lower:
        return 'Industrial Dataset'
    if any(k in technique_lower for k in ['interview', 'generating interview scripts', 'manually annotating', 'manually annotated', 'curated a corpus', 'compiling a custom dataset', 'generating a dataset', 'custom dataset', 'manually created']):
        return 'Constructed Dataset'
    if any(k in technique_lower for k in ['existing datasets', 'publicly available', 'pure dataset', 'benchmark', 'crowd-re', 'rico dataset', 'nlp4re']):
        return 'Open source-data'
    if any(k in technique_lower for k in ['collected from', 'collecting user stories', 'collected a large-scale dataset', 'extracted from sources', 'gathering publicly available', 'github', 'stack overflow', 'app reviews']):
        return 'Collected dataset'
    
    # --- Priority 2: Educated Defaulting for Ambiguous Cases ---
    if 'not mentioned' in technique_lower or 'do not contain specific information' in technique_lower:
        return 'Collected dataset'
    if any(k in technique_lower for k in ['feature engineering', 'tuning', 'normalization', 'cleaning', 'tokenization', 'fine-tuning']):
        return 'Open source-data'

    # Final fallback default for any remaining cases
    return 'Collected dataset'

try:
    df = pd.read_csv(input_filename)
    print("✅ Successfully loaded the dataset.")

    df['Dataset Category'] = df['The adopted data handling techniques'].apply(categorize_dataset)
    print("✅ Data categorization complete. All items are now categorized.")
    
    df.to_csv(processed_data_filename, index=False)
    print(f"✅ Processed data saved to '{processed_data_filename}' for your review.")

    # --- 2. Create the Visualization ---

    plot_data = df.groupby(['Year', 'Dataset Category']).size().reset_index(name='count')

    print("\n📊 Data prepared for plotting:")
    print(plot_data)

    sns.set_theme(style="whitegrid")
    g = sns.catplot(
        data=plot_data,
        kind="bar", x="Year", y="count", hue="Dataset Category",
        palette="plasma", height=7, aspect=1.8,
        hue_order=['Open source-data', 'Collected dataset', 'Constructed Dataset', 'Industrial Dataset']
    )

    g.despine(left=True)
    g.set_axis_labels("Year", "Number of Papers")
    g.legend.set_title("Dataset Type")
    g.fig.suptitle('Trends of Data Handling Techniques in RE Papers', y=1.03, fontsize=18)

    for ax in g.axes.flat:
        for p in ax.patches:
            if p.get_height() > 0:
                ax.annotate(f"{p.get_height():.0f}",
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', xytext=(0, 9),
                            textcoords='offset points', fontsize=10)

    plt.savefig(output_filename, dpi=300)
    print(f"\n✅ Chart saved as '{output_filename}'")
    plt.show()

except FileNotFoundError:
    print(f"❌ Error: The file '{input_filename}' was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")