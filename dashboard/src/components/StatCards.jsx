const Card = ({ label, value, sub, color }) => (
  <div style={{ background:'var(--bg-panel)', border:'0.5px solid var(--border)', borderRadius:8, padding:'14px 16px' }}>
    <div style={{ fontSize:10, letterSpacing:'0.1em', color:'var(--text-muted)', textTransform:'uppercase', marginBottom:10 }}>{label}</div>
    <div style={{ fontFamily:'var(--font-mono)', fontSize:26, fontWeight:500, color: color || 'var(--text-primary)', lineHeight:1 }}>{value}</div>
    {sub && <div style={{ fontFamily:'var(--font-mono)', fontSize:11, color:'var(--text-muted)', marginTop:6 }}>{sub}</div>}
  </div>
)

export default function StatCards({ stats, leaderboard }) {
  const topFaith = leaderboard.reduce((best, m) => m.avg_faithfulness > (best?.avg_faithfulness || 0) ? m : best, null)
  const safest = leaderboard.reduce((best, m) => (m.avg_hallucination_rate ?? 1) < (best?.avg_hallucination_rate ?? 1) ? m : best, null)
  const resistance = stats ? `${(stats.overall_attack_resistance * 100).toFixed(0)}%` : '—'

  return (
    <div style={{ display:'grid', gridTemplateColumns:'repeat(4, minmax(0,1fr))', gap:10, marginBottom:12 }}>
      <Card label="Top faithfulness" value={topFaith ? topFaith.avg_faithfulness.toFixed(3) : '—'} sub={topFaith?.model_name.split('-').slice(0,2).join('-')} color="var(--green)" />
      <Card label="Hallucination rate" value={`${((safest?.avg_hallucination_rate || 0) * 100).toFixed(1)}%`} sub="best model" color="var(--green)" />
      <Card label="Total evals run" value={stats?.total_evals || '—'} sub={`${stats?.models_evaluated} models`} />
      <Card label="Attack resistance" value={resistance} sub={`${stats?.total_attacks} attacks total`} color="var(--amber)" />
    </div>
  )
}
