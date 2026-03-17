import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Tooltip, Legend } from 'recharts'

export default function DomainBreakdown({ data }) {
  const domains = [...new Set(data.map(d => d.domain))]
  const models = [...new Set(data.map(d => d.model_name))]

  const radarData = domains.map(domain => {
    const entry = { domain: domain.replace(/_/g, ' ') }
    models.forEach(m => {
      const row = data.find(d => d.model_name === m && d.domain === domain)
      entry[m.split('-')[0]] = row ? parseFloat((row.avg_faithfulness * 100).toFixed(1)) : 0
    })
    return entry
  })

  return (
    <div style={{ background:'var(--bg-panel)', border:'0.5px solid var(--border)', borderRadius:8, padding:16, marginBottom:12 }}>
      <div style={{ fontSize:10, letterSpacing:'0.12em', color:'var(--text-muted)', textTransform:'uppercase', marginBottom:16 }}>
        Domain breakdown — faithfulness by domain
      </div>
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:16 }}>
        <div style={{ height:240 }}>
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={radarData} margin={{ top:10, right:30, bottom:10, left:30 }}>
              <PolarGrid stroke="#2a2b2e" />
              <PolarAngleAxis dataKey="domain" tick={{ fontFamily:'DM Mono', fontSize:10, fill:'#6b6a64' }} />
              <PolarRadiusAxis angle={90} domain={[95, 100]} tick={{ fontFamily:'DM Mono', fontSize:9, fill:'#3a3b3e' }} tickCount={3} />
              {models.map((m, i) => (
                <Radar key={m} name={m.split('-').slice(0,2).join('-')} dataKey={m.split('-')[0]} stroke={i === 0 ? '#4ade80' : '#fbbf24'} fill={i === 0 ? '#4ade80' : '#fbbf24'} fillOpacity={0.1} strokeWidth={1.5} />
              ))}
              <Tooltip contentStyle={{ background:'#1a1c20', border:'0.5px solid #2a2b2e', borderRadius:6, fontFamily:'DM Mono', fontSize:11 }} formatter={(val) => [`${val}%`]} />
              <Legend wrapperStyle={{ fontFamily:'DM Mono', fontSize:10, color:'#6b6a64' }} />
            </RadarChart>
          </ResponsiveContainer>
        </div>
        <div style={{ display:'grid', gridTemplateColumns:'repeat(3, minmax(0,1fr))', gap:8, alignContent:'start' }}>
          {domains.map(domain => (
            <div key={domain} style={{ background:'var(--bg-card)', border:'0.5px solid var(--border)', borderRadius:6, padding:12 }}>
              <div style={{ fontSize:10, letterSpacing:'0.08em', color:'var(--text-muted)', textTransform:'uppercase', marginBottom:10 }}>
                {domain.replace(/_/g, ' ')}
              </div>
              {models.map(m => {
                const row = data.find(d => d.model_name === m && d.domain === domain)
                return (
                  <div key={m} style={{ display:'flex', justifyContent:'space-between', fontFamily:'var(--font-mono)', fontSize:11, marginBottom:4 }}>
                    <span style={{ color:'var(--text-muted)' }}>{m.split('-')[0]}</span>
                    <span style={{ color:'var(--text-primary)' }}>{row?.avg_faithfulness?.toFixed(3) || '—'}</span>
                  </div>
                )
              })}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
