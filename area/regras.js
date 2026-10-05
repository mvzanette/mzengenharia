// Regras de prazos, alertas e recomendações das ARTs.
// Usado pela área restrita (navegador) e pela rotina diária de e-mails (Node).

export const AVISO_DIAS = 30; // primeiro alerta
export const MARCOS_ANTES = [30, 7, 0]; // dias antes do fim previsto em que há alerta
export const INTERVALO_ATRASO = 7; // depois de vencida, um alerta por semana até a baixa

const DIA = 86400000;

export function hojeISO(agora = new Date()) {
  // data local (Brasil), sem horário
  const d = new Date(agora.getTime() - agora.getTimezoneOffset() * 60000);
  return d.toISOString().slice(0, 10);
}

export function diasAte(fimISO, hoje = hojeISO()) {
  if (!fimISO) return null;
  return Math.round((Date.parse(fimISO + "T00:00:00Z") - Date.parse(hoje + "T00:00:00Z")) / DIA);
}

export function dataBR(iso) {
  if (!iso) return "—";
  const [a, m, d] = iso.split("-");
  return `${d}/${m}/${a}`;
}

// Situação da ART: baixada | sem-data | vencida | vencendo | ativa
export function situacao(art, hoje = hojeISO()) {
  if (art.baixa_data) return "baixada";
  const dias = diasAte(art.fim, hoje);
  if (dias === null) return "sem-data";
  if (dias < 0) return "vencida";
  if (dias <= AVISO_DIAS) return "vencendo";
  return "ativa";
}

export const ROTULO_SITUACAO = {
  ativa: "Ativa",
  vencendo: "Vence em até 30 dias",
  vencida: "Vencida sem baixa",
  baixada: "Baixada",
  "sem-data": "Sem data de término",
};

// Marco de alerta atingido hoje (ou o mais recente ainda não superado).
// d30 → entre 30 e 8 dias; d7 → entre 7 e 1 dia; d0 → no dia; atraso-N → N-ésima semana após o fim.
export function marcoAtual(art, hoje = hojeISO()) {
  if (art.baixa_data) return null;
  const dias = diasAte(art.fim, hoje);
  if (dias === null || dias > AVISO_DIAS) return null;
  if (dias > 7) return "d30";
  if (dias > 0) return "d7";
  if (dias === 0) return "d0";
  return "atraso-" + (Math.floor((-dias - 1) / INTERVALO_ATRASO) + 1);
}

const cliente = (art) => art.contratante || "não informado";

export function mensagem(art, marco, hoje = hojeISO()) {
  const dias = diasAte(art.fim, hoje);
  const fim = dataBR(art.fim);
  if (marco === "d30" || marco === "d7") {
    return `Daqui a ${dias} dias a ART nº ${art.numero} do cliente ${cliente(art)} vencerá (fim previsto em ${fim}).`;
  }
  if (marco === "d0") return `A ART nº ${art.numero} do cliente ${cliente(art)} vence hoje (${fim}).`;
  return `A ART nº ${art.numero} do cliente ${cliente(art)} venceu em ${fim} e ainda não tem baixa registrada.`;
}

// Alertas a exibir/enviar: um por ART, no marco atual, se ainda não foi marcado como lido/enviado.
export function alertasPendentes(arts, jaTratados = new Set(), hoje = hojeISO()) {
  const lista = [];
  for (const art of arts) {
    const marco = marcoAtual(art, hoje);
    if (!marco) continue;
    const chave = `${art.id || art.numero}:${marco}`;
    if (jaTratados.has(chave)) continue;
    lista.push({ chave, art, marco, mensagem: mensagem(art, marco, hoje), dias: diasAte(art.fim, hoje) });
  }
  return lista.sort((a, b) => a.dias - b.dias);
}

// ---------------------------------------------------------------- tipo de serviço
const CONTINUO = /pmoc|plano de manuten|manuten[çc][ãa]o preventiva|contrato de manuten|responsabilidade t[ée]cnica|execu[çc][ãa]o de manuten/i;

export function tipoServicoSugerido(art) {
  if (art.tipo_servico) return art.tipo_servico;
  if ((art.tos || []).includes("16.2.2")) return "continuo";
  const texto = [art.observacao, art.contrato, ...(art.atividades || []).map((a) => `${a.atividade} ${a.descricao}`)].join(" ");
  return CONTINUO.test(texto) ? "continuo" : "pontual";
}

// Ação recomendada quando a ART se aproxima do fim (ou já passou).
// pontual: pergunta se o serviço foi concluído; contínuo: pergunta se o contrato foi renovado.
export function recomendacao(tipo, resposta) {
  if (resposta === undefined || resposta === null) return null;
  if (tipo === "continuo") {
    return resposta
      ? {
          acao: "Dar baixa da ART atual e emitir nova ART para o novo período",
          passos: [
            "Dar baixa por conclusão da ART atual no portal do CREA, com a data de fim do período",
            "Emitir nova ART para o novo período do contrato (use “Copiar dados para nova ART”)",
            "Cadastrar aqui a nova ART e vinculá-la a esta",
          ],
        }
      : {
          acao: "Dar baixa por conclusão",
          passos: ["Dar baixa por conclusão no portal do CREA", "Registrar aqui a data da baixa"],
        };
  }
  return resposta
    ? {
        acao: "Dar baixa por conclusão",
        passos: ["Dar baixa por conclusão no portal do CREA", "Registrar aqui a data da baixa"],
      }
    : {
        acao: "Ajustar a data da ART ou dar baixa por interrupção",
        passos: [
          "Se o serviço continua: ajustar a data de término da ART conforme as regras do CREA (retificação)",
          "Se o serviço foi encerrado sem conclusão: dar baixa por interrupção, informando a fase em que parou",
          "Registrar aqui o que foi feito",
        ],
      };
}

// Texto para colar no portal do CREA ao emitir uma nova ART a partir de uma anterior.
export function textoNovaArt(art) {
  const linhas = [
    `Contratante: ${art.contratante || ""}${art.contratante_doc ? ` – CPF/CNPJ ${art.contratante_doc}` : ""}`,
    art.proprietario && art.proprietario !== art.contratante ? `Proprietário: ${art.proprietario}` : null,
    `Local da obra/serviço: ${[art.endereco, art.local].filter(Boolean).join(" – ")}`,
    art.contrato ? `Contrato: ${art.contrato}` : null,
    art.valor != null ? `Valor do contrato (anterior): R$ ${art.valor.toLocaleString("pt-BR", { minimumFractionDigits: 2 })}` : null,
    `Atividades (TOS):`,
    ...(art.atividades || []).map((a) => `  • ${a.atividade ? a.atividade + " – " : ""}${a.tos} ${a.descricao || ""}`.trimEnd()),
    art.observacao ? `Observação: ${art.observacao}` : null,
    `ART anterior: ${art.numero} (CREA-${art.crea})`,
  ];
  return linhas.filter(Boolean).join("\n");
}
