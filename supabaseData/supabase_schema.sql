create extension if not exists pgcrypto;

create table if not exists public.datasets (
    id uuid primary key,
    name text not null,
    version text not null,
    description text,
    labels_csv_name text,
    num_crops integer default 0,
    num_full_disk_images integer default 0,
    created_at timestamptz not null default now(),
    unique(name, version)
);

create table if not exists public.full_disk_images (
    id uuid primary key,
    dataset_id uuid not null references public.datasets(id) on delete cascade,
    file_name text not null,
    storage_bucket text not null,
    storage_path text not null,
    date_obs date,
    width integer,
    height integer,
    num_crops integer default 0,
    noaa_list jsonb,
    metadata_json jsonb,
    created_at timestamptz not null default now(),
    unique(dataset_id, file_name),
    unique(storage_bucket, storage_path)
);

create table if not exists public.sunspot_crops (
    id uuid primary key,
    dataset_id uuid not null references public.datasets(id) on delete cascade,
    full_disk_image_id uuid not null references public.full_disk_images(id) on delete cascade,
    crop_filename text not null,
    storage_bucket text not null,
    storage_path text not null,
    full_disk_filename text,
    crop_index integer,
    date_obs date,
    z_class text,
    p_class text,
    c_class text,
    mcintosh_full text,
    pred_z text,
    pred_p text,
    pred_c text,
    pred_mcintosh_full text,
    noaa bigint,
    lat double precision,
    lon double precision,
    carrington_lo double precision,
    extension_ll double precision,
    area double precision,
    mag_class text,
    num_spots_srs integer,
    orig_w integer,
    orig_h integer,
    square_size integer,
    yolo_conf double precision,
    created_at timestamptz not null default now(),
    unique(dataset_id, crop_filename),
    unique(storage_bucket, storage_path),
    unique(full_disk_image_id, crop_index)
);

create index if not exists idx_full_disk_images_dataset_id
    on public.full_disk_images(dataset_id);

create index if not exists idx_full_disk_images_date_obs
    on public.full_disk_images(date_obs);

create index if not exists idx_sunspot_crops_dataset_id
    on public.sunspot_crops(dataset_id);

create index if not exists idx_sunspot_crops_full_disk_image_id
    on public.sunspot_crops(full_disk_image_id);

create index if not exists idx_sunspot_crops_date_obs
    on public.sunspot_crops(date_obs);

create index if not exists idx_sunspot_crops_noaa
    on public.sunspot_crops(noaa);

create index if not exists idx_sunspot_crops_mcintosh_full
    on public.sunspot_crops(mcintosh_full);