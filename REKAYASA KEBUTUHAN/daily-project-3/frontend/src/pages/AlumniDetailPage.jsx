import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import StatusBadge from '../components/StatusBadge'
import { getAlumni } from '../services/alumniService'

function AlumniDetailPage() {
  const { id } = useParams()
  const [alumni, setAlumni] = useState(null)

  useEffect(() => {
    const run = async () => {
      const data = await getAlumni(id)
      setAlumni(data)
    }

    run()
  }, [id])

  if (!alumni) {
    return <p className="text-sm text-slate-500">Loading alumni detail...</p>
  }

  return (
    <section>
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-2xl font-bold text-slate-900">Alumni Detail</h2>
        <Link to="/alumni" className="rounded border border-slate-300 px-3 py-1 text-sm font-semibold text-slate-700">Back</Link>
      </div>

      <div className="rounded-2xl bg-white p-6 shadow-panel">
        <div className="grid gap-3 text-sm text-slate-700 md:grid-cols-2">
          <p><span className="font-semibold">Name:</span> {alumni.name}</p>
          <p><span className="font-semibold">NIM:</span> {alumni.nim}</p>
          <p><span className="font-semibold">Program:</span> {alumni.study_program}</p>
          <p><span className="font-semibold">Graduation Year:</span> {alumni.graduation_year}</p>
          <p><span className="font-semibold">Email:</span> {alumni.email || '-'}</p>
          <p><span className="font-semibold">Tracking Status:</span> <StatusBadge status={alumni.tracking_status} /></p>
        </div>

        <div className="mt-6">
          <h3 className="text-lg font-semibold text-slate-900">Tracking History</h3>
          <div className="mt-3 overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-left text-slate-500">
                  <th className="px-2 py-2">Source</th>
                  <th className="px-2 py-2">Title</th>
                  <th className="px-2 py-2">Score</th>
                  <th className="px-2 py-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {(alumni.tracking_results || []).map((item) => (
                  <tr key={item.id} className="border-b border-slate-100">
                    <td className="px-2 py-2">{item.source}</td>
                    <td className="px-2 py-2">{item.title}</td>
                    <td className="px-2 py-2">{item.confidence_score}</td>
                    <td className="px-2 py-2"><StatusBadge status={item.status} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  )
}

export default AlumniDetailPage
