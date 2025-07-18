import pandas as pd

input_filename = 'Trends of LLM arch.csv'
output_filename = 'trends_with_architecture.csv'

try:
    df = pd.read_csv(input_filename)
    print(f"✅ Successfully loaded '{input_filename}'")

    # --- DEBUGGING STEP: Print the actual column names from your file ---
    print(f"Columns found in file: {df.columns.tolist()}")

    # --- UPDATE THIS LINE with the correct column name from the output above ---
    CATEGORY_COLUMN = 'Category of LLM' # <-- REPLACE THIS with the correct name

    # Check if the specified column exists
    if CATEGORY_COLUMN not in df.columns:
        raise KeyError # Triggers the error message below if name is still wrong

    # Define the architecture mapping
    def get_architecture(category):
        category_lower = str(category).lower().strip()
        if any(model in category_lower for model in ['t5', 'bart', 't0', 'transformer', 'encoder-decoder']):
            return 'Encoder-Decoder'
        elif any(model in category_lower for model in ['gpt', 'llama', 'palm', 'falcon', 'bloom', 'chatgpt', 'gpt-3', 'gpt-4','decoder', 'mistral','mixtral', 'gemini', 'claude','zephyr']):
            return 'Decoder-only'
        elif any(model in category_lower for model in ['bert', 'roberta', 'distilbert', 'albert', 'xlnet', 'electra', 'deberta', 'longformer', 'bertology']):
            return 'Encoder-only'
        else:
            return 'Encoder-only'  # Default case if no match is found

    # Create the new column
    df['LLM architecture'] = df[CATEGORY_COLUMN].apply(get_architecture)
    print("✅ New 'LLM architecture' column created successfully.")

    # Save the new file
    df.to_csv(output_filename, index=False)
    print(f"✅ Analysis complete! The new file has been saved as '{output_filename}'")

    # Display a preview of the result
    print("\n--- Preview of the new data ---")
    print(df[[CATEGORY_COLUMN, 'LLM architecture']].head(15))

except FileNotFoundError:
    print(f"❌ Error: The file '{input_filename}' was not found.")
except KeyError:
    print(f"❌ Error: The column '{CATEGORY_COLUMN}' was not found.")
    print("Please check the 'Columns found in file' list above and update the CATEGORY_COLUMN variable in the script with the correct name.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")