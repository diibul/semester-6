import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import AlumniForm from '../components/AlumniForm'
import { getAlumni, updateAlumni } from '../services/alumniService'

const defaultForm = {
  name: '',
  nim: '',
  study_program: '',
  graduation_year: '',
  email: '',
}

function EditAlumniPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [form, setForm] = useState(defaultForm)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const run = async () => {
      const data = await getAlumni(id)
      setForm({
        name: data.name || '',
        nim: data.nim || '',
        study_program: data.study_program || '',
        graduation_year: data.graduation_year || '',
        email: data.email || '',
      })
    }

    run()
  }, [id])

  const handleChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)

    try {
      await updateAlumni(id, form)
      navigate('/alumni')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section>
      <h2 className="mb-4 text-2xl font-bold text-slate-900">Edit Alumni</h2>
      <AlumniForm form={form} onChange={handleChange} onSubmit={handleSubmit} submitLabel="Update Alumni" loading={loading} />
    </section>
  )
}

export default EditAlumniPage
