const STATUS_STYLE = {
  'Belum Dilacak': 'bg-slate-100 text-slate-700',
  Teridentifikasi: 'bg-emerald-100 text-emerald-700',
  'Perlu Verifikasi': 'bg-amber-100 text-amber-700',
  'Belum Ditemukan': 'bg-rose-100 text-rose-700',
}

function StatusBadge({ status }) {
  return (
    <span className={`rounded-full px-3 py-1 text-xs font-semibold ${STATUS_STYLE[status] || 'bg-slate-100 text-slate-700'}`}>
      {status}
    </span>
  )
}

export default StatusBadge
