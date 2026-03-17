import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const COLORS = ['#4ade80', '#fbbf24']

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div style={{ background:'#1a1c20', border:'0.5px solid #2a2b2e', borderRadius:6, padding:'8px 12px', fontFamily:'var(--font-mono)', fontSize:11 }}>
      <div style={{ color:'#9e9c94', marginBottom:4 }}>{label}</div>
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.color }}>{p.name}: {p.value?.toFixed(3)}</div>
      ))}
    </div>
  )
}

export default function Leaderboard({ data }) {
  const chartData = data.map((m, i) => ({
    name: m.model_name.split('-').slice(0, 2).join('-'),
    faithfulness: m.avg_faithfulness,
    relevancy: m.avg_answer_relevancy,
    composite: m.composite_score,
    color: COLORS[i % COLORS.length]
  }))

  return (
    <div style={{ background:'var(--bg-panel)', border:'0.5px solid var(--border)', borderRadius:8, padding:16 }}>
      <div style={{ fontSize:10, letterSpacing:'0.12em', color:'var(--text-muted)', textTransform:'uppercase', marginBottom:16 }}>
        Model leaderboard
      </div>

      {data.map((m, i) => (
        <div key={m.model_name} style={{ marginBottom:16 }}>
          <div style={{ display:'flex', justifyContent:'space-between', marginBottom:6 }}>
            <span style={{ fontFamily:'var(--font-mono)', fontSize:11, color:'var(--text-secondary)' }}>
              {m.model_name}
            </span>
            <span style={{ fontFamily:'var(--font-mono)', fontSize:11, color: COLORS[i % COLORS.length] }}>
              {m.composite_score?.toFixed(4)}
            </span>
          </div>
          {[
            { label:'faithfulness', val: m.avg_faithfulness },
            { label:'relevancy', val: m.avg_answer_relevancy },
          ].map(({ label, val }) => (
            <div key={label} style={{ display:'flex', alignItems:'center', gap:10, marginBottom:5 }}>
              <div style={{ fontFamily:'var(--font-mono)', fontSize:10, color:'var(--text-muted)', width:80 }}>{label}</div>
              <div style={{ flex:1, height:3, background:'var(--border)', borderRadius:2 }}>
                <div style={{ height:3, borderRadius:2, background: COLORS[i % COLORS.length], width:`${(val || 0) * 100}%`, transition:'width 1s ease' }} />
              </div>
              <div style={{ fontFamily:'var(--font-mono)', fontSize:11, color:'var(--text-primary)', width:40, textAlign:'right' }}>
                {val?.toFixed(3)}
              </div>
            </div>
          ))}
        </div>
      ))}

      <div style={{ marginTop:16, height:140 }}>
        <div style={{ fontSize:10, letterSpacing:'0.12em', color:'var(--text-muted)', textTransform:'uppercase', marginBottom:10 }}>
          Composite score
        </div>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} barSize={40}>
            <XAxis dataKey="name" tick={{ fontFamily:'DM Mono', fontSize:10, fill:'#6b6a64' }} axisLine={false} tickLine={false} />
            <YAxis domain={[0.9, 1]} tick={{ fontFamily:'DM Mono', fontSize:10, fill:'#6b6a64' }} axisLine={false} tickLine={false} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="composite" radius={[4,4,0,0]}>
              {chartData.map((entry, i) => <Cell key={i} fill={entry.color} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
