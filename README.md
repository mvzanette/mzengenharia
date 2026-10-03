# Marcos Zanette — Engenharia Mecânica

Site institucional estático (HTML + CSS + JS, sem servidor) para captação de clientes: laudo NR-12 de equipamentos móveis, gestão e eletrificação de frotas, manutenção industrial, laudos NR-13, PMOC e ART. O formulário de proposta chega por e-mail.

Custo: **R$ 0** (hospedagem no GitHub Pages + formulário pelo FormSubmit).

## Arquivos

| Arquivo | O que é |
| --- | --- |
| `config.js` | **Dados de contato** (e-mail, WhatsApp, CREA). Edite só este arquivo para trocar contatos. |
| `ferramentas/gerar_site.py` | **Todos os textos das páginas.** Gera os arquivos `.html` (ver "Alterar textos"). |
| `index.html`, `laudo-nr12.html`, `laudo-nr13.html`, `pmoc.html`, `obrigado.html`, `politica-de-privacidade.html` | Páginas geradas pelo script acima. Não edite à mão. |
| `tos-mecanica.js` | Tabela de Obras e Serviços (TOS) do CREA, área 16 (Mecânica), usada no formulário. |
| `styles.css` | Visual do site (grafite e amarelo industrial). |
| `main.js` | Menu do celular e formulário. Não precisa mexer. |
| `img/` | Fotos do site (ver "Fotos"). |

## Fotos

Enquanto uma foto não existir, o site mostra um espaço reservado com um ícone. Para colocar a foto, salve o arquivo **com o nome exato abaixo** na pasta indicada. Uma mesma foto pode ser usada em mais de um lugar (basta copiar com outro nome).

| Arquivo | Onde aparece | Formato ideal |
| --- | --- | --- |
| `img/hero.jpg` | Topo da página (fica em preto e branco automaticamente) | Horizontal, 1920 px ou mais |
| `img/nr12.jpg` | Seção "Laudo NR-12 para equipamentos móveis" | Vertical ou quadrada |
| `img/eletrificacao.jpg` | Seção "Eletrificação de frotas" | Vertical ou quadrada |
| `img/perfil.jpg` | Card "Responsável técnico" | Vertical ou quadrada |
| `img/equipamentos/escavadeira.jpg`, `pa-carregadeira.jpg`, `trator-esteiras.jpg`, `motoniveladora.jpg`, `rolo-compactador.jpg`, `retroescavadeira.jpg`, `minicarregadeira.jpg`, `caminhao-munck.jpg`, `caminhao-basculante.jpg`, `caminhao-pipa.jpg`, `caminhao-comboio.jpg`, `veiculos-apoio.jpg` | Grade "Equipamentos atendidos" | Horizontal (4:3) |
| `img/servicos/laudo-nr12.jpg`, `laudo-nr13.jpg`, `laudos-mecanicos.jpg`, `planos-manutencao.jpg`, `consultoria-frotas.jpg`, `insumos.jpg`, `eletrificacao.jpg`, `manutencao-industrial.jpg`, `pmoc.jpg`, `ar-condicionado.jpg`, `art.jpg` | Cards de "Serviços" | Horizontal (16:10) |

Use apenas fotos com direito de uso (próprias, com autorização, ou de bancos de imagem com licença comercial), de preferência sem logos de fabricantes ou placas em destaque.

**Nunca publique** laudos, fotos de laudos, números de série, placas ou códigos internos de clientes. A seção "Experiência" traz apenas descrições do tipo de trabalho, sem nomes de clientes.

## Alterar textos

Os textos ficam em `ferramentas/gerar_site.py`. Depois de editar, gere as páginas de novo, na pasta do site:

```
python3 ferramentas/gerar_site.py
```

Cabeçalho, formulário e rodapé são iguais em todas as páginas e saem do mesmo lugar no script.

## Formulário de proposta

- **Lista de serviços** (`SERVICOS_FORM` no script): cada opção leva o código TOS do CREA correspondente, que chega no e-mail junto com o pedido.
- **"Outro serviço – escolher na lista do CREA"** abre a lista completa da área de Mecânica em cascata (subárea → obra/serviço → complemento), a partir de `tos-mecanica.js` (Árvore TOS do CREA-RJ).
- Obrigatórios: nome, e-mail, WhatsApp, cidade, estado e serviço.

## 1. Publicar de graça no GitHub Pages

1. O repositório precisa ser **público** (no plano gratuito do GitHub).
2. No GitHub: **Settings → Pages → Build and deployment**.
3. Em *Source*, escolha **Deploy from a branch**, selecione a branch e a pasta `/ (root)`. Clique em **Save**.
4. Em 1 ou 2 minutos o site estará no ar em `https://mvzanette.github.io/vectraengenharia/`.

**Para tirar o "vectraengenharia" do endereço:** renomeie o repositório (*Settings → General → Repository name*) para `mvzanette.github.io` (o site passa a ficar em `https://mvzanette.github.io/`) ou use um domínio próprio (passo 3).

## 2. Ativar o formulário (uma única vez)

O formulário usa o [FormSubmit](https://formsubmit.co), gratuito e sem cadastro.

1. Com o site no ar, envie o formulário uma vez.
2. O FormSubmit envia um e-mail pedindo **confirmação**. Clique em *Activate*.
3. A partir daí, cada solicitação chega no e-mail em formato de tabela, com o assunto `Solicitação de proposta: <serviço> – <nome>`. *Responder* responde direto ao cliente, que também recebe uma confirmação automática.
4. *(Opcional)* No e-mail de ativação vem um código aleatório. Cole em `formsubmitId` no `config.js` para esconder o e-mail do código do site.

**Se começar a chegar spam:** em `ferramentas/gerar_site.py`, troque `name="_captcha" value="false"` por `value="true"` e gere as páginas de novo.

## 3. Domínio próprio (recomendado, ~R$ 40/ano)

1. Registre o domínio em [registro.br](https://registro.br) (ex.: `marcoszanette.eng.br` ou `.com.br`).
2. No GitHub: **Settings → Pages → Custom domain**, digite o domínio e salve.
3. No registro.br, configure o DNS conforme a [documentação do GitHub Pages](https://docs.github.com/pt/pages/configuring-a-custom-domain-for-your-github-pages-site).
4. Marque **Enforce HTTPS**.

## 4. Para aparecer no Google

- **Perfil da Empresa no Google** (gratuito): [google.com/business](https://www.google.com/business/), com o link do site.
- **Google Search Console** (gratuito): [search.google.com/search-console](https://search.google.com/search-console), para indexar o site mais rápido.
- Link do site no LinkedIn, no WhatsApp Business e na assinatura de e-mail.
