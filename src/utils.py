from pathlib import Path
import pandas as pd

def save_df(df: pd.DataFrame, name: str, folder: Path, fmt="parquet"):
    folder.mkdir(parents=True, exist_ok=True)
    base = folder / name
    
    # save parquet
    df.to_parquet(base.with_suffix(".parquet"), index=False)
    # save csv
    df.to_csv(base.with_suffix(".csv"), index=False)
    

def load_df(name: str, folder: Path, fmt="parquet") -> pd.DataFrame:
    path = folder / f"{name}.{fmt}"
    return pd.read_csv(path) if fmt=="csv" else pd.read_parquet(path)
