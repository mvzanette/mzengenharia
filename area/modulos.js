// Recursos da área restrita. Aparecem no painel (página inicial da área) e no menu suspenso do cabeçalho.
// Para incluir um recurso novo: acrescente um item nesta lista e crie a página correspondente na pasta area/.
// Enquanto "pagina" for null, o recurso aparece como "Em breve".

const svg = (caminhos) => `<svg class="i" viewBox="0 0 24 24" aria-hidden="true">${caminhos}</svg>`;

export const MODULOS = [
  {
    id: "art",
    titulo: "Controle de ART",
    descricao: "Prazos, alertas de vencimento, baixas e renovação das ARTs.",
    pagina: "art.html",
    icone: svg('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m9 15 2 2 4-4"/>'),
  },
  {
    id: "financeiro",
    titulo: "Controle financeiro",
    descricao: "Receitas, despesas, valores a receber e em atraso, resumo mensal e exportação em planilha.",
    pagina: "financeiro.html",
    icone: svg('<rect x="2" y="5" width="20" height="14" rx="1"/><path d="M2 10h20"/><path d="M6 15h4"/>'),
  },
  {
    id: "demandas",
    titulo: "Controle de demandas",
    descricao: "Solicitações de clientes, propostas, etapas, prazos e lembretes de cada serviço.",
    pagina: "demandas.html",
    icone: svg('<path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="M9 12h6M9 16h4"/>'),
  },
];
