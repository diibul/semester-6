import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { logout } from '../services/authService'

const navItems = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Alumni', to: '/alumni' },
  { label: 'Tracking', to: '/tracking' },
  { label: 'Results', to: '/results' },
]

function AdminLayout() {
  const navigate = useNavigate()

  const handleLogout = async () => {
    try {
      await logout()
    } catch (error) {
      // Intentionally swallow API logout errors and continue client logout.
    } finally {
      localStorage.removeItem('auth_token')
      navigate('/login', { replace: true })
    }
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <div className="flex min-h-screen">
        <aside className="w-64 bg-slate-900 px-6 py-7 text-slate-100">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-brand-300">Rekayasa Kebutuhan</p>
          <h1 className="mt-2 text-2xl font-bold leading-tight">Alumni Tracking Admin</h1>

          <nav className="mt-8 space-y-2">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `block rounded-lg px-4 py-2 text-sm font-medium transition ${
                    isActive ? 'bg-brand-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>

          <button
            type="button"
            onClick={handleLogout}
            className="mt-8 w-full rounded-lg border border-slate-700 px-4 py-2 text-sm font-semibold text-slate-100 hover:bg-slate-800"
          >
            Logout
          </button>
        </aside>

        <main className="flex-1 p-6 md:p-10">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default AdminLayout
