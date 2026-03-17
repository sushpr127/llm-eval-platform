with source as (
    select * from eval_runs
),

cleaned as (
    select
        id,
        run_id,
        model_name,
        domain,
        question,
        answer,
        ground_truth,
        faithfulness,
        answer_relevancy,
        hallucination_rate,
        toxicity,
        safety_score,
        latency_ms,
        created_at,
        date_trunc('day', created_at) as eval_date
    from source
    where faithfulness is not null
      and answer_relevancy is not null
)

select * from cleaned
