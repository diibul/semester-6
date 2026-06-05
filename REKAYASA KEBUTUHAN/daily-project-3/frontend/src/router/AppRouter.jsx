import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import AdminLayout from '../layouts/AdminLayout'
import AddAlumniPage from '../pages/AddAlumniPage'
import AlumniDetailPage from '../pages/AlumniDetailPage'
import AlumniListPage from '../pages/AlumniListPage'
import DashboardPage from '../pages/DashboardPage'
import EditAlumniPage from '../pages/EditAlumniPage'
import LoginPage from '../pages/LoginPage'
import TrackingPage from '../pages/TrackingPage'
import TrackingResultsPage from '../pages/TrackingResultsPage'
import ProtectedRoute from './ProtectedRoute'

function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />

        <Route
          element={(
            <ProtectedRoute>
              <AdminLayout />
            </ProtectedRoute>
          )}
        >
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/alumni" element={<AlumniListPage />} />
          <Route path="/alumni/add" element={<AddAlumniPage />} />
          <Route path="/alumni/:id/edit" element={<EditAlumniPage />} />
          <Route path="/alumni/:id" element={<AlumniDetailPage />} />
          <Route path="/tracking" element={<TrackingPage />} />
          <Route path="/results" element={<TrackingResultsPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default AppRouter
