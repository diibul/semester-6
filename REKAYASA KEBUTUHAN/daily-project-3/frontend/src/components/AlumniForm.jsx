function AlumniForm({ form, onChange, onSubmit, submitLabel = 'Simpan', loading = false }) {
  return (
    <form onSubmit={onSubmit} className="space-y-5 rounded-2xl bg-white p-6 shadow-panel">
      <div className="grid gap-5 md:grid-cols-2">
        <label className="block text-sm font-medium text-slate-700">
          Nama
          <input
            name="name"
            value={form.name}
            onChange={onChange}
            required
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-brand-500 focus:outline-none"
          />
        </label>

        <label className="block text-sm font-medium text-slate-700">
          NIM
          <input
            name="nim"
            value={form.nim}
            onChange={onChange}
            required
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-brand-500 focus:outline-none"
          />
        </label>

        <label className="block text-sm font-medium text-slate-700">
          Program Studi
          <input
            name="study_program"
            value={form.study_program}
            onChange={onChange}
            required
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-brand-500 focus:outline-none"
          />
        </label>

        <label className="block text-sm font-medium text-slate-700">
          Tahun Lulus
          <input
            name="graduation_year"
            type="number"
            value={form.graduation_year}
            onChange={onChange}
            required
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-brand-500 focus:outline-none"
          />
        </label>

        <label className="block text-sm font-medium text-slate-700 md:col-span-2">
          Email
          <input
            name="email"
            type="email"
            value={form.email}
            onChange={onChange}
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-brand-500 focus:outline-none"
          />
        </label>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="rounded-lg bg-brand-600 px-5 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-70"
      >
        {loading ? 'Menyimpan...' : submitLabel}
      </button>
    </form>
  )
}

export default AlumniForm
