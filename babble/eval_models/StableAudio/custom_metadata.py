import pandas as pd


def get_prompt(file_path: str) -> str:
    dataset_path: str
    filename: str
    dataset_path, filename = file_path.split("/[")
    dataset_path = dataset_path.replace("audio", "metadata")
    file_dataset_id: str = filename.split("]")[0]
    
    df: pd.DataFrame = pd.read_csv(f"{dataset_path}/musiccaps-public.csv")
    caption_value = df.loc[df['ytid'] == file_dataset_id, 'caption']
    return caption_value.iloc[0]


def get_custom_metadata(info, audio):
    prompt: str = get_prompt(info["path"])
    return {"prompt": prompt}