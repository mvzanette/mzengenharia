// Área restrita – Controle financeiro: receitas, despesas, valores a receber e resumo mensal.
import { abrirPagina } from "./sessao.js";
import { dataBR, hojeISO } from "./regras.js";
import * as G from "./regras-gestao.js";
import { $, esc, moeda, avisar, baixarCsv, opcoes, prepararDialogos, numeroDigitado } from "./ui.js";

const hoje = hojeISO();
let armazem, colecao;
let lancamentos = [];
let arts = [];
let demandas = [];
const filtro = { busca: "", periodo: "ano", tipo: "", situacao: "" };


async function recarregar() {
  [lancamentos, arts, demandas] = await Promise.all([
    colecao.listar(),
    armazem.listar(),
    armazem.colecao("demandas").listar(),
  ]);
  renderizar();
}

function renderizar() {
  renderResumo();
  renderTabela();
  renderMensal();
}

// ---------------------------------------------------------------- resumo
function kpi(rotulo, valor, detalhe = "", acao = "") {
  const tag = acao ? "button" : "div";
  const extra = acao ? ` type="button" data-situacao="${acao}" aria-pressed="${filtro.situacao === acao}"` : "";
  return `<${tag} class="kpi${acao ? " kpi-botao" : ""}"${extra}>
      <span class="kpi-rotulo">${rotulo}</span>
      <strong class="kpi-valor">${valor}</strong>
      ${detalhe ? `<span class="kpi-detalhe">${detalhe}</span>` : ""}
    </${tag}>`;
}

function renderResumo() {
  const p = G.periodo(filtro.periodo, hoje);
  const r = G.resumoFinanceiro(lancamentos, p, hoje);
  const nomePeriodo = G.PERIODOS.find(([k]) => k === filtro.periodo)[1].toLowerCase();
  $("#resumo").innerHTML = [
    kpi("Total recebido", moeda(r.recebido), nomePeriodo),
    kpi("Gastos totais", moeda(r.gastos), nomePeriodo),
    kpi("Lucro líquido", moeda(r.lucro), r.margem == null ? nomePeriodo : `margem de ${Math.round(r.margem * 100)}%`),
    kpi("A receber", moeda(r.aReceber), "no prazo", "pendente"),
    kpi("Em atraso", moeda(r.atrasado), `${r.qtdAtrasado} ${r.qtdAtrasado === 1 ? "recebimento" : "recebimentos"}`, "atrasado"),
  ].join("");
}

// ---------------------------------------------------------------- lista
function filtrados() {
  const p = G.periodo(filtro.periodo, hoje);
  const termo = filtro.busca.toLowerCase();
  return lancamentos
    .filter((l) => {
      const situacao = G.situacaoLancamento(l, hoje);
      // atrasados e pendentes aparecem mesmo fora do período
      if (situacao === "pago" && !(G.dataReferencia(l) >= p.inicio && G.dataReferencia(l) <= p.fim)) return false;
      if (situacao !== "pago" && filtro.periodo !== "tudo" && G.dataReferencia(l) > p.fim) return false;
      if (filtro.tipo && l.tipo !== filtro.tipo) return false;
      if (filtro.situacao && situacao !== filtro.situacao) return false;
      if (termo && ![l.descricao, l.cliente, l.categoria].join(" ").toLowerCase().includes(termo)) return false;
      return true;
    })
    .sort((a, b) => (G.dataReferencia(b) || "").localeCompare(G.dataReferencia(a) || ""));
}

function etiquetaSituacao(l) {
  const s = G.situacaoLancamento(l, hoje);
  const classe = { pago: "s-ativa", pendente: "s-vencendo", atrasado: "s-vencida" }[s];
  return `<span class="etiqueta ${classe}">${G.ROTULO_SITUACAO_LANC[l.tipo][s]}</span>`;
}

function renderTabela() {
  const lista = filtrados();
  $("#tabela tbody").innerHTML = lista
    .map(
      (l) => `<tr class="clicavel" data-id="${esc(l.id)}" tabindex="0">
        <td class="data">${dataBR(l.competencia)}</td>
        <td><span class="tipo tipo-${l.tipo}">${l.tipo === "receita" ? "Receita" : "Despesa"}</span></td>
        <td>${esc(l.descricao)}</td>
        <td>${esc(l.cliente || "—")}</td>
        <td class="servico">${esc(l.categoria || "—")}</td>
        <td class="data">${l.pago_em ? `pago em ${dataBR(l.pago_em)}` : dataBR(l.vencimento)}</td>
        <td class="num">${l.tipo === "despesa" ? "−" : ""}${moeda(Number(l.valor))}</td>
        <td>${etiquetaSituacao(l)}</td>
      </tr>`
    )
    .join("");
  $("#vazio").hidden = lista.length > 0;
}

function renderMensal() {
  const p = G.periodo(filtro.periodo, hoje);
  const meses = G.porMes(lancamentos, p.meses);
  $("#tabela-mensal tbody").innerHTML = meses
    .map(
      (m) => `<tr><td>${G.rotuloMes(m.mes)}</td><td class="num">${moeda(m.receitas)}</td>
        <td class="num">${moeda(m.despesas)}</td><td class="num${m.resultado < 0 ? " negativo" : ""}">${moeda(m.resultado)}</td></tr>`
    )
    .join("");
  const total = meses.reduce((t, m) => ({ r: t.r + m.receitas, d: t.d + m.despesas }), { r: 0, d: 0 });
  $("#tabela-mensal tfoot").innerHTML = `<tr><th>Total</th><th class="num">${moeda(total.r)}</th>
    <th class="num">${moeda(total.d)}</th><th class="num">${moeda(total.r - total.d)}</th></tr>`;
}

// ---------------------------------------------------------------- lançamento
const nomeArt = (a) => `${a.numero}${a.contratante ? " – " + a.contratante : ""}`;
const nomeDemanda = (d) => `${d.titulo}${d.cliente ? " – " + d.cliente : ""}`;

function abrirLancamento(id, novo = {}) {
  const existente = lancamentos.find((l) => l.id === id);
  const l = existente ? { ...existente } : { tipo: "receita", competencia: hoje, ...novo };
  const dlg = $("#dlg-lanc");
  const artsOrdenadas = [...arts].sort((a, b) => (b.registrada || "").localeCompare(a.registrada || ""));
  dlg.innerHTML = `<form id="form-lanc">
    <div class="dlg-cab">
      <h2>${existente ? "Editar lançamento" : l.tipo === "receita" ? "Nova receita" : "Nova despesa"}</h2>
      <button class="btn-link" data-fechar type="button">Fechar</button>
    </div>
    <div class="dlg-corpo">
      <div class="opcoes" role="radiogroup" aria-label="Tipo">
        <label><input type="radio" name="tipo" value="receita"${l.tipo === "receita" ? " checked" : ""}> Receita</label>
        <label><input type="radio" name="tipo" value="despesa"${l.tipo === "despesa" ? " checked" : ""}> Despesa</label>
      </div>
      <div class="campos">
        <label class="c4">Descrição<input name="descricao" value="${esc(l.descricao)}" required></label>
        <label class="c2">Categoria<select name="categoria"></select></label>
        <label class="c4">Cliente / fornecedor<input name="cliente" value="${esc(l.cliente)}"></label>
        <label class="c2">Valor (R$)<input name="valor" inputmode="decimal" value="${l.valor == null ? "" : String(l.valor).replace(".", ",")}" required></label>
        <label class="c2">Data do serviço / emissão<input type="date" name="competencia" value="${esc(l.competencia)}" required></label>
        <label class="c2">Vencimento<input type="date" name="vencimento" value="${esc(l.vencimento)}"></label>
        <label class="c2"><span class="rotulo-pago">${l.tipo === "despesa" ? "Pago em" : "Recebido em"}</span><input type="date" name="pago_em" value="${esc(l.pago_em)}"></label>
        <label class="c2">Forma de pagamento<select name="forma"><option value="">—</option>${opcoes(G.FORMAS, l.forma)}</select></label>
        <label class="c2">ART vinculada<select name="art_id"><option value="">Nenhuma</option>${opcoes(artsOrdenadas.map((a) => [a.id, nomeArt(a)]), l.art_id)}</select></label>
        <label class="c2">Demanda vinculada<select name="demanda_id"><option value="">Nenhuma</option>${opcoes(demandas.map((d) => [d.id, nomeDemanda(d)]), l.demanda_id)}</select></label>
        <label class="c6">Observação<textarea name="observacao" rows="2">${esc(l.observacao)}</textarea></label>
      </div>
      ${l.pago_em ? "" : `<button class="btn btn-claro" type="button" id="btn-pago-hoje">${l.tipo === "despesa" ? "Marcar como pago hoje" : "Marcar como recebido hoje"}</button>`}
    </div>
    <div class="dlg-rodape">
      ${existente ? `<button class="btn btn-perigo esquerda" type="button" id="btn-excluir">Excluir</button>` : ""}
      <button class="btn btn-claro" type="button" data-fechar>Cancelar</button>
      <button class="btn btn-primary" type="submit">Salvar</button>
    </div>
  </form>`;

  const form = $("#form-lanc", dlg);
  const campo = (nome) => form.elements[nome];
  const tipoAtual = () => form.querySelector("input[name=tipo]:checked").value;
  const preencherCategorias = (manter) => {
    const tipo = tipoAtual();
    campo("categoria").innerHTML = `<option value="">—</option>${opcoes(G.CATEGORIAS[tipo], manter)}`;
    $(".rotulo-pago", form).textContent = tipo === "despesa" ? "Pago em" : "Recebido em";
    const pagoHoje = $("#btn-pago-hoje", form);
    if (pagoHoje) pagoHoje.textContent = tipo === "despesa" ? "Marcar como pago hoje" : "Marcar como recebido hoje";
  };
  preencherCategorias(l.categoria);

  // Ao escolher a ART ou a demanda, completa o que estiver em branco
  const completar = (dados) => {
    for (const [nome, valor] of Object.entries(dados)) {
      if (valor == null || valor === "") continue;
      if (!campo(nome).value) campo(nome).value = nome === "valor" ? String(valor).replace(".", ",") : valor;
    }
  };
  const aoEscolherArt = () => {
    const art = arts.find((a) => a.id === campo("art_id").value);
    if (!art) return;
    if (tipoAtual() === "despesa") {
      if (!campo("categoria").value) campo("categoria").value = "Taxa de ART";
      if (campo("categoria").value === "Taxa de ART") completar({ descricao: `Taxa da ART nº ${art.numero}`, valor: art.taxa, cliente: `CREA-${art.crea}` });
    } else {
      completar({ descricao: `Serviço – ART nº ${art.numero}`, cliente: art.contratante, valor: art.valor });
    }
  };
  const aoEscolherDemanda = () => {
    const d = demandas.find((x) => x.id === campo("demanda_id").value);
    if (!d) return;
    completar({ descricao: d.titulo, cliente: d.cliente || d.contato, ...(tipoAtual() === "receita" ? { valor: d.valor } : {}) });
    if (tipoAtual() === "receita" && !campo("categoria").value && G.SERVICOS.includes(d.servico)) campo("categoria").value = d.servico;
    if (!campo("art_id").value && d.art_id) campo("art_id").value = d.art_id;
  };
  form.addEventListener("change", (e) => {
    if (e.target.name === "tipo") preencherCategorias(campo("categoria").value);
    if (e.target.name === "art_id") aoEscolherArt();
    if (e.target.name === "demanda_id") aoEscolherDemanda();
  });
  if (!existente) {
    if (novo.art_id) aoEscolherArt();
    if (novo.demanda_id) aoEscolherDemanda();
  }

  $("#btn-pago-hoje", form)?.addEventListener("click", (e) => {
    campo("pago_em").value = hoje;
    e.target.remove();
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const f = new FormData(form);
    const valor = numeroDigitado(f.get("valor"));
    if (valor == null || valor < 0) return avisar("Informe um valor válido.");
    const dados = { ...l, tipo: tipoAtual(), valor };
    for (const nome of ["descricao", "categoria", "cliente", "competencia", "vencimento", "pago_em", "forma", "art_id", "demanda_id", "observacao"]) {
      const v = (f.get(nome) ?? "").toString().trim();
      dados[nome] = v === "" ? null : v;
    }
    try {
      await colecao.salvar(dados);
      dlg.close();
      limparEndereco();
      avisar("Lançamento salvo.");
      await recarregar();
    } catch (err) {
      avisar("Não foi possível salvar: " + err.message);
    }
  });

  $("#btn-excluir", form)?.addEventListener("click", async () => {
    if (!confirm("Excluir este lançamento?")) return;
    await colecao.remover(existente.id);
    dlg.close();
    avisar("Lançamento excluído.");
    await recarregar();
  });

  dlg.showModal();
}

// Links de outras páginas: financeiro.html?novo=receita&demanda=<id> ou ?novo=despesa&art=<id>&categoria=Taxa de ART
function abrirPeloEndereco() {
  const q = new URLSearchParams(location.search);
  const tipo = q.get("novo");
  if (tipo !== "receita" && tipo !== "despesa") return;
  abrirLancamento(null, {
    tipo,
    art_id: q.get("art") || null,
    demanda_id: q.get("demanda") || null,
    categoria: q.get("categoria") || null,
  });
}
const limparEndereco = () => location.search && history.replaceState(null, "", location.pathname);

// ---------------------------------------------------------------- exportação
function exportar() {
  const lista = filtrados();
  if (!lista.length) return avisar("Não há lançamentos para exportar com os filtros atuais.");
  const artPorId = new Map(arts.map((a) => [a.id, a.numero]));
  const demPorId = new Map(demandas.map((d) => [d.id, d.titulo]));
  baixarCsv(
    `financeiro-${hoje}.csv`,
    ["Data", "Tipo", "Descrição", "Categoria", "Cliente/fornecedor", "Valor (R$)", "Vencimento", "Recebido/pago em",
      "Situação", "Forma de pagamento", "ART", "Demanda", "Observação"],
    lista.map((l) => [
      dataBR(l.competencia), l.tipo === "receita" ? "Receita" : "Despesa", l.descricao, l.categoria, l.cliente,
      Number(l.valor), l.vencimento ? dataBR(l.vencimento) : "", l.pago_em ? dataBR(l.pago_em) : "",
      G.ROTULO_SITUACAO_LANC[l.tipo][G.situacaoLancamento(l, hoje)], l.forma, artPorId.get(l.art_id) || "",
      demPorId.get(l.demanda_id) || "", l.observacao,
    ])
  );
}

// ---------------------------------------------------------------- eventos
function prepararEventos() {
  prepararDialogos();
  $("#btn-receita").addEventListener("click", () => abrirLancamento(null, { tipo: "receita" }));
  $("#btn-despesa").addEventListener("click", () => abrirLancamento(null, { tipo: "despesa" }));
  $("#btn-exportar").addEventListener("click", exportar);
  $("#busca").addEventListener("input", (e) => {
    filtro.busca = e.target.value;
    renderTabela();
  });
  $("#periodo").addEventListener("change", (e) => {
    filtro.periodo = e.target.value;
    renderizar();
  });
  $("#filtro-tipo").addEventListener("change", (e) => {
    filtro.tipo = e.target.value;
    renderTabela();
  });
  $("#filtro-situacao").addEventListener("change", (e) => {
    filtro.situacao = e.target.value;
    renderizar();
  });
  $("#resumo").addEventListener("click", (e) => {
    const b = e.target.closest("[data-situacao]");
    if (!b) return;
    filtro.situacao = filtro.situacao === b.dataset.situacao ? "" : b.dataset.situacao;
    $("#filtro-situacao").value = filtro.situacao;
    renderizar();
  });
  const abrirLinha = (e) => {
    const tr = e.target.closest("tr[data-id]");
    if (tr) abrirLancamento(tr.dataset.id);
  };
  $("#tabela tbody").addEventListener("click", abrirLinha);
  $("#tabela tbody").addEventListener("keydown", (e) => e.key === "Enter" && abrirLinha(e));
  $("#dlg-lanc").addEventListener("close", limparEndereco);
}

// Início: roda depois de todo o módulo carregado
async function iniciar() {
  const sessao = await abrirPagina("financeiro.html");
  if (!sessao) return;
  armazem = sessao.armazem;
  colecao = armazem.colecao("lancamentos");
  $("#tela").hidden = false;
  $("#periodo").innerHTML = opcoes(G.PERIODOS, filtro.periodo);
  prepararEventos();
  await recarregar();
  abrirPeloEndereco();
}

iniciar();
