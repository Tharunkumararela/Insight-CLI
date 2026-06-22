import argparse
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

def analyze_data(filepath: str):
    try:
        with console.status("[bold green]Loading data..."):
            df = pd.read_csv(filepath)
        
        console.print(f"\n[bold blue]Dataset:[/] {filepath}")
        console.print(f"[bold blue]Total Rows:[/] {df.shape[0]:,}")
        console.print(f"[bold blue]Total Columns:[/] {df.shape[1]}\n")

        table = Table(title="Data Profile", show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("Column Name", style="cyan", min_width=15)
        table.add_column("Data Type", style="white")
        table.add_column("Missing %", justify="right", style="red")
        table.add_column("Unique Values", justify="right", style="green")
        table.add_column("Sample Data", style="yellow")

        for col in df.columns:
            dtype = str(df[col].dtype)
            missing_pct = round((df[col].isnull().sum() / len(df)) * 100, 1)
            unique_count = df[col].nunique()
            
            # Get a sample value safely
            sample_val = df[col].dropna().iloc[0] if not df[col].dropna().empty else "N/A"
            sample_str = str(sample_val)[:25] + "..." if len(str(sample_val)) > 25 else str(sample_val)

            table.add_row(col, dtype, f"{missing_pct}%", str(unique_count), sample_str)

        console.print(table)
        console.print("\n[bold green]✨ Analysis complete![/bold green]\n")

    except FileNotFoundError:
        console.print(f"\n[bold red]Error:[/] The file '{filepath}' was not found. Please check the path.\n")
    except Exception as e:
        console.print(f"\n[bold red]Error:[/] {str(e)}\n")

def main():
    parser = argparse.ArgumentParser(description="Instantly profile any CSV file directly in your terminal.")
    parser.add_argument("file", help="Path to the CSV file")
    args = parser.parse_args()

    analyze_data(args.file)

if __name__ == "__main__":
    main()
