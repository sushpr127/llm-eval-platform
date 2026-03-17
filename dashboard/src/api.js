import axios from 'axios'
const BASE = 'http://localhost:8000'
export const fetchStats = () => axios.get(`${BASE}/api/stats`).then(r => r.data)
export const fetchLeaderboard = () => axios.get(`${BASE}/api/leaderboard`).then(r => r.data)
export const fetchDomainBreakdown = () => axios.get(`${BASE}/api/domain-breakdown`).then(r => r.data)
export const fetchRedTeam = () => axios.get(`${BASE}/api/red-team`).then(r => r.data)
export const fetchAbResults = () => axios.get(`${BASE}/api/ab-results`).then(r => r.data)
