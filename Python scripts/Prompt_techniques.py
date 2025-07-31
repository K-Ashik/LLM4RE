import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# --- Configuration ---
INPUT_FILENAME = 'Prompt Engineering Techniques.csv'
OUTPUT_FILENAME_CSV = 'Prompt Engineering Techniques_categorized_final.csv'
OUTPUT_FILENAME_CHART = 'prompt_techniques_percentage_chart_final.png'
TECHNIQUE_COLUMN_NAME = 'The optimization and assessment strategies'

# --- List of all techniques and their keywords ---
TECHNIQUES_MAP = {
    'Chain of Thought (CoT)': ['chain of thought', 'chain-of-thought', 'cot'],
    'Tree of Thought (ToT)': ['tree of thought', 'tree-of-thought', 'tot'],
    'Retrieval Augmented Generation (RAG)': ['retrieval augmented generation', 'rag'],
    'Few-shot prompting': ['few-shot', 'few shot', 'one-shot', 'one shot'],
    'Zero-shot prompting': ['zero-shot', 'zero shot'],
    'Prompt templates and role-based prompts': ['prompt template', 'iterative prompting', 'comprehensive prompt', 'structured prompts', 'prompt chaining', 'role-based', 'persona'],
    # --- UPDATED AND EXPANDED KEYWORDS FOR THIS CATEGORY ---
    'Contextual cues and knowledge augmentation': [
        'context provided',
        'contextual cues',
        'knowledge augmentation',
        'expert knowledge',
        'similarity knowledge',
        'contextual information',
        'textual information',
        'dedicated schema',
        'domain-expert knowledge',
        'domain-specific',
        'providing context',
        'background information',
        'undersampling',
        'knowledge graph',
        'uml diagrams',
        'legal compliance',
        'glossary'
    ]
}

# --- Main Script Execution ---
try:
    # 1. Load your dataset
    df = pd.read_csv(INPUT_FILENAME)
    print(f"✅ Successfully loaded '{INPUT_FILENAME}'")
    
    total_papers = len(df.index)
    print(f"✅ Found {total_papers} total papers.")

    # 2. Find all techniques mentioned in each paper
    technique_counts = Counter()
    all_techniques_per_row = []

    for description in df[TECHNIQUE_COLUMN_NAME]:
        found_in_row = []
        if isinstance(description, str):
            desc_lower = description.lower()
            for tech_name, keywords in TECHNIQUES_MAP.items():
                if any(keyword in desc_lower for keyword in keywords):
                    found_in_row.append(tech_name)
        
        for tech in set(found_in_row):
            technique_counts[tech] += 1
            
        if not found_in_row:
            technique_counts['Others'] += 1
            all_techniques_per_row.append('Others')
        else:
            all_techniques_per_row.append(', '.join(found_in_row))
    
    df['Techniques Found'] = all_techniques_per_row
    df.to_csv(OUTPUT_FILENAME_CSV, index=False)
    print(f"✅ Detailed analysis saved to '{OUTPUT_FILENAME_CSV}'")

    # 3. Convert counts to percentages
    technique_percentages = {tech: (count / total_papers) * 100 for tech, count in technique_counts.items()}

    # 4. Prepare data for plotting
    plot_data = pd.DataFrame(technique_percentages.items(), columns=['Technique', 'Percentage of Papers'])
    plot_data = plot_data.sort_values('Percentage of Papers', ascending=False)
    print("\n📊 Data prepared for percentage chart:")
    print(plot_data)

    # 5. Create the percentage bar chart
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(14, 8))
    ax = sns.barplot(
        data=plot_data,
        x='Technique',
        y='Percentage of Papers',
        palette='viridis'
    )

    # 6. Customize and save the chart
    plt.title('Percentage of Papers Using Each Prompt Engineering Technique', fontsize=18)
    plt.xlabel('Prompt Engineering Technique', fontsize=12)
    plt.ylabel('Percentage of Papers (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}%'))

    for p in ax.patches:
        ax.annotate(
            f"{p.get_height():.1f}%",
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center', va='center',
            xytext=(0, 9),
            textcoords='offset points'
        )

    plt.tight_layout()
    plt.savefig(OUTPUT_FILENAME_CHART, dpi=300)
    print(f"\n✅ Percentage bar chart saved as '{OUTPUT_FILENAME_CHART}'")
    plt.show()

except FileNotFoundError:
    print(f"❌ Error: The file '{INPUT_FILENAME}' was not found.")
except KeyError:
    print(f"❌ Error: A column named '{TECHNIQUE_COLUMN_NAME}' was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")