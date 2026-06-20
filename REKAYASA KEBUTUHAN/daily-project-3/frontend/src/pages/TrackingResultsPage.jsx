import { useEffect, useState } from 'react'
import StatusBadge from '../components/StatusBadge'
import { fetchResults, verifyResult } from '../services/resultService'

function TrackingResultsPage() {
  const [results, setResults] = useState([])
  const [page, setPage] = useState(1)
  const [meta, setMeta] = useState({ current_page: 1, last_page: 1 })

  const loadResults = async (targetPage = 1) => {
    const data = await fetchResults({ page: targetPage })
    setResults(data.data)
    setMeta({ current_page: data.current_page, last_page: data.last_page })
    setPage(targetPage)
  }

  useEffect(() => {
    const initialize = async () => {
      const data = await fetchResults({ page: 1 })
      setResults(data.data)
      setMeta({ current_page: data.current_page, last_page: data.last_page })
      setPage(1)
    }

    initialize()
  }, [])

  const handleVerify = async (id, action) => {
    await verifyResult(id, action)
    loadResults(page)
  }

  return (
    <section>
      <h2 className="text-2xl font-bold text-slate-900">Tracking Results</h2>
      <p className="mt-1 text-sm text-slate-500">Riwayat hasil pelacakan dan proses verifikasi admin.</p>

      <div className="mt-5 rounded-2xl bg-white p-4 shadow-panel">
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-left text-slate-500">
                <th className="px-3 py-2">Source</th>
                <th className="px-3 py-2">Summary</th>
                <th className="px-3 py-2">Status</th>
                <th className="px-3 py-2">Tracking Date</th>
                <th className="px-3 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {results.map((item) => (
                <tr key={item.id} className="border-b border-slate-100">
                  <td className="px-3 py-3">{item.source}</td>
                  <td className="px-3 py-3">
                    <p className="font-medium text-slate-800">{item.title}</p>
                    <p className="text-xs text-slate-500">{item.description}</p>
                  </td>
                  <td className="px-3 py-3"><StatusBadge status={item.status} /></td>
                  <td className="px-3 py-3">{item.tracked_at ? new Date(item.tracked_at).toLocaleString() : '-'}</td>
                  <td className="px-3 py-3">
                    <div className="flex flex-wrap gap-2">
                      <button type="button" onClick={() => handleVerify(item.id, 'confirm')} className="rounded border border-emerald-300 px-2 py-1 text-xs font-semibold text-emerald-700">Confirm</button>
                      <button type="button" onClick={() => handleVerify(item.id, 'uncertain')} className="rounded border border-amber-300 px-2 py-1 text-xs font-semibold text-amber-700">Uncertain</button>
                      <button type="button" onClick={() => handleVerify(item.id, 'invalid')} className="rounded border border-rose-300 px-2 py-1 text-xs font-semibold text-rose-700">Invalid</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-4 flex gap-2">
          <button
            type="button"
            disabled={meta.current_page <= 1}
            onClick={() => loadResults(meta.current_page - 1)}
            className="rounded border border-slate-300 px-3 py-1 text-xs font-semibold disabled:opacity-50"
          >
            Prev
          </button>
          <button
            type="button"
            disabled={meta.current_page >= meta.last_page}
            onClick={() => loadResults(meta.current_page + 1)}
            className="rounded border border-slate-300 px-3 py-1 text-xs font-semibold disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>
    </section>
  )
}

export default TrackingResultsPage
