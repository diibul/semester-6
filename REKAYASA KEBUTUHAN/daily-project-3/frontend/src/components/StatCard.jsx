function StatCard({ title, value, accent = 'from-brand-500 to-brand-700' }) {
  return (
    <div className="rounded-2xl bg-white p-5 shadow-panel">
      <p className="text-sm font-medium text-slate-500">{title}</p>
      <div className="mt-3 flex items-end justify-between">
        <p className="text-3xl font-bold text-slate-800">{value}</p>
        <div className={`h-2 w-16 rounded-full bg-gradient-to-r ${accent}`} />
      </div>
    </div>
  )
}

export default StatCard
