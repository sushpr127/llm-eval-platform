with eval_data as (
    select * from {{ ref('stg_eval_runs') }}
),

leaderboard as (
    select
        model_name,
        count(*)                                        as total_evals,
        round(avg(faithfulness)::numeric, 4)            as avg_faithfulness,
        round(avg(answer_relevancy)::numeric, 4)        as avg_answer_relevancy,
        round(avg(hallucination_rate)::numeric, 4)      as avg_hallucination_rate,
        round(avg(toxicity)::numeric, 4)                as avg_toxicity,
        round(avg(latency_ms)::numeric, 0)              as avg_latency_ms,
        min(created_at)                                 as first_eval_at,
        max(created_at)                                 as last_eval_at
    from eval_data
    group by model_name
)

select
    model_name,
    total_evals,
    avg_faithfulness,
    avg_answer_relevancy,
    avg_hallucination_rate,
    avg_toxicity,
    avg_latency_ms,
    first_eval_at,
    last_eval_at,
    round(
        (avg_faithfulness + avg_answer_relevancy + (1 - avg_hallucination_rate) + (1 - avg_toxicity)) / 4
    , 4) as composite_score
from leaderboard
order by composite_score desc
