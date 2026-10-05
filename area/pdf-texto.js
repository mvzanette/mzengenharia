// Extrai o texto de um PDF em linhas, na ordem de leitura, usando o pdf.js.
// Funciona no navegador e no Node (recebe a biblioteca pdf.js já carregada).

const TOLERANCIA_Y = 2.5; // diferença máxima de altura para considerar a mesma linha

export async function extrairLinhas(pdfjs, dados) {
  const doc = await pdfjs.getDocument({ data: dados, isEvalSupported: false }).promise;
  const linhas = [];
  for (let n = 1; n <= doc.numPages; n++) {
    const pagina = await doc.getPage(n);
    const conteudo = await pagina.getTextContent();
    const itens = conteudo.items
      .filter((i) => i.str && i.str.trim())
      .map((i) => ({ x: i.transform[4], y: i.transform[5], w: i.width, h: Math.abs(i.transform[3]) || 8, s: i.str }));

    // agrupa por altura (y), de cima para baixo
    itens.sort((a, b) => b.y - a.y || a.x - b.x);
    const grupos = [];
    for (const item of itens) {
      const g = grupos.find((gr) => Math.abs(gr.y - item.y) <= TOLERANCIA_Y);
      if (g) g.itens.push(item);
      else grupos.push({ y: item.y, itens: [item] });
    }
    grupos.sort((a, b) => b.y - a.y);

    for (const g of grupos) {
      g.itens.sort((a, b) => a.x - b.x);
      let linha = "";
      let fim = null;
      for (const it of g.itens) {
        if (fim !== null) {
          const vao = it.x - fim;
          // vão grande separa colunas (dois espaços); vão pequeno é espaço comum
          linha += vao > it.h * 1.2 ? "  " : vao > it.h * 0.15 ? " " : "";
        }
        linha += it.s;
        fim = it.x + it.w;
      }
      linhas.push(linha.replace(/\s+$/, ""));
    }
    linhas.push(`--- fim da página ${n} ---`);
  }
  await doc.destroy();
  return linhas;
}
