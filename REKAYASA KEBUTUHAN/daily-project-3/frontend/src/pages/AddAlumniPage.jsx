import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import AlumniForm from '../components/AlumniForm'
import { createAlumni } from '../services/alumniService'

const defaultForm = {
  name: '',
  nim: '',
  study_program: '',
  graduation_year: '',
  email: '',
}

function AddAlumniPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState(defaultForm)
  const [loading, setLoading] = useState(false)

  const handleChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)

    try {
      await createAlumni(form)
      navigate('/alumni')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section>
      <h2 className="mb-4 text-2xl font-bold text-slate-900">Add Alumni</h2>
      <AlumniForm form={form} onChange={handleChange} onSubmit={handleSubmit} submitLabel="Create Alumni" loading={loading} />
    </section>
  )
}

export default AddAlumniPage
