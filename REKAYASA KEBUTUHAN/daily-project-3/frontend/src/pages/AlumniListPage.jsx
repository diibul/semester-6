import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import StatusBadge from '../components/StatusBadge'
import { deleteAlumni, fetchAlumni, trackAlumni } from '../services/alumniService'

function AlumniListPage() {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const [items, setItems] = useState([])
  const [meta, setMeta] = useState({ current_page: 1, last_page: 1 })

  const loadData = async (page = 1, searchTerm = search) => {
    const data = await fetchAlumni({ page, search: searchTerm })
    setItems(data.data)
    setMeta({ current_page: data.current_page, last_page: data.last_page })
  }

  useEffect(() => {
    const initialize = async () => {
      const data = await fetchAlumni({ page: 1, search: '' })
      setItems(data.data)
      setMeta({ current_page: data.current_page, last_page: data.last_page })
    }

    initialize()
  }, [])

  const handleDelete = async (id) => {
    if (!window.confirm('Hapus data alumni ini?')) {
      return
    }

    await deleteAlumni(id)
    loadData(meta.current_page)
  }

  const handleTrack = async (id) => {
    await trackAlumni(id)
    loadData(meta.current_page)
    navigate('/results')
  }

  return (
    <section>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Alumni Data</h2>
          <p className="text-sm text-slate-500">Manajemen data alumni untuk proses pelacakan.</p>
        </div>
        <Link to="/alumni/add" className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700">
          + Add Alumni
        </Link>
      </div>

      <div className="mt-5 rounded-2xl bg-white p-4 shadow-panel">
        <div className="mb-4 flex flex-wrap items-center gap-3">
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search name / nim / program"
            className="w-full max-w-sm rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
          />
          <button
            type="button"
            onClick={() => loadData(1, search)}
            className="rounded-lg border border-brand-300 px-4 py-2 text-sm font-semibold text-brand-700 hover:bg-brand-50"
          >
            Search
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-left text-slate-500">
                <th className="px-3 py-2">Name</th>
                <th className="px-3 py-2">NIM</th>
                <th className="px-3 py-2">Program</th>
                <th className="px-3 py-2">Graduation Year</th>
                <th className="px-3 py-2">Tracking Status</th>
                <th className="px-3 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {items.map((alumni) => (
                <tr key={alumni.id} className="border-b border-slate-100">
                  <td className="px-3 py-3 font-medium text-slate-800">{alumni.name}</td>
                  <td className="px-3 py-3">{alumni.nim}</td>
                  <td className="px-3 py-3">{alumni.study_program}</td>
                  <td className="px-3 py-3">{alumni.graduation_year}</td>
                  <td className="px-3 py-3"><StatusBadge status={alumni.tracking_status} /></td>
                  <td className="px-3 py-3">
                    <div className="flex flex-wrap gap-2">
                      <Link to={`/alumni/${alumni.id}`} className="rounded border border-slate-300 px-2 py-1 text-xs font-semibold text-slate-700">View</Link>
                      <Link to={`/alumni/${alumni.id}/edit`} className="rounded border border-brand-300 px-2 py-1 text-xs font-semibold text-brand-700">Edit</Link>
                      <button type="button" onClick={() => handleDelete(alumni.id)} className="rounded border border-rose-300 px-2 py-1 text-xs font-semibold text-rose-700">Delete</button>
                      <button type="button" onClick={() => handleTrack(alumni.id)} className="rounded border border-emerald-300 px-2 py-1 text-xs font-semibold text-emerald-700">Track</button>
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
            onClick={() => loadData(meta.current_page - 1)}
            className="rounded border border-slate-300 px-3 py-1 text-xs font-semibold disabled:opacity-50"
          >
            Prev
          </button>
          <button
            type="button"
            disabled={meta.current_page >= meta.last_page}
            onClick={() => loadData(meta.current_page + 1)}
            className="rounded border border-slate-300 px-3 py-1 text-xs font-semibold disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>
    </section>
  )
}

export default AlumniListPage
