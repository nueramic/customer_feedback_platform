drop view ai_responses_tobe_parse;

create or replace view ai_responses_tobe_parse as
with a as
         ( select *
                , row_number() over
                 (partition by id_feedback order by (json_gpt_resp_content is null) desc nulls last, feedback.dtime_uploaded desc nulls last) as rn
                , count(1) over (partition by id_store)                                                                                       as cnt_store
           from prod.feedback
                    left join prod.ai_responses using (id_feedback) )
select id_feedback
from a
where rn = 1
  and json_gpt_resp_content is null
order by cnt_store desc;

select *
from ai_responses_tobe_parse
where id_feedback = '017ea695822e17e75f73e9b4072323dd84d981acaf8e3f7dace323b25e200c49';
