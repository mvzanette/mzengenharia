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
| `area-restrita.html`, `area/` | **Área restrita – Controle de ART** (ver seção própria abaixo). |
| `supabase/schema.sql` | Estrutura do banco de dados da área restrita. |
| `ferramentas/alertas-art.mjs`, `.github/workflows/alertas-art.yml` | Rotina diária que envia os alertas de ART por e-mail. |

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
2. Nome do repositório: `mzengenharia` (*Settings → General → Repository name → Rename*). O nome do repositório é o que aparece no endereço.
3. No GitHub: **Settings → Pages → Build and deployment**.
4. Em *Source*, escolha **Deploy from a branch**, selecione a branch principal do repositório (hoje `claude/exciting-curie-vngk32`) e a pasta `/ (root)`. Clique em **Save**.
5. Em 1 ou 2 minutos o site estará no ar em `https://mvzanette.github.io/mzengenharia/`.

A cada alteração enviada para essa branch, o GitHub publica a nova versão sozinho (leva 1 ou 2 minutos).

**Endereço mais curto:** renomeie o repositório para `mvzanette.github.io` (o site passa a ficar em `https://mvzanette.github.io/`) ou use um domínio próprio (passo 3).

### Ver o site no computador, sem publicar

1. No GitHub: **Code → Download ZIP** e descompacte.
2. Dê dois cliques em `index.html`: o site abre no navegador como um arquivo comum.

Nesse modo o formulário não envia e a área restrita não abre (o navegador bloqueia os módulos dela em arquivos locais). Para testar tudo, use o endereço do GitHub Pages.

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

---

# Área restrita – Controle de ART

Endereço: `area-restrita.html` (link discreto no rodapé do site; não aparece no Google).

## O que faz

- **Importa PDFs com leitura automática:** ART individual do CREA-MG e do CREA-RJ, e o relatório "ARTs (Todas)" do CREA-MG (várias ARTs de uma vez). O CREA-SP ainda não tem leitor (falta um PDF de exemplo); por enquanto, cadastre manualmente.
- **Painel:** ARTs ativas, que vencem em até 30 dias, vencidas sem baixa e baixadas, com busca e filtros por CREA e situação.
- **Alertas** na plataforma (sino) e por e-mail, com base no **fim previsto** da ART:
  - 30 dias antes: "Daqui a 30 dias a ART nº … do cliente … vencerá (fim previsto em …)."
  - 7 dias antes e no dia;
  - depois de vencida, uma vez por semana até a baixa ser registrada.
- **Ajuda na decisão:** para serviço pontual (laudo, vistoria, projeto), pergunta se foi concluído; para serviço contínuo (PMOC, manutenção), pergunta se o contrato foi renovado. Indica se é caso de dar baixa, de emitir nova ART ou de ajustar a data.
- **Registro de baixa**, vínculo entre a ART anterior e a nova (renovação) e **"Copiar dados para nova ART"**, para colar no portal do CREA.
- **Exportação em planilha (CSV)**, que também serve como cópia de segurança.

A emissão e a baixa da ART continuam sendo feitas no portal de cada CREA. Nenhum dos três CREAs oferece integração oficial para sistemas externos; por isso a plataforma trabalha com os PDFs.

## Modo demonstração

Enquanto `area/config-area.js` estiver vazio, a área restrita funciona em **modo demonstração**: os dados ficam só no navegador em uso e os e-mails não são enviados. Serve para testar a importação e as telas.

## Ativar de verdade (uma única vez, ~20 minutos)

### 1. Supabase (banco de dados e login – gratuito)

1. Crie a conta em [supabase.com](https://supabase.com) e um projeto (região **South America (São Paulo)**). Guarde a senha do banco.
2. Em **SQL Editor**, cole todo o conteúdo de `supabase/schema.sql` e clique em **Run**.
3. Em **Authentication → Users → Add user**, crie o seu usuário (e-mail e senha, marcando *Auto Confirm User*).
4. Em **Authentication → Sign In / Providers**, **desative "Allow new users to sign up"**: assim ninguém mais consegue criar conta.
5. Em **Authentication → URL Configuration**, coloque o endereço do site em *Site URL* (usado no link de "Esqueci a senha").
6. Em **Project Settings → API**, copie:
   - **Project URL** e a chave **anon public** → cole em `area/config-area.js`;
   - a chave **service_role** → **não** coloque no site; ela vai só para o GitHub (passo 3).

### 2. Resend (envio dos e-mails – gratuito até 3.000/mês)

1. Crie a conta em [resend.com](https://resend.com) com o e-mail que vai receber os alertas.
2. Em **API Keys**, crie uma chave e copie.
   Sem domínio próprio, o Resend envia apenas para o e-mail da própria conta, o que basta para os alertas.

### 3. GitHub (rotina diária)

Em **Settings → Secrets and variables → Actions**:

- aba **Secrets** → *New repository secret*: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `RESEND_API_KEY` e `ALERTA_EMAIL` (o e-mail que recebe os alertas);
- aba **Variables** → `ALERTA_LINK` com o endereço da área restrita (vai no e-mail).

Para testar na hora: **Actions → Alertas de ART → Run workflow**. Depois disso a rotina roda todo dia às 8h (Brasília).

Observações:

- A rotina agendada roda a partir da branch principal do repositório.
- Em repositório público, o GitHub pausa rotinas agendadas depois de 60 dias sem nenhuma alteração no repositório. Ele avisa por e-mail antes; basta clicar em **Enable workflow** em *Actions*.
- A execução diária também mantém o projeto do Supabase ativo (o plano gratuito pausa projetos parados por uma semana).

## Segurança e privacidade

- O código do site é público, mas os dados não: ficam no Supabase, protegidos pelo login e por regras de acesso no banco (cada usuário só enxerga os próprios registros). Os PDFs ficam em armazenamento privado.
- **Nunca** coloque PDFs de ART, relatórios ou planilhas exportadas dentro do repositório (o `.gitignore` já bloqueia `.pdf`, `.csv` e `.xlsx`).
- A chave `service_role` dá acesso total ao banco: guarde-a só nos *Secrets* do GitHub.

## Testes locais

```
node ferramentas/alertas-art.mjs --teste   # simula o e-mail do dia com ARTs fictícias
```
