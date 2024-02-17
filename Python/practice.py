import pandas as pd
import time
import random

def corrupt_column(df, column_name):
    # Corrupt the specified column with random values
    df[column_name] = [random.uniform(0, 5) for _ in range(df.shape[0])]
    return df

def generate_pattern(length):
    # Generate a random pattern for demonstration purposes
    return [random.uniform(0, 1) for _ in range(length)]

def generate_pandas_table(num_rows, column_names):
    data = {column: generate_pattern(num_rows) for column in column_names}
    df = pd.DataFrame(data)
    return df

def save_to_file_and_print(table, filename):
    table.to_csv(filename, index=False)  # Change to .to_excel if you want to save as Excel
    print(f"Table saved to {filename}")

def print_pandas_table():
    num_rows = 5
    column_names = [f"Column{i + 1}" for i in range(3)]  # Adjust the number of columns as needed

    while True:
        table = generate_pandas_table(num_rows, column_names)
        print(table,end="\n\n")

        # Prompt the user to press a button to corrupt a column
        user_input = input("Press 'c' to corrupt a column, 'q' to quit, and any other key to continue : ")
        if user_input.lower() == 'c':
            column_to_corrupt = random.choice(column_names)
            table = corrupt_column(table, column_to_corrupt)
            print(f"Column '{column_to_corrupt}' corrupted!")

            print(table,end="\n\n")

        elif user_input.lower() == 'q':
            print("Exiting the loop. Goodbye!")
            break

        # Wait for 20 seconds before printing the next table
        save_to_file_and_print(table, "data.csv")
        time.sleep(5)

if __name__ == "__main__":
    print_pandas_table()
