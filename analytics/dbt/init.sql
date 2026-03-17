CREATE TABLE IF NOT EXISTS eval_runs (
    id SERIAL PRIMARY KEY,
    run_id UUID NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    domain VARCHAR(100) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    contexts TEXT[],
    ground_truth TEXT,
    faithfulness FLOAT,
    answer_relevancy FLOAT,
    context_precision FLOAT,
    hallucination_rate FLOAT,
    toxicity FLOAT,
    safety_score FLOAT,
    latency_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS red_team_runs (
    id SERIAL PRIMARY KEY,
    run_id UUID NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    attack_type VARCHAR(100) NOT NULL,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    attack_succeeded BOOLEAN,
    safety_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ab_test_runs (
    id SERIAL PRIMARY KEY,
    test_id UUID NOT NULL,
    model_a VARCHAR(100) NOT NULL,
    model_b VARCHAR(100) NOT NULL,
    domain VARCHAR(100) NOT NULL,
    metric VARCHAR(100) NOT NULL,
    model_a_score FLOAT,
    model_b_score FLOAT,
    winner VARCHAR(100),
    p_value FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
