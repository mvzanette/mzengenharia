-- ============================================================
-- Controle de ART – estrutura do banco (Supabase)
-- Cole tudo no SQL Editor do Supabase e clique em "Run" (uma única vez).
-- ============================================================

-- ARTs cadastradas
create table if not exists public.arts (
  id              uuid primary key default gen_random_uuid(),
  user_id         uuid not null default auth.uid() references auth.users (id) on delete cascade,
  numero          text not null,
  crea            text not null default 'MG' check (crea in ('MG', 'RJ', 'SP', 'Outro')),
  tipo            text,
  forma           text,
  contratante     text,
  contratante_doc text,
  proprietario    text,
  local           text,
  endereco        text,
  contrato        text,
  valor           numeric(14, 2),
  taxa            numeric(10, 2),
  celebrado       date,
  inicio          date,
  fim             date,
  registrada      date,
  atividades      jsonb not null default '[]'::jsonb,
  tos             text[] not null default '{}',
  observacao      text,
  chave           text,
  tipo_servico    text check (tipo_servico in ('pontual', 'continuo')),
  baixa_data      date,
  baixa_motivo    text check (baixa_motivo in ('conclusao', 'interrupcao')),
  anterior_id     uuid references public.arts (id) on delete set null,
  pdf_path        text,
  notas           text,
  criado_em       timestamptz not null default now(),
  atualizado_em   timestamptz not null default now(),
  unique (user_id, numero)
);

create index if not exists arts_fim_idx on public.arts (user_id, fim) where baixa_data is null;

-- Alertas: um registro por ART e marco (30 dias, 7 dias, no dia, semanas de atraso)
create table if not exists public.alertas (
  id               uuid primary key default gen_random_uuid(),
  user_id          uuid not null default auth.uid() references auth.users (id) on delete cascade,
  art_id           uuid not null references public.arts (id) on delete cascade,
  marco            text not null,
  mensagem         text not null,
  criado_em        timestamptz not null default now(),
  lido_em          timestamptz,
  email_enviado_em timestamptz,
  unique (art_id, marco)
);

-- Atualiza "atualizado_em" a cada alteração
create or replace function public.tocar_atualizado_em() returns trigger
language plpgsql as $$
begin
  new.atualizado_em := now();
  return new;
end $$;

drop trigger if exists arts_atualizado_em on public.arts;
create trigger arts_atualizado_em before update on public.arts
  for each row execute function public.tocar_atualizado_em();

-- ------------------------------------------------------------
-- Segurança: cada usuário só enxerga e altera os próprios dados
-- ------------------------------------------------------------
alter table public.arts enable row level security;
alter table public.alertas enable row level security;

drop policy if exists "arts do proprio usuario" on public.arts;
create policy "arts do proprio usuario" on public.arts
  for all to authenticated
  using (user_id = auth.uid())
  with check (user_id = auth.uid());

drop policy if exists "alertas do proprio usuario" on public.alertas;
create policy "alertas do proprio usuario" on public.alertas
  for all to authenticated
  using (user_id = auth.uid())
  with check (user_id = auth.uid());

-- ------------------------------------------------------------
-- PDFs das ARTs: armazenamento privado, uma pasta por usuário
-- ------------------------------------------------------------
insert into storage.buckets (id, name, public)
values ('arts', 'arts', false)
on conflict (id) do nothing;

drop policy if exists "pdfs do proprio usuario - ler" on storage.objects;
create policy "pdfs do proprio usuario - ler" on storage.objects
  for select to authenticated
  using (bucket_id = 'arts' and (storage.foldername(name))[1] = auth.uid()::text);

drop policy if exists "pdfs do proprio usuario - enviar" on storage.objects;
create policy "pdfs do proprio usuario - enviar" on storage.objects
  for insert to authenticated
  with check (bucket_id = 'arts' and (storage.foldername(name))[1] = auth.uid()::text);

drop policy if exists "pdfs do proprio usuario - atualizar" on storage.objects;
create policy "pdfs do proprio usuario - atualizar" on storage.objects
  for update to authenticated
  using (bucket_id = 'arts' and (storage.foldername(name))[1] = auth.uid()::text);

drop policy if exists "pdfs do proprio usuario - apagar" on storage.objects;
create policy "pdfs do proprio usuario - apagar" on storage.objects
  for delete to authenticated
  using (bucket_id = 'arts' and (storage.foldername(name))[1] = auth.uid()::text);
