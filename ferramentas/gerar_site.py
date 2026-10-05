"""Gera as páginas HTML do site a partir de um só lugar.

Cabeçalho, formulário de contato e rodapé são compartilhados por todas as páginas.
Para alterar um texto, edite este arquivo e rode, na pasta do site:

    python3 ferramentas/gerar_site.py
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

EMAIL = "mvszanette@gmail.com"
WHATS = "5532998111414"
FONE = "(32) 99811-1414"
CREA = "CREA/RNP 1420122860"

# ---------------------------------------------------------------- ícones (traço)
ICON = {
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "down": '<path d="m6 9 6 6 6-6"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="1"/><path d="m22 7-10 6L2 7"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "badge": '<rect x="3" y="4" width="18" height="16" rx="1"/><circle cx="9" cy="10" r="2"/><path d="M15 8h2M15 12h2M7 16h10"/>',
    "forklift": '<path d="M12 12H5a2 2 0 0 0-2 2v5"/><circle cx="13" cy="19" r="2"/><circle cx="5" cy="19" r="2"/><path d="M8 19h3m5-17v17h6M6 12V7c0-1.1.9-2 2-2h3l5 5"/>',
    "gauge": '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="1"/><path d="M16 2v4M8 2v4M3 10h18"/><path d="m9 16 2 2 4-4"/>',
    "presentation": '<path d="M2 3h20"/><path d="M21 3v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V3"/><path d="m7 21 5-5 5 5"/>',
    "droplet": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
    "fan": '<path d="M10.827 16.379a6.082 6.082 0 0 1-8.618-7.002l5.412 1.45a6.082 6.082 0 0 1 7.002-8.618l-1.45 5.412a6.082 6.082 0 0 1 8.618 7.002l-5.412-1.45a6.082 6.082 0 0 1-7.002 8.618l1.45-5.412Z"/><path d="M12 12v.01"/>',
    "snow": '<path d="M2 12h20M12 2v20M4.93 4.93l14.14 14.14M4.93 19.07 19.07 4.93"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="m9 15 2 2 4-4"/>',
    "track": '<rect x="2" y="8" width="20" height="8" rx="4"/><circle cx="7" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="17" cy="12" r="1.5"/>',
    "tire": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="M12 2v6M12 16v6M2 12h6M16 12h6"/>',
    "filter": '<path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/>',
    "fuel": '<path d="M3 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18"/><path d="M2 22h14"/><path d="M15 9h2a2 2 0 0 1 2 2v6a2 2 0 0 0 4 0V8l-3-3"/><path d="M7 7h4"/>',
    "bolt": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "factory": '<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1M12 18h1M7 18h1"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "chart": '<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>',
    "plug": '<path d="M12 22v-5M9 8V2M15 8V2M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
}


def icon(nome, cls="i"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICON[nome]}</svg>'


CK = '<svg class="ck" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12"/><path d="m7 12.5 3.2 3.2L17 9"/></svg>'


def checks(itens, cls="checks"):
    """Lista com check. Cada item é texto simples ou (título, descrição)."""
    linhas = []
    for item in itens:
        if isinstance(item, tuple):
            corpo = f"<div><strong>{item[0]}</strong><span>{item[1]}</span></div>"
        else:
            corpo = f"<div>{item}</div>"
        linhas.append(f"          <li>{CK}{corpo}</li>")
    return f'<ul class="{cls}">\n' + "\n".join(linhas) + "\n        </ul>"


def faq(itens):
    return "\n".join(
        f"          <details>\n            <summary>{p}</summary>\n            <p>{r}</p>\n          </details>"
        for p, r in itens
    )


# ---------------------------------------------------------------- partes comuns
FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' fill='%23f5b800'/%3E%3Ctext x='16' y='21.5' text-anchor='middle' "
    "font-family='Arial, sans-serif' font-weight='800' font-size='14' fill='%23111214'%3EMZ%3C/text%3E%3C/svg%3E"
)


def head(titulo, descricao, com_formulario=False, extra="", indexar=True):
    tos = '\n  <script src="tos-mecanica.js" defer></script>' if com_formulario else ""
    robots = "" if indexar else '\n  <meta name="robots" content="noindex">'
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{titulo}</title>
  <meta name="description" content="{descricao}">{robots}
  <meta property="og:title" content="{titulo}">
  <meta property="og:description" content="{descricao}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <link rel="icon" href="{FAVICON}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <script src="config.js"></script>{tos}
  <script src="main.js" defer></script>{extra}
</head>
<body>
"""


def header(inicio, contato="#contato"):
    """inicio = "" na página inicial ou "index.html" nas demais."""
    home = inicio or "#inicio"
    return f"""
  <header class="site-header">
    <a class="logo" href="{home}" aria-label="Marcos Zanette – Engenharia Mecânica, página inicial">
      <span class="logo-mark" aria-hidden="true">MZ</span>
      <span class="logo-text">MARCOS ZANETTE<small>ENGENHARIA MECÂNICA</small></span>
    </a>
    <button class="menu-toggle" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu">{icon("menu")}</button>
    <nav class="nav" id="menu" aria-label="Principal">
      <a href="{inicio}#nr12">Laudo NR-12</a>
      <a href="{inicio}#servicos">Serviços</a>
      <a href="{inicio}#frotas">Gestão de frotas</a>
      <a href="{inicio}#eletrificacao">Eletrificação</a>
      <a href="{inicio}#industrial">Manutenção industrial</a>
      <a class="btn btn-primary" href="{contato}">Solicitar proposta</a>
    </nav>
  </header>
"""


UFS = "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split()

# Lista curta de serviços. Cada opção leva os códigos TOS (área 16 – Mecânica) que chegam no e-mail.
SERVICOS_FORM = [
    ("Laudo NR-12", [
        ("Laudo NR-12 – equipamento móvel / linha amarela", "16.7.29 16.5.6"),
        ("Laudo NR-12 – caminhão munck", "16.5.9"),
        ("Laudo NR-12 – empilhadeira", "16.5.8"),
        ("Laudo NR-12 – máquinas industriais", "16.7.29 16.7.32"),
    ]),
    ("Laudos mecânicos e eletromecânicos", [
        ("Laudo de equipamento de movimentação de terra", "16.7.4.5"),
        ("Laudo mecânico", "16.7.4"),
        ("Laudo eletromecânico", "16.7.5"),
        ("Laudo de caminhões", "16.5.5.4"),
        ("Laudo de implementos e reboques", "16.5.7 16.5.10"),
    ]),
    ("Laudo NR-13", [
        ("Laudo NR-13 – vaso de pressão / compressor", "16.3.2 16.3.3 16.3.15"),
        ("Laudo NR-13 – caldeira", "16.2.1.10"),
    ]),
    ("Manutenção e gestão de frotas", [
        ("Plano de manutenção de frota / equipamentos", "16.5.6 16.7.4"),
        ("Consultoria em gestão de frota", "16.5.6 16.5.5"),
        ("Treinamento para gestores de frota", "16.5.6 16.5.5"),
        ("Especificação de insumos", "16.5.6 16.5.5"),
    ]),
    ("Eletrificação de frotas", [
        ("Análise de viabilidade de eletrificação de frota", "16.5.5 16.5.6"),
    ]),
    ("Manutenção industrial", [
        ("Laudo de máquinas e equipamentos industriais", "16.7.32"),
        ("Consultoria em manutenção industrial", "16.7.13 16.7.32"),
        ("Assessoria técnica em manutenção industrial", "16.7.13 16.7.32"),
    ]),
    ("Climatização", [
        ("PMOC", "16.2.2"),
        ("Projeto de instalação de ar-condicionado", "16.2.1.4"),
    ]),
    ("Içamento", [
        ("Plano de rigging / içamento", "16.6.3 16.6.7"),
    ]),
    ("ART e outros", [
        ("ART de serviço de engenharia mecânica", ""),
    ]),
]


def opcoes_servico(selecionado=None):
    linhas = [f'<option value="" disabled{"" if selecionado else " selected"}>Selecione o serviço…</option>']
    for grupo, itens in SERVICOS_FORM:
        linhas.append(f'<optgroup label="{grupo}">')
        for nome, tos in itens:
            sel = " selected" if nome == selecionado else ""
            linhas.append(f'  <option data-tos="{tos}"{sel}>{nome}</option>')
        linhas.append("</optgroup>")
    linhas.append('<option data-outro value="Outro serviço (lista do CREA)">Outro serviço – escolher na lista do CREA</option>')
    return "\n".join("                " + l for l in linhas)


def contato(selecionado=None):
    ufs = "\n".join(f"                  <option>{uf}</option>" for uf in UFS)
    return f"""
    <!-- ============ CONTATO ============ -->
    <section class="contact on-dark" id="contato">
      <div class="container contact-grid">
        <div class="contact-info">
          <h2 class="section-title">Contato</h2>
          <p>Para solicitar uma proposta técnica, preencha o formulário com os dados do serviço e do equipamento.</p>
          <ul class="contact-list">
            <li>{icon("mail")}<div><small>E-mail</small><a href="mailto:{EMAIL}" data-email>{EMAIL}</a></div></li>
            <li>{icon("phone")}<div><small>WhatsApp</small><a href="https://wa.me/{WHATS}" data-whatsapp target="_blank" rel="noopener">{FONE}</a></div></li>
            <li>{icon("badge")}<div><small>Responsável técnico</small>Marcos Zanette – Engenheiro Mecânico<br><span data-config="crea">{CREA}</span></div></li>
          </ul>
        </div>

        <!-- Envio pelo FormSubmit (gratuito). O e-mail de destino é definido em config.js. -->
        <form class="quote-form" id="form-proposta" action="https://formsubmit.co/{EMAIL}" method="POST">
          <input type="hidden" name="_subject" value="Solicitação de proposta pelo site">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_captcha" value="false">
          <input type="hidden" name="_next" value="">
          <input type="hidden" name="_autoresponse" value="Sua solicitação de proposta foi recebida e será respondida pelo e-mail ou telefone informado. Marcos Zanette – Engenheiro Mecânico – {CREA}">
          <input type="hidden" name="Código TOS" value="">
          <input type="text" name="_honey" class="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true">

          <div class="form-grid">
            <div class="field">
              <label for="f-nome">Nome</label>
              <input id="f-nome" name="Nome" type="text" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="f-email">E-mail</label>
              <input id="f-email" name="email" type="email" autocomplete="email" required>
            </div>
            <div class="field">
              <label for="f-whats">WhatsApp</label>
              <input id="f-whats" name="WhatsApp" type="tel" autocomplete="tel" inputmode="tel" required>
            </div>
            <div class="field">
              <label for="f-empresa">Empresa <span class="opt">(opcional)</span></label>
              <input id="f-empresa" name="Empresa" type="text" autocomplete="organization">
            </div>
            <div class="field w4">
              <label for="f-cidade">Cidade</label>
              <input id="f-cidade" name="Cidade" type="text" autocomplete="address-level2" required>
            </div>
            <div class="field w2">
              <label for="f-uf">Estado</label>
              <select id="f-uf" name="Estado" required>
                <option value="" disabled selected>UF</option>
{ufs}
              </select>
            </div>
            <div class="field">
              <label for="f-doc">CPF/CNPJ <span class="opt">(opcional)</span></label>
              <input id="f-doc" name="CPF/CNPJ" type="text" inputmode="numeric">
            </div>
            <div class="field">
              <label for="f-qtd">Nº de equipamentos <span class="opt">(opcional)</span></label>
              <input id="f-qtd" name="Quantidade" type="text" inputmode="numeric">
            </div>
            <div class="field full">
              <label for="f-servico">Serviço</label>
              <select id="f-servico" name="Serviço" required>
{opcoes_servico(selecionado)}
              </select>
            </div>
            <div class="tos-box" id="tos-box" hidden>
              <p>Selecione o item na Tabela de Obras e Serviços do CREA (área de Mecânica).</p>
              <div class="field full">
                <label for="tos-subarea">Subárea</label>
                <select id="tos-subarea"></select>
              </div>
              <div class="field full">
                <label for="tos-obra">Obra ou serviço</label>
                <select id="tos-obra"></select>
              </div>
              <div class="field full">
                <label for="tos-complemento">Complemento <span class="opt">(quando houver)</span></label>
                <select id="tos-complemento"></select>
              </div>
            </div>
            <div class="field full">
              <label for="f-equip">Equipamento <span class="opt">(fabricante, modelo e ano – opcional)</span></label>
              <input id="f-equip" name="Equipamento" type="text">
            </div>
            <div class="field full">
              <label for="f-msg">Mensagem <span class="opt">(opcional)</span></label>
              <textarea id="f-msg" name="Mensagem"></textarea>
            </div>
          </div>

          <p class="lgpd">Os dados informados são utilizados exclusivamente para a elaboração e o envio da proposta. Consulte a <a href="politica-de-privacidade.html">Política de Privacidade</a>.</p>
          <button class="btn btn-primary" type="submit">Enviar solicitação</button>
        </form>
      </div>
    </section>
"""


def footer(inicio):
    home = inicio or "#inicio"
    return f"""
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <a class="logo" href="{home}" aria-label="Marcos Zanette – Engenharia Mecânica, página inicial">
            <span class="logo-mark" aria-hidden="true">MZ</span>
            <span class="logo-text">MARCOS ZANETTE<small>ENGENHARIA MECÂNICA</small></span>
          </a>
          <p>Engenharia mecânica aplicada à manutenção, à segurança e à conformidade legal de equipamentos e frotas.</p>
        </div>
        <div>
          <h3>Serviços</h3>
          <ul>
            <li><a href="laudo-nr12.html">Laudo NR-12</a></li>
            <li><a href="laudo-nr13.html">Laudo NR-13</a></li>
            <li><a href="pmoc.html">PMOC</a></li>
            <li><a href="{inicio}#frotas">Gestão de frotas</a></li>
            <li><a href="{inicio}#eletrificacao">Eletrificação de frotas</a></li>
            <li><a href="{inicio}#industrial">Manutenção industrial</a></li>
          </ul>
        </div>
        <div>
          <h3>Contato</h3>
          <ul>
            <li><a href="mailto:{EMAIL}" data-email>{EMAIL}</a></li>
            <li><a href="{inicio}#contato">Solicitar proposta</a></li>
          </ul>
        </div>
        <div>
          <h3>Responsável técnico</h3>
          <ul>
            <li>Marcos Zanette</li>
            <li>Engenheiro Mecânico</li>
            <li data-config="crea">{CREA}</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© <span id="ano">2026</span> Marcos Zanette – Engenharia Mecânica</span>
        <span><a href="politica-de-privacidade.html">Política de Privacidade</a> · <a href="area-restrita.html" rel="nofollow">Área restrita</a></span>
      </div>
    </div>
  </footer>

</body>
</html>
"""


# ---------------------------------------------------------------- página inicial
EQUIPAMENTOS = [
    ("Linha amarela", "Escavadeira hidráulica", "escavadeira"),
    ("Linha amarela", "Pá carregadeira", "pa-carregadeira"),
    ("Linha amarela", "Trator de esteiras", "trator-esteiras"),
    ("Linha amarela", "Motoniveladora", "motoniveladora"),
    ("Linha amarela", "Rolo compactador", "rolo-compactador"),
    ("Linha amarela", "Retroescavadeira", "retroescavadeira"),
    ("Linha amarela", "Minicarregadeira", "minicarregadeira"),
    ("Linha diesel", "Caminhão munck", "caminhao-munck"),
    ("Linha diesel", "Caminhão basculante", "caminhao-basculante"),
    ("Linha diesel", "Caminhão pipa", "caminhao-pipa"),
    ("Linha diesel", "Caminhão comboio", "caminhao-comboio"),
    ("Apoio", "Veículos leves e de apoio", "veiculos-apoio"),
]

# Cards de serviço (estrutura VIX): ícone, título, texto, link e nome da foto em img/servicos/<foto>.jpg
SERVICOS = [
    ("forklift", "Laudo NR-12", "Apreciação de riscos, matriz de conformidade e ART para equipamentos móveis, caminhões e máquinas industriais.", "laudo-nr12.html", "laudo-nr12"),
    ("gauge", "Laudo NR-13", "Inspeção de segurança de vasos de pressão, compressores, autoclaves e caldeiras.", "laudo-nr13.html", "laudo-nr13"),
    ("wrench", "Laudos mecânicos e eletromecânicos", "Avaliação técnica de equipamentos, componentes e sistemas mecânicos e eletromecânicos, com ART.", None, "laudos-mecanicos"),
    ("calendar", "Planos de manutenção", "Planos de manutenção preventiva e corretiva por equipamento, com base em horímetro, quilometragem e recomendações do fabricante.", None, "planos-manutencao"),
    ("presentation", "Consultoria e treinamento para gestores de frota", "Diagnóstico, indicadores e capacitação para a gestão de manutenção de frotas.", "#frotas", "consultoria-frotas"),
    ("droplet", "Especificação de insumos", "Indicação dos insumos mais adequados para cada aplicação: material rodante, pneus, insumos de manutenção e combustíveis.", "#frotas", "insumos"),
    ("bolt", "Eletrificação de frotas", "Análise de viabilidade técnica e econômica para a transição de veículos e equipamentos para modelos elétricos.", "#eletrificacao", "eletrificacao"),
    ("factory", "Manutenção industrial", "Laudos, consultoria e assessoria técnica para a manutenção de máquinas, equipamentos e instalações industriais.", "#industrial", "manutencao-industrial"),
    ("fan", "PMOC", "Plano de Manutenção, Operação e Controle de sistemas de climatização, conforme a Lei 13.589/2018.", "pmoc.html", "pmoc"),
    ("snow", "Projeto de instalação de ar-condicionado", "Projeto de instalação de sistemas de ar-condicionado, com cálculo de carga térmica e ART.", "pmoc.html", "ar-condicionado"),
    ("file", "ART", "Anotação de Responsabilidade Técnica para obras e serviços de engenharia mecânica.", None, "art"),
]

OUTROS = [
    "Instalações de gás",
    "Sistemas de combate a incêndio",
    "Estruturas para eventos",
    "Equipamentos de elevação e içamento",
    "Veículos, reboques e food trucks",
    "Projetos e memoriais de cálculo",
    "Parecer técnico e perícia",
]

CASOS = [
    ("Laudo NR-12", "Caminhão com guindaste hidráulico (munck)", "Apreciação de riscos com HRN e categoria de segurança, análise do sistema hidráulico e da movimentação de cargas, procedimentos operacionais e recomendações dos fabricantes do caminhão e do guindaste.", "Máquina móvel · 2026"),
    ("Laudo NR-12", "Minicarregadeira em área portuária", "Matriz de conformidade NR-12, análise preliminar de riscos com cálculo HRN, histórico de manutenção preventiva e requisitos de mineração e portos (NR-22 e NR-29).", "Rio de Janeiro · 2026"),
    ("Vistoria e memorial de cálculo", "Trenó de arraste para 2.000 kg", "Inspeção visual e dimensional, memorial de cálculo estrutural de longarinas, cambão e pontos de içamento, e ART.", "Rio de Janeiro · 2026"),
    ("PMOC", "Base administrativa com 6 ambientes climatizados", "Levantamento de ocupantes, áreas e carga térmica, com rotinas e periodicidade de manutenção conforme a Lei 13.589/2018 e a Resolução ANVISA RE nº 9/2003.", "Rio de Janeiro · 2026"),
    ("Parecer técnico", "Falha em motor de veículo após a compra", "Testes de ignição e injeção, desmontagem parcial e análise das evidências para apurar a natureza e a extensão do dano.", "Juiz de Fora/MG · 2026"),
]

NORMAS_NR12 = [
    "NR-12", "NR-11", "NR-22", "NR-29", "ABNT NBR ISO 12100", "ISO/TR 14121-2", "ABNT NBR 14153",
    "ABNT NBR ISO 13849-1", "ABNT NBR ISO 13850", "ABNT NBR ISO 14118", "ABNT NBR ISO 14119", "ABNT NBR ISO 20474",
]

FAQ_INICIO = [
    ("Quais equipamentos precisam de laudo NR-12?",
     "A NR-12 se aplica a máquinas e equipamentos utilizados no trabalho, incluindo equipamentos móveis como escavadeiras, carregadeiras, caminhões munck e empilhadeiras. O laudo documenta a apreciação de riscos e a conformidade com os requisitos da norma."),
    ("Qual a validade do laudo NR-12?",
     "A NR-12 não define um prazo fixo de validade. O laudo deve ser revisado sempre que houver modificação no equipamento, mudança de aplicação, acidente ou atualização normativa. Para equipamentos críticos, a revisão periódica é uma boa prática."),
    ("O laudo atende às exigências de mobilização de grandes contratantes?",
     "O laudo contempla apreciação de riscos, matriz de conformidade, registro fotográfico e ART, que são os itens normalmente exigidos para a liberação de equipamentos em operações de mineração, portos e óleo e gás."),
    ("O que é ART?",
     "A Anotação de Responsabilidade Técnica, instituída pela Lei 6.496/1977, é o registro no CREA que identifica o profissional responsável por um serviço de engenharia, como laudo, projeto, vistoria ou plano de manutenção."),
    ("A consultoria atende frotas de qualquer porte?",
     "Sim. O escopo é definido de acordo com o tamanho da frota, os tipos de equipamento e os objetivos da operação."),
    ("O treinamento pode ser realizado na empresa?",
     "Sim. Os treinamentos são realizados na empresa ou online, com conteúdo adaptado à frota e à operação, e emissão de certificado de participação."),
    ("A análise de eletrificação inclui o projeto elétrico da recarga?",
     "A análise dimensiona a demanda de energia e a infraestrutura de recarga necessária e serve de base para o projeto elétrico, que é elaborado por profissional habilitado em engenharia elétrica."),
    ("Quais serviços de manutenção industrial são atendidos?",
     "Laudos técnicos de máquinas e equipamentos, consultoria para estruturação e gestão da manutenção e assessoria técnica em paradas programadas, especificações, contratação e acompanhamento de serviços."),
    ("Como é definido o valor do serviço?",
     "O valor é definido conforme o tipo de serviço, a quantidade e o tipo de equipamento e a necessidade de deslocamento, e é informado na proposta."),
]


def pagina_inicial():
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Marcos Zanette – Engenharia Mecânica",
        "description": "Laudo NR-12 para equipamentos móveis, gestão e eletrificação de frotas, manutenção industrial, laudos NR-13, PMOC e ART.",
        "telephone": "+55-32-99811-1414",
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": "Juiz de Fora", "addressRegion": "MG", "addressCountry": "BR"},
        "areaServed": "BR",
    }, ensure_ascii=False, indent=2)
    extra = '\n  <script type="application/ld+json">\n' + jsonld + "\n  </script>"

    equip = "\n".join(
        f"""          <figure class="equip">
            <div class="equip-img" style="--photo:url('img/equipamentos/{slug}.jpg') center / cover no-repeat" role="img" aria-label="{nome}"></div>
            <figcaption><span class="equip-tag">{tag}</span><span class="equip-name">{nome}</span></figcaption>
          </figure>"""
        for tag, nome, slug in EQUIPAMENTOS
    )
    servicos = "\n".join(
        f"""          <article class="svc">
            <div class="svc-img" style="--photo:url('img/servicos/{foto}.jpg') center / cover no-repeat">
              <span class="svc-icon">{icon(ic)}</span>
            </div>
            <div class="svc-body">
              <h3>{titulo}</h3>
              <p>{texto}</p>{f'''
              <a class="link-arrow" href="{link}">Saiba mais</a>''' if link else ''}
            </div>
          </article>"""
        for ic, titulo, texto, link, foto in SERVICOS
    )
    outros = "\n".join(f"                <li>{o}</li>" for o in OUTROS)
    casos = "\n".join(
        f"""          <article class="case">
            <span class="case-tag">{tag}</span>
            <h3>{titulo}</h3>
            <p>{texto}</p>
            <span class="case-meta">{meta}</span>
          </article>"""
        for tag, titulo, texto, meta in CASOS
    )
    normas = "\n".join(f"          <li>{n}</li>" for n in NORMAS_NR12)
    destaques = [
        ("track", "Material rodante", "Avaliação de desgaste e especificação de esteiras, roletes, rodas-guia e sapatas conforme a aplicação."),
        ("tire", "Pneus", "Especificação por aplicação e severidade da operação, com acompanhamento de desgaste, pressão e custo por hora ou quilômetro."),
        ("filter", "Insumos de manutenção preventiva e corretiva", "Filtros, lubrificantes, graxas, fluidos e componentes de reposição adequados a cada plano de manutenção."),
        ("fuel", "Eficiência energética de combustíveis", "Análise de consumo por hora trabalhada ou por quilômetro, comparação entre combustíveis e aditivos e identificação de perdas."),
    ]
    destaques_html = "\n".join(
        f"""            <div class="highlight">{icon(ic)}<h4>{t}</h4><p>{d}</p></div>"""
        for ic, t, d in destaques
    )

    return head(
        "Soluções em Engenharia Mecânica | Laudo NR-12 e Gestão de Frotas",
        "Laudo NR-12 para equipamentos móveis, gestão e eletrificação de frotas, manutenção industrial, laudos NR-13, PMOC e ART. Engenheiro mecânico especialista em linha amarela e caminhões linha diesel.",
        com_formulario=True, extra=extra,
    ) + header("") + f"""
  <main>
    <!-- ============ TOPO ============ -->
    <section class="hero" id="inicio">
      <div class="container">
        <h1>Soluções em engenharia mecânica</h1>
        <p class="hero-lead">Laudos NR-12 para equipamentos móveis, gestão e eletrificação de frotas e manutenção industrial, com foco em linha amarela e caminhões linha diesel.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="#contato">Solicitar proposta</a>
          <a class="btn btn-outline" href="#nr12">Laudo NR-12</a>
        </div>
      </div>
      <a class="hero-down" href="#numeros" aria-label="Rolar para o conteúdo">{icon("down")}</a>
    </section>

    <!-- ============ NÚMEROS ============ -->
    <section class="stats" id="numeros" aria-label="Números">
      <div class="container">
        <div class="stats-grid">
          <div class="stat"><strong>10</strong><span>Anos de atuação</span></div>
          <div class="stat"><strong>+700</strong><span>Equipamentos sob gestão</span></div>
          <div class="stat"><strong>+200</strong><span>Laudos emitidos</span></div>
          <div class="stat"><strong>4</strong><span>Setores atendidos</span></div>
        </div>
        <div class="scope">
          <p><b>Equipamentos</b>Linha amarela · Caminhões linha diesel · Veículos leves e de apoio</p>
          <p><b>Setores</b>Mineração · Portos · Óleo e gás · Construção</p>
        </div>
      </div>
    </section>

    <!-- ============ LAUDO NR-12 ============ -->
    <section id="nr12">
      <div class="container">
        <div class="feature">
          <div class="feature-img photo" role="img" aria-label="Equipamento de linha amarela em operação"></div>
          <div>
            <h2 class="section-title">Laudo NR-12 para equipamentos móveis</h2>
            <p class="section-intro">Avaliação técnica de conformidade com a NR-12 para equipamentos de linha amarela, caminhões e implementos, com apreciação de riscos, matriz de conformidade e ART registrada no CREA. Atende às exigências de fiscalização e aos requisitos de mobilização de grandes contratantes.</p>
            {checks([
                ("Inspeção em campo", "Checklist do equipamento e teste de funcionamento, com simulação de paradas e emergências."),
                ("Apreciação de riscos", "Identificação dos perigos e cálculo HRN, com categoria de segurança e PLr quando aplicável."),
                ("Matriz de conformidade NR-12", "Verificação item a item dos requisitos aplicáveis ao equipamento."),
                ("Recomendações técnicas", "Medidas de adequação em ordem de prioridade, incluindo as recomendações do fabricante."),
                ("Laudo com ART", "Relatório com registro fotográfico, conclusão técnica e ART registrada no CREA."),
            ])}
            <div class="feature-actions">
              <a class="btn btn-primary" href="#contato">Solicitar proposta</a>
              <a class="link-arrow" href="laudo-nr12.html">Detalhes do laudo NR-12</a>
            </div>
          </div>
        </div>

        <h3 class="subhead">Quando o laudo é exigido</h3>
        <div class="req-grid">
          <div class="req"><h3>Mobilização em contratantes</h3><p>Liberação de equipamentos em operações de mineração, portos e óleo e gás.</p></div>
          <div class="req"><h3>Fiscalização do trabalho</h3><p>Comprovação da conformidade com a NR-12 perante a auditoria fiscal.</p></div>
          <div class="req"><h3>Locação de equipamentos</h3><p>Documentação técnica exigida por locadoras e locatários.</p></div>
          <div class="req"><h3>Compra e venda</h3><p>Avaliação das condições de segurança na aquisição ou venda de equipamentos.</p></div>
          <div class="req"><h3>Auditorias e certificações</h3><p>Evidência técnica para auditorias de clientes e sistemas de gestão.</p></div>
          <div class="req"><h3>Modificações e acidentes</h3><p>Reavaliação após alterações, mudança de aplicação ou ocorrências.</p></div>
        </div>

        <h3 class="subhead">Normas aplicadas</h3>
        <ul class="chips">
{normas}
        </ul>
      </div>
    </section>

    <!-- ============ EQUIPAMENTOS ============ -->
    <section class="bg-gray" id="equipamentos">
      <div class="container">
        <h2 class="section-title">Equipamentos atendidos</h2>
        <p class="section-intro">Laudos, inspeções e gestão de manutenção para equipamentos de linha amarela, caminhões linha diesel e veículos de apoio.</p>
        <div class="equip-grid">
{equip}
        </div>
      </div>
    </section>

    <!-- ============ SERVIÇOS ============ -->
    <section id="servicos">
      <div class="container">
        <h2 class="section-title">Serviços</h2>
        <p class="section-intro">Engenharia mecânica aplicada à manutenção, à segurança e à conformidade legal de equipamentos e instalações.</p>
        <div class="svc-grid">
{servicos}
          <article class="svc svc-others">
            <div class="svc-body">
              <span class="svc-icon">{icon("list")}</span>
              <h3>Outros serviços</h3>
              <ul>
{outros}
              </ul>
              <a class="link-arrow" href="#contato">Solicitar proposta</a>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- ============ GESTÃO DE FROTAS ============ -->
    <section class="bg-gray" id="frotas">
      <div class="container">
        <h2 class="section-title">Consultoria para gestão de frotas</h2>
        <p class="section-intro">Apoio técnico a gestores de frotas de linha amarela e caminhões linha diesel, com foco na disponibilidade dos equipamentos, na redução do custo de manutenção e na conformidade com a legislação.</p>
        <div class="fleet-grid">
          <div class="panel">
            <h3>Consultoria e treinamento</h3>
            <h4>Consultoria</h4>
            {checks([
                "Diagnóstico da gestão de manutenção: processos, indicadores e histórico de falhas",
                "Estruturação de planos de manutenção preventiva por equipamento, com base no horímetro ou na quilometragem e nas recomendações do fabricante",
                "Definição e acompanhamento de indicadores: disponibilidade física, MTBF, MTTR, backlog e custo por hora trabalhada",
                "Análise de falhas recorrentes e ações de confiabilidade",
                "Rotinas de inspeção pré-uso e controle da documentação técnica (laudos NR-12, ARTs, manuais)",
                "Preparação da frota para mobilização em grandes contratantes",
            ])}
            <h4>Treinamento</h4>
            {checks([
                "Gestão de manutenção de frotas: planejamento, controle e indicadores",
                "NR-12 aplicada a equipamentos móveis: requisitos, inspeção e documentação",
                "Inspeção pré-uso para operadores e mecânicos",
                "Lubrificação e controle de contaminação",
                "Confiabilidade e análise de falhas",
            ])}
            <p class="note">Na empresa ou online, com conteúdo adaptado à frota e à operação. Certificado de participação.</p>
          </div>
          <div class="panel">
            <h3>Especificação de insumos</h3>
            <p>Indicação técnica dos insumos mais adequados para cada equipamento e condição de operação. <strong>Recomendação independente, sem vínculo com fabricantes ou fornecedores.</strong></p>
            <div class="highlight-grid">
{destaques_html}
            </div>
            <div class="kv">
              <p><b>Também avaliados:</b> peças de desgaste e ferramentas de penetração no solo (dentes, lâminas e bordas cortantes).</p>
              <p><b>Critérios:</b> aplicação e severidade da operação, recomendações do fabricante, histórico de falhas, análise de óleo e custo por hora trabalhada.</p>
              <p><b>Entregável:</b> relatório de especificação com as recomendações por equipamento.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ ELETRIFICAÇÃO ============ -->
    <section id="eletrificacao">
      <div class="container">
        <div class="feature">
          <div>
            <h2 class="section-title">Eletrificação de frotas</h2>
            <p class="section-intro">Análise de viabilidade técnica e econômica para a transição de veículos e equipamentos a combustão para modelos elétricos ou híbridos. Metas de descarbonização, exigências de grandes contratantes e a variação do preço do diesel tornam a eletrificação uma decisão estratégica: a análise indica onde ela é viável e em quanto tempo o investimento retorna.</p>
            {checks([
                ("Diagnóstico da frota", "Perfil de uso, ciclos de trabalho, quilometragem ou horas trabalhadas, consumo de combustível e custo de manutenção por equipamento."),
                ("Seleção dos candidatos", "Identificação dos veículos e equipamentos com maior potencial de eletrificação, conforme a operação e a disponibilidade de modelos no mercado."),
                ("Autonomia e ciclo de operação", "Compatibilidade entre a autonomia das baterias, os turnos de trabalho e as rotas."),
                ("Infraestrutura de recarga", "Levantamento da demanda de energia e do tipo, da quantidade e da localização dos carregadores, como base para o projeto elétrico."),
                ("Custo total de propriedade (TCO)", "Comparativo entre aquisição, energia e combustível, manutenção, vida útil das baterias e valor residual, com cálculo do retorno do investimento."),
                ("Emissões e ESG", "Estimativa da redução de emissões de CO₂ e indicadores para relatórios de sustentabilidade."),
            ])}
            <p class="note"><b>Entregável:</b> relatório de viabilidade técnico-econômica, com recomendação por grupo de equipamentos e plano de transição em etapas.</p>
            <div class="feature-actions">
              <a class="btn btn-primary" href="#contato">Solicitar proposta</a>
            </div>
          </div>
          <div class="feature-img elec-img photo" role="img" aria-label="Veículo elétrico em recarga"></div>
        </div>
      </div>
    </section>

    <!-- ============ MANUTENÇÃO INDUSTRIAL ============ -->
    <section class="bg-gray" id="industrial">
      <div class="container">
        <h2 class="section-title">Manutenção industrial</h2>
        <p class="section-intro">Laudos, consultoria e assessoria técnica para aumentar a disponibilidade e a segurança de máquinas, equipamentos e instalações industriais.</p>
        <div class="ind-grid">
          <div class="panel">
            <div class="service-icon">{icon("clipboard")}</div>
            <h3>Laudos</h3>
            {checks([
                "Laudos técnicos de máquinas e equipamentos industriais",
                "Laudo NR-12 de máquinas fixas e linhas de produção",
                "Laudo NR-13 de vasos de pressão, compressores e caldeiras",
                "Laudos de condição e de análise de falhas",
                "Laudos mecânicos e eletromecânicos com ART",
            ])}
          </div>
          <div class="panel">
            <div class="service-icon">{icon("chart")}</div>
            <h3>Consultoria</h3>
            {checks([
                "Estruturação do plano de manutenção preventiva, preditiva e corretiva",
                "Indicadores de manutenção: disponibilidade, MTBF, MTTR e backlog",
                "Classificação de criticidade e gestão de ativos",
                "Análise de causa raiz de falhas recorrentes",
                "Gestão de sobressalentes e estoque de peças",
            ])}
          </div>
          <div class="panel">
            <div class="service-icon">{icon("search")}</div>
            <h3>Assessoria técnica</h3>
            {checks([
                "Planejamento e acompanhamento de paradas programadas",
                "Especificação técnica para compra de equipamentos e serviços",
                "Avaliação técnica de propostas e fornecedores",
                "Acompanhamento e fiscalização de serviços de terceiros",
                "Suporte técnico em auditorias e fiscalizações",
            ])}
          </div>
        </div>
      </div>
    </section>

    <!-- ============ PERFIL ============ -->
    <section class="profile on-dark" id="perfil">
      <div class="profile-text">
        <h2 class="section-title">Responsável técnico</h2>
        <p class="profile-name">MARCOS ZANETTE</p>
        <p class="profile-role">Engenheiro Mecânico · <span data-config="crea">{CREA}</span></p>
        {checks([
            "Gerente de manutenção",
            "Especialista em equipamentos de linha amarela e caminhões linha diesel",
            "Especialista em confiabilidade e eficiência operacional",
            "Conformidade com a legislação",
        ])}
        <div class="years"><strong>10</strong><span>Anos de atuação<br>na área</span></div>
      </div>
      <div class="profile-img photo" role="img" aria-label="Equipamento de linha amarela"></div>
    </section>

    <!-- ============ EXPERIÊNCIA ============ -->
    <!-- Apenas descrições do tipo de trabalho: os laudos são confidenciais e não devem ser publicados. -->
    <section id="experiencia">
      <div class="container">
        <h2 class="section-title">Experiência</h2>
        <p class="section-intro">Laudos e projetos desenvolvidos para grandes empresas de mineração e óleo e gás.</p>
        <div class="cases">
{casos}
        </div>
      </div>
    </section>

    <!-- ============ PERGUNTAS FREQUENTES ============ -->
    <section class="bg-gray center" id="duvidas">
      <div class="container">
        <h2 class="section-title">Perguntas frequentes</h2>
        <div class="faq">
{faq(FAQ_INICIO)}
        </div>
      </div>
    </section>
{contato()}
  </main>
""" + footer("")


# ---------------------------------------------------------------- páginas de serviço
PAGINAS = [
    {
        "arquivo": "laudo-nr12.html",
        "titulo": "Laudo NR-12 para Equipamentos Móveis | Marcos Zanette Engenharia Mecânica",
        "descricao": "Laudo NR-12 com apreciação de riscos, matriz de conformidade e ART para escavadeiras, carregadeiras, caminhões munck, empilhadeiras e máquinas industriais.",
        "migalha": "Laudo NR-12",
        "h1": "Laudo NR-12",
        "lead": "Apreciação de riscos, matriz de conformidade e ART para equipamentos móveis de linha amarela, caminhões munck, empilhadeiras e máquinas industriais.",
        "quando_titulo": "Quando é exigido",
        "quando": [
            "Mobilização de equipamentos em contratantes de mineração, portos e óleo e gás",
            "Fiscalização do trabalho",
            "Locação, compra e venda de equipamentos",
            "Auditorias de clientes e certificações",
            "Instalação de proteções e dispositivos de segurança",
            "Modificações, acidentes ou mudança de aplicação",
        ],
        "inclui": [
            "Inspeção técnica em campo",
            "Identificação do equipamento e análise documental",
            "Apreciação de riscos com cálculo HRN",
            "Categoria de segurança e PLr, quando aplicável",
            "Matriz de conformidade com os requisitos da NR-12",
            "Recomendações técnicas e do fabricante",
            "Registro fotográfico",
            "ART registrada no CREA",
        ],
        "metodo": [
            ("Inspeção em campo", "Checklist do equipamento e teste de funcionamento, simulando paradas e emergências."),
            ("Análise documental", "Manuais, histórico de manutenção e procedimentos operacionais."),
            ("Apreciação de riscos", "Identificação dos perigos e cálculo HRN, com categoria de segurança e PLr quando aplicável."),
            ("Matriz de conformidade", "Verificação item a item dos requisitos da NR-12."),
            ("Recomendações", "Medidas técnicas em ordem de prioridade, incluindo as recomendações do fabricante."),
            ("Laudo e ART", "Relatório com registro fotográfico, conclusão técnica e ART registrada no CREA."),
        ],
        "faq": [
            ("Qual a validade do laudo NR-12?",
             "A NR-12 não define um prazo fixo de validade. O laudo deve ser revisado sempre que houver modificação no equipamento, mudança de aplicação, acidente ou atualização normativa. Para equipamentos críticos, a revisão periódica é uma boa prática."),
            ("Quem pode emitir o laudo NR-12?",
             "Um profissional legalmente habilitado, com registro ativo no CREA, como o engenheiro mecânico, que registra a ART do serviço. Sem a ART, o laudo não tem validade perante a fiscalização."),
            ("O laudo atende às exigências de mobilização de grandes contratantes?",
             "O laudo contempla apreciação de riscos, matriz de conformidade, registro fotográfico e ART, que são os itens normalmente exigidos para a liberação de equipamentos em operações de mineração, portos e óleo e gás."),
            ("O laudo inclui a adequação dos equipamentos?",
             "O laudo identifica o que precisa ser adequado e indica as soluções técnicas. A fabricação e a instalação de proteções físicas não fazem parte do laudo."),
            ("Como é definido o valor do serviço?",
             "O valor é definido conforme a quantidade e o tipo de equipamento e a necessidade de deslocamento, e é informado na proposta."),
        ],
        "opcao": "Laudo NR-12 – equipamento móvel / linha amarela",
    },
    {
        "arquivo": "laudo-nr13.html",
        "titulo": "Laudo NR-13 de Vasos de Pressão, Compressores e Caldeiras | Marcos Zanette Engenharia Mecânica",
        "descricao": "Inspeção de segurança e laudo NR-13 de vasos de pressão, compressores de ar, autoclaves e caldeiras, com ART de engenheiro mecânico.",
        "migalha": "Laudo NR-13",
        "h1": "Laudo NR-13",
        "lead": "Inspeção de segurança e laudo de vasos de pressão, compressores de ar, autoclaves e caldeiras, com ART.",
        "quando_titulo": "Quando é necessário",
        "quando": [
            "Antes de colocar o equipamento em operação (inspeção inicial)",
            "Nas inspeções periódicas, nos prazos definidos pela NR-13",
            "Após reparos, alterações, mudança de local ou longo período parado",
            "Fiscalização do trabalho e auditorias",
            "Exigência de seguradoras ou de contratantes",
        ],
        "inclui": [
            "Inspeção de segurança do equipamento no local",
            "Verificação de válvula de segurança, manômetro e dispositivos de controle",
            "Conferência da placa de identificação",
            "Orientação sobre a documentação obrigatória (prontuário e registro de segurança)",
            "Relatório de inspeção com parecer conclusivo",
            "ART registrada no CREA",
        ],
        "faq": [
            ("Todo compressor precisa de NR-13?",
             "O enquadramento depende da pressão máxima de operação e do volume do reservatório, conforme os critérios da NR-13. Esses dados constam na placa de identificação do equipamento e podem ser informados no formulário de contato."),
            ("Com que frequência a inspeção deve ser feita?",
             "Os prazos das inspeções periódicas dependem da categoria do equipamento e da existência de Serviço Próprio de Inspeção na empresa, conforme a NR-13. O prazo da próxima inspeção é indicado no relatório."),
            ("E se o equipamento não tiver documentação?",
             "É uma situação comum em equipamentos antigos ou usados. Na inspeção, o caso é avaliado e são indicadas as providências para regularizar a documentação exigida pela norma."),
            ("Como é definido o valor do serviço?",
             "O valor é definido conforme a quantidade e o tipo de equipamento, os ensaios necessários e a necessidade de deslocamento, e é informado na proposta."),
        ],
        "opcao": "Laudo NR-13 – vaso de pressão / compressor",
    },
    {
        "arquivo": "pmoc.html",
        "titulo": "PMOC e Projeto de Ar-Condicionado com ART | Marcos Zanette Engenharia Mecânica",
        "descricao": "PMOC – Plano de Manutenção, Operação e Controle de sistemas de climatização com responsável técnico e ART, conforme a Lei 13.589/2018, e projeto de instalação de ar-condicionado.",
        "migalha": "PMOC",
        "h1": "PMOC",
        "lead": "Plano de Manutenção, Operação e Controle de sistemas de climatização, com responsável técnico e ART, conforme a Lei 13.589/2018.",
        "quando_titulo": "Quem precisa",
        "quando": [
            "Escritórios e empresas",
            "Lojas, shoppings e restaurantes",
            "Clínicas, consultórios e hospitais",
            "Escolas, academias e templos",
            "Hotéis e órgãos públicos",
            "Condomínios com áreas comuns climatizadas",
        ],
        "inclui": [
            "Levantamento dos aparelhos e dos ambientes climatizados",
            "PMOC com as rotinas e a periodicidade de manutenção",
            "Responsabilidade técnica com ART registrada no CREA",
            "Orientação para os registros de manutenção",
            "Orientação sobre as análises de qualidade do ar (Resolução ANVISA RE nº 9/2003)",
        ],
        "nota": "Também disponível: projeto de instalação de sistemas de ar-condicionado, com cálculo de carga térmica e ART.",
        "faq": [
            ("O PMOC é obrigatório?",
             "Sim, para edifícios de uso público e coletivo com ar-condicionado, conforme a Lei 13.589/2018. A ausência do PMOC sujeita o estabelecimento às penalidades da legislação sanitária."),
            ("É necessário um engenheiro para elaborar o PMOC?",
             "Sim. O PMOC deve ter um responsável técnico habilitado, com ART. A manutenção do dia a dia pode continuar com a equipe ou empresa de refrigeração já contratada, seguindo o plano."),
            ("A empresa já tem manutenção contratada. O PMOC ainda é necessário?",
             "Sim. A empresa de manutenção executa os serviços; o PMOC é o plano que define o que deve ser feito e com que frequência, sob a responsabilidade de um engenheiro."),
            ("Como é definido o valor do serviço?",
             "O valor é definido conforme a quantidade de aparelhos, o tamanho do local e a necessidade de deslocamento, e é informado na proposta."),
        ],
        "opcao": "PMOC",
    },
]


def pagina_servico(p):
    quando = checks(p["quando"])
    inclui = checks(p["inclui"])
    nota = f'\n        <p class="note">{p["nota"]}</p>' if p.get("nota") else ""
    metodo = ""
    fundo_faq = "bg-gray"
    if p.get("metodo"):
        etapas = "\n".join(
            f"          <li>\n            <h3>{t}</h3>\n            <p>{d}</p>\n          </li>" for t, d in p["metodo"]
        )
        normas = "\n".join(f"          <li>{n}</li>" for n in NORMAS_NR12)
        metodo = f"""
    <section class="bg-gray" id="metodologia">
      <div class="container">
        <h2 class="section-title">Metodologia</h2>
        <ol class="steps">
{etapas}
        </ol>
        <h3 class="subhead">Normas aplicadas</h3>
        <ul class="chips">
{normas}
        </ul>
      </div>
    </section>
"""
        fundo_faq = ""
    return head(p["titulo"], p["descricao"], com_formulario=True) + header("index.html") + f"""
  <main>
    <section class="page-hero">
      <div class="container">
        <nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a> / {p["migalha"]}</nav>
        <h1>{p["h1"]}</h1>
        <p>{p["lead"]}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="#contato">Solicitar proposta</a>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="split">
          <div class="panel">
            <h3>{p["quando_titulo"]}</h3>
            {quando}
          </div>
          <div class="panel">
            <h3>O que está incluído</h3>
            {inclui}
          </div>
        </div>{nota}
      </div>
    </section>
{metodo}
    <section class="{fundo_faq} center" id="duvidas">
      <div class="container">
        <h2 class="section-title">Perguntas frequentes</h2>
        <div class="faq">
{faq(p["faq"])}
        </div>
      </div>
    </section>
{contato(p["opcao"])}
  </main>
""" + footer("index.html")


def pagina_obrigado():
    return head("Solicitação recebida | Marcos Zanette Engenharia Mecânica",
                "Solicitação de proposta recebida.", indexar=False) + header("index.html", "index.html#contato") + """
  <main class="thanks">
    <div>
      <h1>Solicitação recebida</h1>
      <p>Sua solicitação de proposta foi registrada e será respondida pelo e-mail ou telefone informado.</p>
      <a class="btn btn-dark" href="index.html">Voltar ao site</a>
    </div>
  </main>
""" + footer("index.html")


def pagina_privacidade():
    return head("Política de Privacidade | Marcos Zanette Engenharia Mecânica",
                "Política de privacidade do site Marcos Zanette – Engenharia Mecânica.") + header("index.html", "index.html#contato") + f"""
  <main>
    <section class="page-hero">
      <div class="container">
        <nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a> / Política de Privacidade</nav>
        <h1>Política de Privacidade</h1>
        <p>Como os dados enviados pelo formulário de contato são tratados, em conformidade com a Lei Geral de Proteção de Dados (Lei 13.709/2018).</p>
      </div>
    </section>

    <section>
      <div class="container prose">
        <h2>Responsável pelos dados</h2>
        <p>Marcos Zanette, engenheiro mecânico, {CREA}. Contato: <a href="mailto:{EMAIL}" data-email>{EMAIL}</a>.</p>

        <h2>Dados coletados</h2>
        <p>Pelo formulário de contato são coletados: nome, e-mail, telefone/WhatsApp, cidade e estado, e, opcionalmente, empresa, CPF/CNPJ, dados do equipamento e a mensagem enviada.</p>

        <h2>Finalidade</h2>
        <p>Os dados são utilizados exclusivamente para responder à solicitação, elaborar e enviar a proposta técnica e manter o contato relacionado ao serviço solicitado. Não são utilizados para envio de publicidade nem compartilhados para fins comerciais.</p>

        <h2>Base legal</h2>
        <p>O tratamento se baseia na execução de procedimentos preliminares relacionados a contrato, a pedido do titular dos dados (art. 7º, V, da LGPD).</p>

        <h2>Compartilhamento</h2>
        <p>O envio do formulário é processado pelo serviço FormSubmit (formsubmit.co), que encaminha a mensagem por e-mail. O site também carrega fontes do Google Fonts. Fora esses serviços técnicos necessários ao funcionamento do site, os dados não são compartilhados com terceiros.</p>

        <h2>Armazenamento</h2>
        <p>Os dados são mantidos pelo tempo necessário para o atendimento da solicitação e para o cumprimento de obrigações legais, e então eliminados.</p>

        <h2>Cookies</h2>
        <p>Este site não utiliza cookies de rastreamento ou de publicidade.</p>

        <h2>Direitos do titular</h2>
        <p>O titular pode solicitar, a qualquer momento, a confirmação do tratamento, o acesso, a correção ou a eliminação dos seus dados, pelo e-mail <a href="mailto:{EMAIL}" data-email>{EMAIL}</a>.</p>

        <p><em>Última atualização: outubro de 2026.</em></p>
      </div>
    </section>
  </main>
""" + footer("index.html")


def main():
    paginas = {"index.html": pagina_inicial(), "obrigado.html": pagina_obrigado(),
               "politica-de-privacidade.html": pagina_privacidade()}
    for p in PAGINAS:
        paginas[p["arquivo"]] = pagina_servico(p)
    for nome, html in paginas.items():
        (RAIZ / nome).write_text(html, encoding="utf-8")
        print("gerado:", nome)


if __name__ == "__main__":
    main()
