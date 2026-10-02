# Marcos Zanette — site de captação de clientes

Site estático (HTML + CSS + JS, sem servidor) para captar clientes que precisam de **ART de engenheiro mecânico** em Juiz de Fora e região. Tem apresentação dos serviços, "como funciona", sobre, perguntas frequentes e um **formulário de orçamento que chega no seu e-mail**.

Custo: **R$ 0** (hospedagem no GitHub Pages + formulário pelo FormSubmit).

## Arquivos

| Arquivo        | O que é                                                     |
| -------------- | ----------------------------------------------------------- |
| `config.js`    | **Seus dados** (e-mail, WhatsApp, CREA, nome, região). Edite só este arquivo. |
| `index.html`   | Página principal (textos dos serviços, FAQ, formulário).    |
| `obrigado.html`| Página exibida depois que o cliente envia o formulário.     |
| `styles.css`   | Visual do site (cores, fontes, layout).                     |
| `main.js`      | Aplica os dados de `config.js` na página. Não precisa mexer. |

## 1. Seus dados

Já estão preenchidos em `config.js` (e-mail, WhatsApp, nome, CREA e região). Para mudar algum, edite esse arquivo.

Também vale revisar em `index.html`:

- a lista de **serviços**: remova o que você não faz e ajuste o que quiser
- o prazo "Resposta em até 1 dia útil", se não for o seu caso

## 2. Publique de graça no GitHub Pages

1. O repositório precisa ser **público** (no plano gratuito do GitHub).
2. No GitHub: **Settings → Pages → Build and deployment**.
3. Em *Source*, escolha **Deploy from a branch**, selecione a branch (ex.: `main`) e a pasta `/ (root)`. Clique em **Save**.
4. Em 1 ou 2 minutos o site estará no ar em `https://mvzanette.github.io/vectraengenharia/`.

**Para tirar o "vectraengenharia" do endereço**, escolha uma das opções:

- **Grátis:** renomeie o repositório (*Settings → General → Repository name*) para `mvzanette.github.io`. O site passa a ficar em `https://mvzanette.github.io/`.
- **Domínio próprio:** veja o passo 4 abaixo. Aí o nome do repositório não aparece.

## 3. Ative o formulário (uma única vez)

O formulário usa o [FormSubmit](https://formsubmit.co), que é gratuito e não precisa de cadastro.

1. Com o site no ar, preencha e envie o formulário você mesmo.
2. Você vai receber um e-mail do FormSubmit pedindo **confirmação**. Clique em *Activate*.
3. Pronto: a partir daí, toda solicitação chega no seu e-mail, em formato de tabela, com o assunto `Orçamento ART: <serviço> – <nome>`. Clicar em *Responder* já responde direto ao cliente.
4. *(Opcional)* No e-mail de ativação, o FormSubmit envia um código aleatório. Cole em `formsubmitId` no `config.js` para que seu e-mail não fique visível no código do site.

O cliente também recebe uma resposta automática confirmando o recebimento (texto editável no campo `_autoresponse` do `index.html`).

**Se começar a chegar spam:** em `index.html`, troque `name="_captcha" value="false"` por `value="true"`.

## 4. Domínio próprio (recomendado, ~R$ 40/ano)

Um endereço como `marcoszanette.com.br` ou `marcoszanette.eng.br` passa muito mais confiança.

1. Registre o domínio em [registro.br](https://registro.br).
2. No GitHub: **Settings → Pages → Custom domain**, digite o domínio e salve.
3. No registro.br, configure o DNS conforme a [documentação do GitHub Pages](https://docs.github.com/pt/pages/configuring-a-custom-domain-for-your-github-pages-site).
4. Marque **Enforce HTTPS**.

## 5. Para aparecer para os clientes

- **Perfil da Empresa no Google** (gratuito): cadastre em [google.com/business](https://www.google.com/business/). É o que faz você aparecer em buscas como "ART engenheiro mecânico Juiz de Fora" e no Google Maps. Coloque o link do site lá.
- **Google Search Console** (gratuito): cadastre o site em [search.google.com/search-console](https://search.google.com/search-console) para o Google indexá-lo mais rápido.
- Coloque o link do site na bio do Instagram, no WhatsApp Business e na assinatura de e-mail.

## Ver o site no computador

Abra o `index.html` no navegador. O envio do formulário só funciona com o site publicado (passo 2).
