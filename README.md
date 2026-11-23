# Bons e Maus Pagadores 💸

Solução para a competição Kaggle "Give me Some Credit". 

<br><br>
--- 

**Como configurar o ambiente**: Basta configurar o [uv](https://pypi.org/project/uv/) e rodar o comando abaixo.
```sh
uv sync
```

**Como importar os dados**: rodar no terminal o comando abaixo. Será pedido seu token-api de acesso ao Kaggle.
```sh
make download
```

**Como reproduzir a análise** (nesta ordem; o `modelo` leva ~5 min por causa da Random Forest)
```sh
make eda        # reexecuta notebooks/01_eda.ipynb
make modelo     # reexecuta notebooks/02_modelagem.ipynb, gera figuras e submissão
make relatorio  # compila o artigo e monta os slides
```

**Como submeter as soluções** (requer o token em `~/.kaggle/kaggle.json`, criado em kaggle.com → Settings → API → Create New Token)
```sh
make submit MSG="Random forest"   # envia submissions/submission_rf.csv
make submissoes                   # lista as submissões e os scores
```

**Estrutura**
- `notebooks/01_eda.ipynb`: análise exploratória, sujeiras e decisões de limpeza
- `notebooks/02_modelagem.ipynb`: regressão logística × Random Forest, validação cruzada, avaliação no teste e figuras do artigo
- `src/bons_maus_pagadores/preprocessamento.py`: regras de limpeza usadas pelos dois notebooks
- `docs/paper/`: artigo do projeto final de ML (UFABC), em LaTeX (`build.ps1` compila)
- `docs/apresentacao/`: slides da lightning talk (`slides.html` para apresentar, `slides.pdf`)

---
<br><br>

> [!IMPORTANT]
> Sobre o uso de GenAI. Entendo ser uma ferramenta imprencindível para a produtividade e até para o estudo pessoal mesmo, porém a intenção desse repositório é trabalhar minhas habilidades com modelagem, explorando cada uma das dificuldades e aprendendo com elas. Por isso, ressalto que a análise exploratória (`01_eda.ipynb`, até setembro de 2026) foi escrita por mim, sem GenAI. Na reta final do projeto da disciplina (novembro de 2026), usei o Sol para o template do artigo e o Claude Opus 5.5 para revisar o notebook de EDA, escrever o notebook de modelagem e o módulo de pré-processamento, e rascunhar o artigo e os slides, como declarado na seção *Declaration of AI use* do artigo.

---

Solução para a competição Kaggle "Give me Some Credit", disponível em https://www.kaggle.com/competitions/GiveMeSomeCredit.