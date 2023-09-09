create or replace function f_ai_parse_responses() returns void
    volatile
    language plpgsql as
$$
begin
    truncate ai_parsed_responses;

    insert into ai_parsed_responses
    select id_feedback
         , (json_gpt_resp_content -> 'общее впечатление' ->> 'score')::numeric
         , (json_gpt_resp_content -> 'общее впечатление' ->> 'summary')
         , (json_gpt_resp_content -> 'цены и ценники' ->> 'score')::numeric
         , (json_gpt_resp_content -> 'цены и ценники' ->> 'summary')
         , (json_gpt_resp_content -> 'программа лояльности' ->> 'score')::numeric
         , (json_gpt_resp_content -> 'программа лояльности' ->> 'summary')
         , (json_gpt_resp_content -> 'свежесть продуктов' ->> 'score')::numeric
         , (json_gpt_resp_content -> 'свежесть продуктов' ->> 'summary')
         , (json_gpt_resp_content -> 'работа персонала' ->> 'score')::numeric
         , (json_gpt_resp_content -> 'работа персонала' ->> 'summary')
         , (json_gpt_resp_content -> 'ассортимент' ->> 'score')::numeric
         , (json_gpt_resp_content -> 'ассортимент' ->> 'summary')
         , dtime_updated
    from ai_responses;
end;
$$;

select f_ai_parse_responses();


create view v_ai_parsed_responses as
select id_feedback                                                            as id_feedback
     , (json_gpt_resp_content -> 'общее впечатление' ->> 'score')::numeric    as score_overall
     , (json_gpt_resp_content -> 'общее впечатление' ->> 'summary')           as txt_overall
     , (json_gpt_resp_content -> 'цены и ценники' ->> 'score')::numeric       as score_product_range
     , (json_gpt_resp_content -> 'цены и ценники' ->> 'summary')              as txt_product_range
     , (json_gpt_resp_content -> 'программа лояльности' ->> 'score')::numeric as score_staff
     , (json_gpt_resp_content -> 'программа лояльности' ->> 'summary')        as txt_staff
     , (json_gpt_resp_content -> 'свежесть продуктов' ->> 'score')::numeric   as score_prices
     , (json_gpt_resp_content -> 'свежесть продуктов' ->> 'summary')          as txt_prices
     , (json_gpt_resp_content -> 'работа персонала' ->> 'score')::numeric     as score_freshness
     , (json_gpt_resp_content -> 'работа персонала' ->> 'summary')            as txt_freshness
     , (json_gpt_resp_content -> 'ассортимент' ->> 'score')::numeric          as score_bonus_program
     , (json_gpt_resp_content -> 'ассортимент' ->> 'summary')                 as txt_bonus_program
     , dtime_updated                                                          as dtime_updated
from ai_responses;