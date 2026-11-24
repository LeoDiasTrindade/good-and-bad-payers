# Roteiro da lightning talk (5 min)

O texto abaixo é o mesmo das notas do apresentador no deck (tecla **N** no `slides.html`). São cerca de 690 palavras: em ritmo calmo (~140 palavras por minuto), fecha em 5 minutos.

- O tempo ao lado de cada slide é a meta acumulada; se estiver atrasado, pule as frases marcadas com *[corte]*.
- **Negrito** = palavra para enfatizar. A barra `/` marca uma pausa curta.
- Números para falar devagar: 6.7 %, 0.866 × 0.858, 2.4 %, 649.

---

## 1 · Cover — até 0:20

Hi, I'm Leonardo. / My project asks the question every lender asks before granting credit: / what is the **probability** that this person will be ninety days or more past due in the next two years? / In five minutes I'll show what I chose, what the data was hiding, what I tried, what I found, and what I would do differently.

## 2 · Give Me Some Credit — até 0:55

The data comes from **Give Me Some Credit**, a Kaggle competition from 2011: / 150 thousand past borrowers and ten features, such as late payments, use of revolving credit, debt ratio, income and age. / The **bad rate is 6.7 percent**, about seven in every hundred borrowers. / So accuracy is useless: calling everyone a good payer is already 93 percent accurate. / I judge the models by **AUC**, how well they rank risk, and by **log-loss**. / My question: **how much ranking power does an explainable model give up?**

## 3 · Late payments raise default risk over tenfold — até 1:25

First, what the training data shows. / Past late payments are the strongest signal: the bad rate goes from **4 percent** with none to **over 40 percent** with four or more, more than tenfold. / Heavy use of revolving credit raises the risk sharply in the top deciles, and older clients default less. / *[corte]* The last panel shows two flags I created: clients without income default slightly less, and clients with codes 96 or 98 default more than half the time.

## 4 · Six data traps — até 2:00

Those flags came from **traps in the data**. / Impossible values, like an age of zero. / Codes 96 and 98 posing as late-payment counts. / A debt ratio computed without income. / Missing values that carry signal. / Long tails. / And a **leak in my own first notebook**, which imputed medians using all rows, test rows included. / Each trap became a fixed rule in a shared module, and every step that learns moved inside the pipeline.

## 5 · Method — até 2:35

I compared two models from opposite ends of the trade-off discussed in Lecture 9. / The **logistic regression** is the main method: every coefficient is an odds ratio, so a refusal can be **explained** to the client. / The **random forest** finds non-linear effects and interactions on its own, but is harder to explain. / Both follow the same protocol: a stratified 80/20 split with the test set locked away, five-fold cross-validation for every choice, and the test set opened **only once**, at the end.

## 6 · Regularization did not help — até 3:05

For the logistic regression, I compared ridge and lasso over a grid of C. / Regularization **did not help**: with 120 thousand rows and only 14 coefficients there is little to shrink, so the chosen C of 10 is barely penalized. / *[corte]* One lesson from the left panel: a very strong ridge still ranks clients well, but on the right its probabilities are worse than a constant. / That is why I choose by **log-loss**, not only by AUC.

## 7 · Deep trees memorize — até 3:30

For the random forest, the key setting was the minimum number of clients per leaf. / With one client per leaf, the trees **memorize** the training folds: a training AUC of 1, and the worst validation score. / Larger leaves trade variance for bias, as in Lecture 6. / **Twenty clients per leaf** gave the best validation log-loss.

## 8 · Results — até 4:10

Only now did I open the test set. / The forest reaches an AUC of **0.866** and the logistic regression **0.858**, close to their cross-validated scores, so nothing leaked. / The explainable model gives up **only 0.008**. / In credit terms: with a cut-off that catches 70 percent of defaulters, the bank approves about **four in five** applicants, / and the bad rate among those approved falls from **6.7 to 2.4 percent**. / At that same bad rate, the forest approves **649 more customers**.

## 9 · Risk drivers — até 4:35

What drives the risk? / Both models agree on **late payments and revolving use**. / In the logistic regression, the flag for codes 96 and 98 multiplies the odds of default by **more than twelve**, so the cleaning work paid off. / Age lowers the risk, which raises the **fairness** question from Lecture 9: should a credit model learn this?

## 10 · What I would do differently — até 5:00

What would I do differently? / Write the cleaning rules as code **from day one**. / Set the cut-off from **real costs**: the loss on a default against the margin on a good customer. / Try gradient boosting and check calibration. / And discuss whether **age** belongs in a credit model at all. / **Thank you.**

---

## Se perguntarem

- **Por que AUC e não acurácia?** Com 6.7 % de inadimplentes, dizer "todo mundo é bom pagador" já acerta 93 %. A AUC mede se o modelo põe os maus acima dos bons no ranking.
- **O que é o Gini?** Em crédito se reporta Gini = 2·AUC − 1: 0.73 para a floresta e 0.72 para a regressão logística.
- **De onde vêm 80 % aprovados e 2.4 %?** Da matriz de confusão no teste (notebook 02, seção 7): aprovados = TN + FN; inadimplência dos aprovados = FN / aprovados.
- **Por que não usar a floresta, se ela é melhor?** Ganha 0.008 de AUC, mas a regressão logística explica cada recusa (odds ratio por variável), o que importa para o cliente e para o regulador.
