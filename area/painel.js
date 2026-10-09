// Painel da área restrita (area/index.html): cards de acesso a cada recurso.
import { abrirPagina } from "./sessao.js";
import { MODULOS } from "./modulos.js";
import * as R from "./regras.js";

const $ = (sel) => document.querySelector(sel);

const sessao = await abrirPagina("index.html");
if (sessao) {
  $("#conteudo").hidden = false;
  $("#modulos").innerHTML = MODULOS.map(card).join("");
  resumoArt(sessao.armazem);
}

function card(m) {
  const corpo = `<span class="modulo-icone">${m.icone}</span>
      <h2>${m.titulo}</h2>
      <p>${m.descricao}</p>
      <span class="modulo-status" id="status-${m.id}">${m.pagina ? "" : "Em breve"}</span>`;
  return m.pagina
    ? `<a class="modulo" href="${m.pagina}">${corpo}<span class="modulo-abrir">Abrir</span></a>`
    : `<div class="modulo em-breve" aria-disabled="true">${corpo}</div>`;
}

// Situação das ARTs no card do Controle de ART
async function resumoArt(armazem) {
  const lugar = $("#status-art");
  if (!lugar) return;
  try {
    const [arts, tratados] = await Promise.all([armazem.listar(), armazem.tratados()]);
    const hoje = R.hojeISO();
    const conta = (s) => arts.filter((a) => R.situacao(a, hoje) === s).length;
    const alertas = R.alertasPendentes(arts, tratados, hoje).length;
    const partes = [
      `${alertas} ${alertas === 1 ? "alerta pendente" : "alertas pendentes"}`,
      `${conta("vencendo")} vencendo em 30 dias`,
      `${conta("vencida")} vencidas sem baixa`,
    ];
    lugar.textContent = arts.length ? partes.join(" · ") : "Nenhuma ART cadastrada";
    if (alertas) lugar.classList.add("com-alerta");
  } catch {
    lugar.textContent = "";
  }
}
