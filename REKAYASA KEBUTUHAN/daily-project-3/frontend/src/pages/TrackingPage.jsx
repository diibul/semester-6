import { useEffect, useState } from 'react'
import StatusBadge from '../components/StatusBadge'
import { fetchAlumni, trackAlumni } from '../services/alumniService'

function TrackingPage() {
  const [alumni, setAlumni] = useState([])
  const [selectedId, setSelectedId] = useState('')
  const [simulation, setSimulation] = useState(null)

  useEffect(() => {
    const run = async () => {
      const data = await fetchAlumni({ page: 1, search: '' })
      setAlumni(data.data)
      if (data.data.length > 0) {
        setSelectedId(String(data.data[0].id))
      }
    }

    run()
  }, [])

  const handleTrack = async () => {
    if (!selectedId) {
      return
    }

    const data = await trackAlumni(selectedId)
    setSimulation(data)
  }

  return (
    <section>
      <h2 className="text-2xl font-bold text-slate-900">Tracking Simulation</h2>
      <p className="mt-1 text-sm text-slate-500">Jalankan simulasi pelacakan alumni dari multiple public sources.</p>

      <div className="mt-5 rounded-2xl bg-white p-6 shadow-panel">
        <div className="flex flex-wrap gap-3">
          <select
            value={selectedId}
            onChange={(event) => setSelectedId(event.target.value)}
            className="w-full min-w-0 rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none sm:w-auto sm:min-w-64"
          >
            {alumni.map((item) => (
              <option key={item.id} value={item.id}>{item.name} ({item.nim})</option>
            ))}
          </select>

          <button
            type="button"
            onClick={handleTrack}
            className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
          >
            Track Alumni
          </button>
        </div>

        {simulation ? (
          <div className="mt-6">
            <h3 className="text-lg font-semibold text-slate-900">Generated Search Queries</h3>
            <ul className="mt-2 list-disc pl-5 text-sm text-slate-700">
              {simulation.queries.map((query) => (
                <li key={query}>{query}</li>
              ))}
            </ul>

            <h3 className="mt-5 text-lg font-semibold text-slate-900">Candidate Results</h3>
            <div className="mt-3 space-y-3">
              {simulation.results.map((result) => (
                <div key={result.id} className="rounded-xl border border-slate-200 p-4">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <p className="text-sm font-semibold text-slate-800">{result.source}</p>
                    <StatusBadge status={result.status} />
                  </div>
                  <p className="mt-2 text-sm font-medium text-slate-700">{result.title}</p>
                  <p className="mt-1 text-sm text-slate-500">{result.description}</p>
                  <p className="mt-2 text-xs font-semibold text-brand-700">Confidence: {result.confidence_score}%</p>
                </div>
              ))}
            </div>
          </div>
        ) : null}
      </div>
    </section>
  )
}

export default TrackingPage
