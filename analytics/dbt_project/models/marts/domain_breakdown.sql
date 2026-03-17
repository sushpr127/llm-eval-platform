with eval_data as (
    select * from {{ ref('stg_eval_runs') }}
)

select
    model_name,
    domain,
    count(*)                                    as total_evals,
    round(avg(faithfulness)::numeric, 4)        as avg_faithfulness,
    round(avg(answer_relevancy)::numeric, 4)    as avg_answer_relevancy,
    round(avg(hallucination_rate)::numeric, 4)  as avg_hallucination_rate,
    round(avg(latency_ms)::numeric, 0)          as avg_latency_ms
from eval_data
group by model_name, domain
order by model_name, domain
