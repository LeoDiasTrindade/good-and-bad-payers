.PHONY: download eda modelo relatorio artigo slides submit submissoes hello

# Baixa os dados da competição para data/raw (pede o token da API do Kaggle)
download:
	uv run src/bons_maus_pagadores/download_data.py

# Reexecuta a análise exploratória de cima a baixo
eda:
	uv run jupyter nbconvert --to notebook --execute --inplace notebooks/01_eda.ipynb

# Treina e avalia os modelos (~5 min); gera as figuras do artigo e submissions/submission_rf.csv
modelo:
	uv run jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1800 notebooks/02_modelagem.ipynb

# Compila o artigo (docs/paper/main.pdf)
artigo:
	powershell -NoProfile -ExecutionPolicy Bypass -File ./docs/paper/build.ps1

# Monta docs/apresentacao/slides.html a partir de docs/apresentacao/deck (PDF: abrir e imprimir pelo navegador)
slides:
	uv run python docs/apresentacao/build_html.py docs/apresentacao/deck/project docs/apresentacao/slides.html

# Artigo + slides
relatorio: artigo slides

# Submete no Kaggle (requer ~/.kaggle/kaggle.json). Uso: make submit MSG="minha mensagem"
MSG ?= Random forest (min_samples_leaf=20)
SUBMISSAO ?= submissions/submission_rf.csv
submit:
	uv run --with kaggle kaggle competitions submit -c GiveMeSomeCredit -f $(SUBMISSAO) -m "$(MSG)"

# Lista as submissões e os scores (public/private)
submissoes:
	uv run --with kaggle kaggle competitions submissions -c GiveMeSomeCredit

hello:
	echo "Hello"
