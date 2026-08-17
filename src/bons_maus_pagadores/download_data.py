import os
import shutil
from pathlib import Path
import kagglehub; kagglehub.login()

def download_data():
    dest_path = (Path(__file__).resolve().parent.parent.parent / "data" / "raw")
    os.makedirs(dest_path, exist_ok=True)
    
    if os.path.exists(os.path.join(dest_path, "cs-test.csv")):
        print("Dados já estão em data/raw/")
        return
    
    print("Baixando dados do Kaggle...")
    cache_path = kagglehub.competition_download('GiveMeSomeCredit')
    
    # Copia do cache para o repositório
    for file_name in os.listdir(cache_path):
        print(file_name)
        shutil.copy(os.path.join(cache_path, file_name), dest_path)
    print("Download concluído")

if __name__ == "__main__":
    download_data()