# Template do artigo de Machine Learning

Estrutura baseada em `../ml-project.pdf`, com apresentação inspirada em
`../Estimation of risk contributions with MCMC_260224_203147.pdf`: uma coluna,
tipografia serifada, título centralizado, autor em maiúsculas, afiliação abaixo
do nome e abstract e keywords em blocos recuados. É um layout próprio com pacotes padrão;
não depende da classe editorial do artigo de referência.

O PDF contém o nome e a afiliação informados, um título provisório e Lorem ipsum
em todas as seções e nas keywords para visualizar o artigo diagramado. Substitua
esse preenchimento pelo conteúdo real antes de entregar o trabalho. As orientações
ficam em comentários que não aparecem no PDF. As seções científicas são numeradas;
as declarações finais e referências não. Não há cabeçalho, rodapé nem número de página.

## Onde editar

- `metadata.tex`: título provisório, autor, afiliação, keywords e metadados do PDF.
- `sections/*.tex`: um arquivo para cada seção, incluindo o abstract.
- `references.bib`: referências reais no formato BibTeX.
- `paper.sty`: diagramação e pacotes; normalmente não é necessário editar.
- `main.tex`: documento principal, que reúne os arquivos na ordem exigida.
- `main.pdf`: versão renderizada para consulta.

Os cabeçalhos estão em inglês, conforme o enunciado. O texto pode ser digitado
em UTF-8, com acentos. Se escrever o artigo em português, troque `[english]`
por `[brazil]` no carregamento de `babel` em `paper.sty` para ajustar a hifenização.

Ao preencher o artigo, substitua diretamente os parágrafos de Lorem ipsum em
`sections/` e as keywords em `metadata.tex`. As subseções de Data e Method são
sugestões editáveis, não exigências adicionais do enunciado. Não há quebras de
página fixas: a paginação acompanha o texto. O preenchimento de References está
em `sections/references-placeholder.tex`; não representa referências reais.

## Compilar no Windows

Na raiz do repositório:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\docs\paper\build.ps1
```

O script procura Tectonic no PATH ou em `.qa-runtime/tectonic/tectonic.exe`,
na raiz do repositório. Como alternativa, aceita `latexmk` com pdfLaTeX.
Os arquivos auxiliares ficam em `build/` e o PDF final é copiado para `main.pdf`
somente após uma compilação bem-sucedida. Logs e ferramentas locais são
ignorados pelo Git; o PDF final pode ser versionado.

Foi usado Tectonic 0.17.0 portátil. O compilador e seu cache local não fazem parte
dos arquivos versionados. Em outro computador, instale
[Tectonic](https://tectonic-typesetting.github.io/install.html) ou uma distribuição
LaTeX com `latexmk`. O primeiro uso do Tectonic requer acesso à internet para
baixar os pacotes; o cache é reaproveitado nas compilações seguintes.

Com uma distribuição LaTeX instalada, também é possível executar diretamente:

```sh
cd docs/paper
latexmk -pdf main.tex
```

Nesse caso, o PDF fica em `build/main.pdf`.

## Overleaf

Envie os arquivos desta pasta preservando `sections/`, selecione `main.tex` como
documento principal e use pdfLaTeX. Não é necessário enviar `build/`, o PDF
gerado ou o compilador portátil.

## Citações, figuras e tabelas

Depois de adicionar referências reais em `references.bib`, ative
`\paperbibliographytrue` em `metadata.tex`. Use `\citet{chave}` para citações
narrativas e `\citep{chave}` para citações entre parênteses. Tectonic e latexmk
executam BibTeX e as recompilações necessárias automaticamente. Enquanto a
bibliografia estiver desativada, References exibirá o parágrafo de preenchimento.

Para figuras, crie `figures/` e use `\includegraphics`. Os pacotes `graphicx`,
`booktabs` e `amsmath` já estão disponíveis para figuras, tabelas e equações.
Use `\label` e `\ref` para referências cruzadas em vez de números escritos à mão.

O enunciado pede contribuições dos autores mesmo em trabalho individual e uma
declaração explícita das ferramentas de IA utilizadas e suas finalidades.
O arquivo dessa declaração contém um comentário lembrando o uso de Codex para
a criação deste template; o texto da declaração permanece a seu cargo.
