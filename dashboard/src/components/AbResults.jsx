export default function AbResults({ data }) {
  const seen = new Set()
  const deduped = data.filter(row => {
    const key = `${row.domain}-${row.metric}`
    if (seen.has(key)) return false
    seen.add(key)
    return true
  })

  const grouped = deduped.reduce((acc, row) => {
    if (!acc[row.domain]) acc[row.domain] = []
    acc[row.domain].push(row)
    return acc
  }, {})

  return (
    <div style={{ background:'var(--bg-panel)', border:'0.5px solid var(--border)', borderRadius:8, padding:16 }}>
      <div style={{ fontSize:10, letterSpacing:'0.12em', color:'var(--text-muted)', textTransform:'uppercase', marginBottom:16 }}>
        A/B test results — statistical comparison
      </div>
      <div style={{ display:'grid', gridTemplateColumns:'repeat(3, minmax(0,1fr))', gap:12 }}>
        {Object.entries(grouped).map(([domain, rows]) => (
          <div key={domain} style={{ background:'var(--bg-card)', border:'0.5px solid var(--border)', borderRadius:6, padding:12 }}>
            <div style={{ fontSize:10, letterSpacing:'0.08em', color:'var(--text-muted)', textTransform:'uppercase', marginBottom:12 }}>
              {domain.replace(/_/g, ' ')}
            </div>
            {rows.map(row => {
              const tie = row.winner?.includes('tie')
              const aWins = row.winner === row.model_a
              return (
                <div key={row.metric} style={{ marginBottom:10, paddingBottom:10, borderBottom:'0.5px solid var(--border)' }}>
                  <div style={{ display:'flex', justifyContent:'space-between', marginBottom:6 }}>
                    <span style={{ fontFamily:'var(--font-mono)', fontSize:11, color:'var(--text-secondary)' }}>{row.metric}</span>
                    <span style={{ fontFamily:'var(--font-mono)', fontSize:10, color: tie ? 'var(--text-muted)' : 'var(--green)', background: tie ? 'transparent' : 'var(--green-bg)', padding:'2px 6px', borderRadius:3 }}>
                      {tie ? 'tie' : row.winner?.split('-').slice(0,1).join('')}
                    </span>
                  </div>
                  <div style={{ display:'flex', justifyContent:'space-between', fontFamily:'var(--font-mono)', fontSize:10, color:'var(--text-muted)' }}>
                    <span style={{ color: aWins ? 'var(--green)' : 'inherit' }}>A: {row.model_a_score?.toFixed(3)}</span>
                    <span style={{ color:'var(--border)' }}>·</span>
                    <span style={{ color: !aWins && !tie ? 'var(--green)' : 'inherit' }}>B: {row.model_b_score?.toFixed(3)}</span>
                    <span>p={row.p_value?.toFixed(3)}</span>
                  </div>
                </div>
              )
            })}
          </div>
        ))}
      </div>
    </div>
  )
}
