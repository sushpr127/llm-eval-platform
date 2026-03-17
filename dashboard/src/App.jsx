import { useEffect, useState } from 'react'
import { fetchStats, fetchLeaderboard, fetchDomainBreakdown, fetchRedTeam, fetchAbResults } from './api'
import Header from './components/Header'
import StatCards from './components/StatCards'
import Leaderboard from './components/Leaderboard'
import RedTeamPanel from './components/RedTeamPanel'
import DomainBreakdown from './components/DomainBreakdown'
import AbResults from './components/AbResults'
import './index.css'

export default function App() {
  const [stats, setStats] = useState(null)
  const [leaderboard, setLeaderboard] = useState([])
  const [domains, setDomains] = useState([])
  const [redTeam, setRedTeam] = useState([])
  const [abResults, setAbResults] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetchStats(),
      fetchLeaderboard(),
      fetchDomainBreakdown(),
      fetchRedTeam(),
      fetchAbResults(),
    ]).then(([s, l, d, r, a]) => {
      setStats(s)
      setLeaderboard(l)
      setDomains(d)
      setRedTeam(r)
      setAbResults(a)
      setLoading(false)
    })
  }, [])

  if (loading) return (
    <div style={{ display:'flex', alignItems:'center', justifyContent:'center', height:'100vh', fontFamily:'var(--font-mono)', color:'var(--text-muted)', fontSize:13 }}>
      initializing observatory...
    </div>
  )

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: '32px 24px' }}>
      <Header stats={stats} />
      <StatCards stats={stats} leaderboard={leaderboard} />
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:12, marginBottom:12 }}>
        <Leaderboard data={leaderboard} />
        <RedTeamPanel data={redTeam} />
      </div>
      <DomainBreakdown data={domains} />
      <AbResults data={abResults} />
    </div>
  )
}
