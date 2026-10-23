create extension if not exists "pgcrypto";

create table if not exists parcelas (
  id uuid primary key default gen_random_uuid(),
  nombre text not null,
  cultivo_actual text,
  hectareas numeric default 1,
  latitud numeric default -9.93,
  longitud numeric default -76.24,
  created_at timestamptz default now()
);

create table if not exists lecturas_iot (
  id uuid primary key default gen_random_uuid(),
  dispositivo text not null,
  parcela_id uuid references parcelas(id) on delete set null,
  humedad_suelo numeric,
  temperatura numeric,
  ph numeric,
  created_at timestamptz default now()
);

-- Para pruebas: desactivar RLS (en producción define políticas)
alter table parcelas disable row level security;
alter table lecturas_iot disable row level security;
