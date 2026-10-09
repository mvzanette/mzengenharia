// Parte comum das páginas da área restrita: conexão, exigência de login, menu suspenso e aviso do modo demonstração.
import { SUPABASE_URL, SUPABASE_ANON_KEY } from "./config-area.js";
import { criarArmazem } from "./dados.js";
import { MODULOS } from "./modulos.js";

export const PAGINA_LOGIN = new URL("../area-restrita.html", import.meta.url).href;
export const PAGINA_PAINEL = new URL("index.html", import.meta.url).href;

const $ = (sel) => document.querySelector(sel);

export function conectar() {
  return criarArmazem({ url: SUPABASE_URL, chave: SUPABASE_ANON_KEY });
}

// Abre uma página da área: sem login, volta para a tela de login (e retorna para esta página depois de entrar).
export async function abrirPagina(pagina) {
  let armazem;
  try {
    armazem = await conectar();
  } catch {
    mostrarErro("Não foi possível conectar ao banco de dados. Verifique a internet e a configuração.");
    return null;
  }
  const usuario = await armazem.usuario();
  if (!usuario) {
    location.replace(`${PAGINA_LOGIN}?volta=${encodeURIComponent(pagina)}`);
    return null;
  }

  montarMenu(pagina);
  $("#usuario").textContent = usuario.email || "";
  $("#area-top").hidden = false;
  $("#btn-sair").addEventListener("click", async () => {
    await armazem.sair();
    location.replace(PAGINA_LOGIN);
  });

  if (armazem.modo === "demo") {
    $("#aviso-demo").hidden = false;
    $("#btn-limpar-demo").addEventListener("click", async () => {
      if (!confirm("Apagar todos os dados de teste deste navegador?")) return;
      await armazem.limparTudo();
      location.reload();
    });
  }
  return { armazem, usuario };
}

function montarMenu(atual) {
  const lugar = $("#menu-area");
  if (!lugar) return;
  const itens = [{ titulo: "Painel", pagina: "index.html" }, ...MODULOS]
    .map((m) => {
      if (!m.pagina) return `<span class="menu-item desativado">${m.titulo}<small>Em breve</small></span>`;
      const marcado = m.pagina === atual ? ' aria-current="page"' : "";
      return `<a class="menu-item" href="${m.pagina}"${marcado}>${m.titulo}</a>`;
    })
    .join("");
  lugar.innerHTML = `<details class="menu-suspenso">
      <summary>Menu</summary>
      <div class="menu-lista">${itens}<a class="menu-item menu-site" href="../index.html">Voltar ao site</a></div>
    </details>`;

  const menu = lugar.querySelector("details");
  document.addEventListener("click", (e) => {
    if (menu.open && !menu.contains(e.target)) menu.open = false;
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && menu.open) {
      menu.open = false;
      menu.querySelector("summary").focus();
    }
  });
}

function mostrarErro(texto) {
  const main = document.querySelector("main");
  main.hidden = false;
  main.insertAdjacentHTML("afterbegin", `<p class="cartao erro-geral" role="alert">${texto}</p>`);
}
