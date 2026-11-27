# Lightning talk: Give Me Some Credit (5 min)

Lista de pontos para falar em cada slide, na ordem. Os pontos em **inglês** são o que você diz; as notas em português são para você.

- O tempo ao lado de cada slide é a meta **acumulada**.
- Pontos marcados com _[corte]_ podem ser pulados se estiver atrasado.
- **Negrito** = palavra para enfatizar.

|Slide|Tema|Até|
|---|---|---|
|1|Cover|0:20|
|2|Give Me Some Credit|0:55|
|3|Late payments|1:25|
|4|Six data traps|2:00|
|5|Method|2:35|
|6|Regularization|3:05|
|7|Deep trees|3:30|
|8|Results|4:10|
|9|Risk drivers|4:35|
|10|Looking back|5:00|

---

## 1 · Cover (até 0:20)

**Falar**

- Hi, I'm Leonardo.
- The question every lender asks before granting credit: what is the **probability** that this person will be **90 days or more past due** in the next two years?
- Roadmap: what I chose, what the data was hiding, what I tried, what I found, what I would do differently.

> ⚠️ **Nome da base:** _Give Me Some Credit_ (não "who wants some credit"). ⚠️ **É probabilidade, não sim/não.** O projeto avalia ranking de risco (AUC) e log-loss, não uma classificação. 💡 A história do projeto antigo é opcional: no máximo uma frase. Comparar os dois modelos é conteúdo do slide 5, não deste.

---

## 2 · Give Me Some Credit (até 0:55)

**Falar**

- Kaggle competition from 2011: **150 thousand** past borrowers, **ten features**.
- Features: late payments, revolving credit use, debt ratio, income, age.
- The **bad rate is 6.7 percent**, about 7 in every 100.
- So accuracy is useless: calling everyone a good payer is already **93 percent** accurate.
- I judge models by **AUC** (how well they rank risk) and **log-loss**.
- My question: **how much ranking power does an explainable model give up?**

> 💡 Ordem para decorar: **base → desbalanceamento → métrica → pergunta**.

---

## 3 · Late payments raise default risk over tenfold (até 1:25)

**Falar**

- Past late payments are the strongest signal: bad rate goes from **4 percent** (none) to **over 40 percent** (four or more), more than tenfold.
- Heavy revolving credit use raises the risk sharply in the top deciles.
- Older clients default less.
- _[corte]_ Panel (d): the two flags I created.

**Painel (d): o que são as flags**

|Barra|Significado|Taxa|
|---|---|---|
|Has income|grupo de **comparação** da flag de renda|~6,9 %|
|No income|renda faltando; inadimplem um pouco **menos**|~5,6 %|
|Codes 96/98|códigos no lugar de contagem de atrasos|**~55 %**|

> 💡 **O que é 96/98:** valores nas 3 colunas de atraso (30–59, 60–89, 90+). Ninguém atrasa 96 vezes em dois anos, então são **códigos**, não contagens. São 269 clientes. A base não documenta o significado; é uma inferência sua. 💡 **A barra é a taxa de inadimplência (o futuro, a variável-alvo)**, não o atraso passado. Mais da metade desses clientes acabou inadimplente. 💡 A linha tracejada é a média de 6,7 %. Para 96/98, o grupo de comparação é essa média.

---

## 4 · Six data traps (até 2:00)

**Falar**

- Those flags came from **traps in the data**:
    1. Impossible values, like an age of zero.
    2. Codes 96 and 98 posing as late-payment counts.
    3. A debt ratio computed without income.
    4. Missing values that carry signal.
    5. Long tails.
    6. A **leak in my own first notebook**: I imputed medians using all rows, test rows included.
- Each trap became a fixed rule in a shared module, and every step that learns moved inside the pipeline.

**Cola dos números (não ler no slide)**

|#|Número|O que fiz|
|---|---|---|
|01|idade 0 (1 cliente); rotativo até 50.708× o limite (264 acima de 4×)|faltante + flag rotativo > 400 %|
|02|269 clientes, 3 colunas, 55 % inadimplem|faltante + flag|
|03|renda faltando em 29.731 (20 %); razão mediana 1.159 vs 0,30|razão vira faltante se renda é faltante|
|04|sem renda: 5,6 % vs 6,9 %|flags, em vez de imputar o sinal|
|05|assimetria 127 (renda) e 81 (razão de dívida)|$\log(1+x)$ na logística|
|06|medianas com todas as linhas|tudo que aprende dentro do pipeline|

> 💡 **Assimetria positiva = cauda para a direita**: poucos valores gigantes. O log comprime a cauda. 💡 **Faltante informativo:** o fato de faltar já diz algo sobre o risco. Imputar a mediana apagaria isso; a flag preserva. 💡 **Razão sem denominador:** sem renda, dívida/renda explode (mediana 1.159 contra 0,30). 💡 **Vazamento (leak):** o teste deve simular clientes que nunca vi. Se a mediana usa linhas do teste, o treino "viu" o teste e a nota fica otimista. Correção: o pipeline calcula a mediana só no treino (a cada fold) e aplica ao teste. 🗣️ Frase-chave: _"The test set must behave like clients I have never seen, so nothing may learn from it."_ ⏱️ Se estiver atrasado: só os nomes das armadilhas + vazamento + correção.

---

## 5 · Method (até 2:35)

**Falar**

- Two models from opposite ends of the trade-off (Lecture 9).
- **Logistic regression**: the main method. Every coefficient is an odds ratio, so a refusal can be **explained** to the client.
- **Random forest**: finds non-linear effects and interactions on its own, but is harder to explain.
- Same protocol for both: stratified 80/20 split with the test set locked away; five-fold cross-validation for every choice; test set opened **only once**, at the end.

**Termos, se perguntarem**

- **$p$ na logística:** probabilidade de inadimplência, $p=\sigma(\beta_0+x^\top\beta)$.
- **$\sqrt{p}$ na floresta:** $p$ = número de variáveis; cada divisão sorteia $\sqrt{p}$ delas (deixa as árvores diferentes).
- **Odds ratio $e^{\beta}$:** quanto as chances multiplicam quando a variável sobe uma unidade. Variáveis contínuas foram padronizadas, então é por 1 desvio-padrão.
- **Estratificado:** cada parte mantém os 6,7 % de inadimplentes.
- **300 árvores:** cada uma treina numa amostra bootstrap.

> ⏱️ Se estiver atrasado: corte os detalhes das caixas (300 árvores, $\sqrt{p}$, log, padronização).

---

## 6 · Regularization did not help (até 3:05)

**Falar**

- Compared ridge and lasso over a grid of C.
- Regularization **did not help**: 120 thousand rows, only 14 coefficients, so there is little to shrink. The chosen C = 10 is barely penalized.
- _[corte]_ A very strong ridge still ranks well, but its probabilities are worse than a constant.
- That is why I choose by **log-loss**, not only by AUC.

> 💡 **$C = 1/\alpha$:** C pequeno = penalidade forte (esquerda do gráfico); C grande = fraca. 💡 **Painel (a), AUC:** plana (~0,852) de C = 0,1 em diante; ridge e lasso empatam. Lasso com C = 10⁻⁴ zera tudo: AUC 0,50. 💡 **Painel (b), log-loss:** ridge forte tem AUC 0,847, mas log-loss pior que o baseline constante (~0,245, a linha tracejada). 💡 **Escolho pelo log-loss, reporto a AUC.** 💡 Extras do rodapé: $\log(1+x)$ ajudou pouco (0,851 → 0,852); bins por quantil só +0,003.

---

## 7 · Deep trees memorize (até 3:30)

**Falar**

- Key setting for the forest: the minimum number of clients per leaf.
- With **one client per leaf**, the trees memorize the training folds: training AUC of 1, and the worst validation score.
- Larger leaves trade variance for bias (Lecture 6).
- **Twenty clients per leaf** gave the best validation log-loss.

> 💡 **Por que 20?** O critério é a **nota na validação**, não a distância entre as curvas. Depois de 20 a distância cai porque o **treino piora** (árvore simples demais), não porque a validação melhora. A validação fica parada ou piora um pouco (log-loss ~0,179 → ~0,181 em 200). 💡 É um **platô**: de 20 a 100 as diferenças são na terceira casa decimal; 20 é o mínimo. 🗣️ Se questionarem: _"Anything from 20 to 100 would be nearly the same; I took the minimum of the validation log-loss."_ 💡 As 300 árvores e o $\sqrt{p}$ foram **fixados, não ajustados**.

---

## 8 · Results (até 4:10)

**Falar**

- Only now did I open the test set.
- Forest AUC **0.866**, logistic regression **0.858**, close to the cross-validated scores: **nothing leaked**.
- The explainable model gives up **only 0.008**.
- With a cut-off that catches 70 percent of defaulters, the bank approves about **four in five** applicants.
- The bad rate among those approved falls from **6.7 to 2.4 percent**.
- At the same bad rate, the forest approves **649 more customers**.

**Tabela do slide**

|Modelo|Aprovados|Inadimplência dos aprovados|Bons recusados|
|---|---|---|---|
|Regressão logística|80,0 %|2,4 %|4.590|
|Random forest|82,1 %|2,4 %|3.949|

> 💡 **Curva ROC:** y = inadimplentes pegos (recall); x = bons pagadores barrados por engano. Quanto mais no canto superior esquerdo, melhor; a diagonal é cara ou coroa (0,5). As duas curvas quase se sobrepõem. 💡 **Gini:** $\text{Gini}=2\cdot\text{AUC}-1$ → 0,73 (floresta) e 0,72 (logística). 🐢 **Falar devagar:** 0,866 · 0,858 · 0,008 · 6,7 → 2,4 % · 649. ⏱️ Se estiver atrasado: pule Gini e "bons recusados".

---

## 9 · Risk drivers (até 4:35)

**Falar**

- Both models agree on **late payments and revolving use**.
- In the logistic regression, the flag for codes 96 and 98 multiplies the odds of default by **more than twelve** (12.6): the cleaning work paid off.
- Age lowers the risk, which raises the **fairness** question from Lecture 9: should a credit model learn this?

> 💡 **Painel (a), odds ratio:** eixo logarítmico; **1 = nenhum efeito**. À direita aumenta o risco, à esquerda diminui (idade). 💡 **Painel (b), importância:** queda média de impureza de Gini. Soma, nas 300 árvores, o quanto cada variável reduz a mistura de bons e maus pagadores nas divisões. Mostra **quanto** a variável é usada, não a **direção**. ⚠️ **Se perguntarem por que a flag 96/98 quase não aparece na floresta:** minha leitura (não está no roteiro) é que a árvore já separa esses clientes pelas colunas de atraso, onde 96/98 são valores extremos. A logística precisa da flag. 💡 Importância de Gini pode favorecer variáveis contínuas com muitos valores.

---

## 10 · What I would do differently (até 5:00)

**Falar**

- Write the cleaning rules as code **from day one**.
- Set the cut-off from **real costs**: the loss on a default against the margin on a good customer.
- Try gradient boosting and check calibration.
- Discuss whether **age** belongs in a credit model at all.
- **Thank you.**

> ⚠️ **Conferir o slide:** ele mostra só 3 tópicos e há uma linha vazia no topo da lista. O primeiro ponto ("regras de limpeza como código") não aparece; fale mesmo assim. 💡 Diga "gradient boosting e calibração" em vez de "Try new models". 💡 **Calibração:** uma probabilidade de 10 % corresponde a ~10 % de inadimplentes de fato. 💡 **Corte por custos:** hoje o corte (70 % dos inadimplentes) é arbitrário.

---

## Se perguntarem

- **Por que AUC e não acurácia?** Com 6,7 % de inadimplentes, "todo mundo é bom pagador" já acerta 93 %. A AUC mede se o modelo põe os maus acima dos bons no ranking.
- **E o log-loss?** Avalia também se as probabilidades estão boas, não só a ordem.
- **O que é o Gini?** $\text{Gini}=2\cdot\text{AUC}-1$: 0,73 para a floresta e 0,72 para a logística.
- **De onde vêm 80 % aprovados e 2,4 %?** Matriz de confusão no teste (notebook 02, seção 7): aprovados = TN + FN; inadimplência dos aprovados = FN / aprovados.
- **Por que não usar a floresta, se ela é melhor?** Ganha 0,008 de AUC, mas a logística explica cada recusa (odds ratio por variável), o que importa para o cliente e para o regulador.
- **O que são 96/98?** Códigos, não contagens, em 269 clientes. Em vez de descartar, virei flag, porque carregam muito sinal (55 % inadimplem).
- **Como o vazamento foi corrigido?** Passos que aprendem (imputação, padronização) ficam dentro do pipeline: ajustam só no treino de cada fold.
- **Por que min_samples_leaf = 20?** Menor log-loss na validação; de 20 a 100 é um platô.
- **Como a floresta decide a importância?** Queda média de impureza de Gini nas divisões, somada nas 300 árvores.
- **Por que a idade é um problema?** É característica pessoal, não escolha do cliente: o modelo deveria usá-la para negar crédito?