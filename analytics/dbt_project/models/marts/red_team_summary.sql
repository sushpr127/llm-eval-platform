with red_team_data as (
    select * from {{ ref('stg_red_team_runs') }}
)

select
    model_name,
    attack_type,
    count(*)                                            as total_attacks,
    sum(case when attack_succeeded then 1 else 0 end)   as successful_attacks,
    round(
        sum(case when attack_succeeded then 1 else 0 end)::numeric / count(*), 4
    )                                                   as attack_success_rate,
    round(avg(safety_score)::numeric, 4)                as avg_safety_score
from red_team_data
group by model_name, attack_type
order by model_name, attack_success_rate desc
