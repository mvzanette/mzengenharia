// Aplica os dados de config.js na página. Não é preciso editar este arquivo.
document.addEventListener("DOMContentLoaded", () => {
  const zap =
    "https://wa.me/" + CONFIG.whatsapp + "?text=" + encodeURIComponent(CONFIG.whatsappTexto);

  document.querySelectorAll("[data-whatsapp]").forEach((a) => (a.href = zap));
  document.querySelectorAll("[data-config]").forEach((el) => {
    el.textContent = CONFIG[el.dataset.config];
  });
  document.querySelectorAll("[data-email]").forEach((a) => {
    a.href = "mailto:" + CONFIG.email;
    a.textContent = CONFIG.email;
  });
  document.querySelectorAll("[data-tel]").forEach((a) => {
    a.href = "tel:+" + CONFIG.whatsapp;
    a.textContent = CONFIG.telefoneExibicao;
  });

  const ano = document.getElementById("ano");
  if (ano) ano.textContent = new Date().getFullYear();

  const form = document.getElementById("form-orcamento");
  if (!form) return;

  form.action = "https://formsubmit.co/" + (CONFIG.formsubmitId || CONFIG.email);
  form.elements._next.value = new URL("obrigado.html", location.href).href;

  // Assunto do e-mail com o serviço e o nome, para facilitar a triagem na caixa de entrada.
  form.addEventListener("submit", () => {
    const servico = form.elements["Serviço"].value;
    const nome = form.elements["Nome"].value;
    form.elements._subject.value = "Orçamento ART: " + servico + " – " + nome;
    form.querySelector("button[type=submit]").textContent = "Enviando…";
  });
});
