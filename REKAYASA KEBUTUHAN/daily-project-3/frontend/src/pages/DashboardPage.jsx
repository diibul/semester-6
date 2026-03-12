import { useEffect, useMemo, useState } from 'react'
import StatCard from '../components/StatCard'
import { fetchDashboard } from '../services/dashboardService'

function DashboardPage() {
  const [stats, setStats] = useState({
    total_alumni: 0,
    tracked_alumni: 0,
    teridentifikasi: 0,
    perlu_verifikasi: 0,
    belum_ditemukan: 0,
  })

  useEffect(() => {
    const run = async () => {
      try {
        const data = await fetchDashboard()
        setStats(data)
      } catch (error) {
        // Keep fallback values for dashboard when API is not ready.
      }
    }

    run()
  }, [])

  const chartData = useMemo(
    () => [
      { label: 'Teridentifikasi', value: stats.teridentifikasi, color: 'bg-emerald-500' },
      { label: 'Perlu Verifikasi', value: stats.perlu_verifikasi, color: 'bg-amber-500' },
      { label: 'Belum Ditemukan', value: stats.belum_ditemukan, color: 'bg-rose-500' },
    ],
    [stats]
  )

  const maxValue = Math.max(...chartData.map((item) => item.value), 1)

  return (
    <section>
      <h2 className="text-2xl font-bold text-slate-900">Dashboard</h2>
      <p className="mt-1 text-sm text-slate-500">Ringkasan status tracking alumni dari berbagai sumber publik.</p>

      <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Total Alumni" value={stats.total_alumni} />
        <StatCard title="Tracked Alumni" value={stats.tracked_alumni} accent="from-cyan-500 to-blue-700" />
        <StatCard title="Verification Needed" value={stats.perlu_verifikasi} accent="from-amber-500 to-orange-600" />
        <StatCard title="Not Found" value={stats.belum_ditemukan} accent="from-rose-500 to-rose-700" />
      </div>

      <div className="mt-8 rounded-2xl bg-white p-6 shadow-panel">
        <h3 className="text-lg font-semibold text-slate-900">Status Distribution</h3>
        <div className="mt-5 space-y-4">
          {chartData.map((item) => (
            <div key={item.label}>
              <div className="mb-1 flex justify-between text-sm text-slate-600">
                <span>{item.label}</span>
                <span>{item.value}</span>
              </div>
              <div className="h-2 rounded-full bg-slate-100">
                <div
                  className={`h-2 rounded-full ${item.color}`}
                  style={{ width: `${Math.max((item.value / maxValue) * 100, 6)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default DashboardPage
