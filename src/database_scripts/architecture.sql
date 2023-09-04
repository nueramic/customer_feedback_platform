create schema if not exists analytic;

drop schema prod cascade;

create schema if not exists prod;

alter role itmoml set search_path to prod;


create table retail_feedback.prod.user_info
(
    id_user     serial primary key,
    id_platform text,
    txt_link    text
);

create table retail_feedback.prod.platform
(
    id_platform        serial primary key,
    txt_name_platform  text,
    txt_link_main_page text
);

create table retail_feedback.prod.company
(
    id_parent_company serial primary key,
    txt_name_company  text
);


create table retail_feedback.prod.store
(
    id_store                   serial primary key,
    id_parent_company          bigint references company (id_parent_company),
    txt_address                text,
    txt_name                   text,
    num_longitude              float4,
    num_latitude               float4,
    num_phone_number           int,
    text_web_link              text,
    flg_handicapped_accessible bool
);

create table retail_feedback.prod.feedback
(
    id_feedback  serial primary key,
    id_user      bigint references user_info (id_user),
    id_platform  bigint references platform (id_platform),
    id_store     bigint references store (id_store),
    txt_feedback text,
    cnt_likes    bigint,
    cnt_dislikes bigint,
    dt_feedback  date,
    num_rate     float4,
    num_max_rate float4
);
