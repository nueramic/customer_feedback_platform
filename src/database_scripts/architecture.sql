create schema if not exists analytic;

drop schema prod cascade;

create schema if not exists prod;

alter role itmoml set search_path to prod;

drop table retail_feedback.prod.user_info cascade;
create table retail_feedback.prod.user_info
(
    id_user      text,
    id_platform  text,
    txt_userlink text,
    txt_username text
);
drop table retail_feedback.prod.platform;
create table retail_feedback.prod.platform
(
    id_platform        text,
    txt_name_platform  text,
    txt_link_main_page text
);
drop table retail_feedback.prod.company cascade;
create table retail_feedback.prod.company
(
    id_parent_company text,
    txt_name_company  text
);

drop table retail_feedback.prod.store cascade;
create table retail_feedback.prod.store
(
    id_store                   text,
    id_parent_company          text,
    txt_address                text,
    txt_name                   text,
    num_longitude              float4,
    num_latitude               float4,
    num_phone_number           text,
    txt_web_link               text,
    flg_handicapped_accessible bool
);
drop table retail_feedback.prod.raw_json;
create table retail_feedback.prod.raw_json
(
    id_feedback text,
    txt_json    json
);
drop table retail_feedback.prod.feedback cascade;
create table retail_feedback.prod.feedback
(
    id_feedback    text,
    id_user        text,
    id_platform    text,
    id_store       text,
    txt_feedback   text,
    cnt_likes      bigint,
    cnt_dislikes   bigint,
    dt_feedback    text,
    num_rate       float4,
    num_max_rate   float4,
    dtime_uploaded timestamp
);

drop table retail_feedback.prod.ai_responses;
create table retail_feedback.prod.ai_responses
(
    id_feedback           text,
    json_gpt_resp_content json,
    dtime_updated         timestamp
);

drop table retail_feedback.prod.ai_parsed_responses;
create table retail_feedback.prod.ai_parsed_responses
(
    id_feedback         text,
    score_overall       numeric,
    txt_overall         text,
    score_product_range numeric,
    txt_product_range   text,
    score_staff         numeric,
    txt_staff           text,
    score_prices        numeric,
    txt_prices          text,
    score_freshness     numeric,
    txt_freshness       text,
    score_bonus_program numeric,
    txt_bonus_program   text,
    dtime_updated       timestamp
);