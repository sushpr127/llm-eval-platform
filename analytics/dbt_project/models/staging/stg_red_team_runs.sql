with source as (
    select * from red_team_runs
),

cleaned as (
    select
        id,
        run_id,
        model_name,
        attack_type,
        prompt,
        response,
        attack_succeeded,
        safety_score,
        created_at
    from source
)

select * from cleaned
