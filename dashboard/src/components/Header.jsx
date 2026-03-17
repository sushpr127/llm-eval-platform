export default function Header({ stats }) {
  return (
    <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start', marginBottom:28, borderBottom:'0.5px solid var(--border)', paddingBottom:20 }}>
      <div>
        <div style={{ fontSize:10, letterSpacing:'0.15em', color:'var(--text-muted)', textTransform:'uppercase', marginBottom:6 }}>
          LLM Evaluation Platform
        </div>
        <div style={{ fontSize:28, fontWeight:800, color:'var(--text-primary)', letterSpacing:'-0.02em' }}>
          Model Observatory
        </div>
      </div>
      <div style={{ textAlign:'right' }}>
        <div style={{ background:'var(--green-bg)', color:'var(--green)', fontFamily:'var(--font-mono)', fontSize:10, padding:'4px 12px', borderRadius:4, border:'0.5px solid var(--green-border)', display:'inline-block' }}>
          ● Live
        </div>
        <div style={{ fontFamily:'var(--font-mono)', fontSize:11, color:'var(--text-muted)', marginTop:8 }}>
          {stats?.total_evals} evals · {stats?.total_attacks} attacks
        </div>
      </div>
    </div>
  )
}
