const getPill = (rate) => {
  if (rate === 0) return { bg:'var(--green-bg)', color:'var(--green)', border:'0.5px solid var(--green-border)', label:'robust' }
  if (rate <= 0.2) return { bg:'var(--amber-bg)', color:'var(--amber)', border:'0.5px solid #5a4a2d', label:'partial' }
  return { bg:'var(--red-bg)', color:'var(--red)', border:'0.5px solid var(--red-border)', label:'vulnerable' }
}

export default function RedTeamPanel({ data }) {
  const attackTypes = [...new Set(data.map(d => d.attack_type))]
  const models = [...new Set(data.map(d => d.model_name))]

  const getRate = (model, attack) =>
    data.find(d => d.model_name === model && d.attack_type === attack)?.attack_success_rate ?? 0

  const safetyByModel = models.map(m => {
    const rows = data.filter(d => d.model_name === m)
    const avg = rows.reduce((s, r) => s + (r.attack_success_rate || 0), 0) / (rows.length || 1)
    return { model: m, safety: 1 - avg }
  })

  return (
    <div style={{ background:'var(--bg-panel)', border:'0.5px solid var(--border)', borderRadius:8, padding:16 }}>
      <div style={{ fontSize:10, letterSpacing:'0.12em', color:'var(--text-muted)', textTransform:'uppercase', marginBottom:16 }}>
        Red team results
      </div>

      <div style={{ display:'grid', gridTemplateColumns:`140px repeat(${models.length}, 1fr)`, gap:6, marginBottom:12 }}>
        <div />
        {models.map(m => (
          <div key={m} style={{ fontFamily:'var(--font-mono)', fontSize:10, color:'var(--text-muted)', textAlign:'center' }}>
            {m.split('-').slice(0,2).join('-')}
          </div>
        ))}

        {attackTypes.map(attack => (
          <>
            <div key={attack} style={{ fontFamily:'var(--font-mono)', fontSize:11, color:'var(--text-secondary)', display:'flex', alignItems:'center' }}>
              {attack.replace('_', ' ')}
            </div>
            {models.map(m => {
              const rate = getRate(m, attack)
              const pill = getPill(rate)
              return (
                <div key={m} style={{ display:'flex', justifyContent:'center' }}>
                  <span style={{ background:pill.bg, color:pill.color, border:pill.border, fontFamily:'var(--font-mono)', fontSize:10, padding:'3px 8px', borderRadius:3 }}>
                    {(rate * 100).toFixed(0)}%
                  </span>
                </div>
              )
            })}
          </>
        ))}
      </div>

      <div style={{ borderTop:'0.5px solid var(--border)', paddingTop:12, marginTop:8 }}>
        <div style={{ fontSize:10, letterSpacing:'0.12em', color:'var(--text-muted)', textTransform:'uppercase', marginBottom:10 }}>
          Overall safety score
        </div>
        {safetyByModel.map((item, i) => (
          <div key={item.model} style={{ display:'flex', alignItems:'center', gap:10, marginBottom:8 }}>
            <div style={{ fontFamily:'var(--font-mono)', fontSize:11, color:'var(--text-secondary)', width:120 }}>
              {item.model.split('-').slice(0,2).join('-')}
            </div>
            <div style={{ flex:1, height:3, background:'var(--border)', borderRadius:2 }}>
              <div style={{ height:3, borderRadius:2, background: i === 0 ? 'var(--green)' : 'var(--amber)', width:`${item.safety * 100}%`, transition:'width 1s ease' }} />
            </div>
            <div style={{ fontFamily:'var(--font-mono)', fontSize:12, color: i === 0 ? 'var(--green)' : 'var(--amber)', width:36, textAlign:'right' }}>
              {item.safety.toFixed(2)}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
