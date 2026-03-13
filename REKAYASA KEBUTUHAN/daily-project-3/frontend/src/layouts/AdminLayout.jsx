import { useState } from 'react'
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
  const [mobileNavOpen, setMobileNavOpen] = useState(false)

  const handleLogout = async () => {
    try {
      await logout()
    } catch {
      // Intentionally swallow API logout errors and continue client logout.
    } finally {
      localStorage.removeItem('auth_token')
      navigate('/login', { replace: true })
    }
  }

  const handleNavClick = () => {
    setMobileNavOpen(false)
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <div className="border-b border-slate-200 bg-white px-4 py-3 shadow-sm md:hidden">
        <div className="flex items-center justify-between">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand-700">Alumni Admin</p>
          <button
            type="button"
            onClick={() => setMobileNavOpen((prev) => !prev)}
            className="rounded-lg border border-slate-300 px-3 py-1 text-sm font-semibold text-slate-700"
          >
            Menu
          </button>
        </div>
      </div>

      {mobileNavOpen ? (
        <button
          type="button"
          aria-label="Close menu"
          onClick={() => setMobileNavOpen(false)}
          className="fixed inset-0 z-30 bg-slate-950/50 md:hidden"
        />
      ) : null}

      <div className="flex min-h-screen">
        <aside
          className={`fixed inset-y-0 left-0 z-40 w-72 transform bg-slate-900 px-6 py-7 text-slate-100 transition-transform duration-200 md:static md:w-64 md:translate-x-0 ${
            mobileNavOpen ? 'translate-x-0' : '-translate-x-full'
          }`}
        >
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-brand-300">Rekayasa Kebutuhan</p>
          <h1 className="mt-2 text-2xl font-bold leading-tight">Alumni Tracking Admin</h1>

          <nav className="mt-8 space-y-2">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                onClick={handleNavClick}
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

        <main className="w-full flex-1 p-4 sm:p-6 md:p-10">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default AdminLayout
