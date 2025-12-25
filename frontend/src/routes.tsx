import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import App from './App'
import HomePage from './pages/HomePage'
import MeasurementsPage from './pages/MeasurementsPage'
import ChildProfilePage from './pages/ChildProfilePage'
import ChartsPage from './pages/ChartsPage'
import RemindersPage from './pages/RemindersPage'
import LoginForm from './components/LoginForm'

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<App />}>
        <Route index element={<HomePage />} />
        <Route path="login" element={<LoginForm />} />
        <Route path="measurements" element={<MeasurementsPage />} />
        <Route path="measurements/add" element={<MeasurementsPage />} />
        <Route path="child-profile" element={<ChildProfilePage />} />
        <Route path="charts" element={<ChartsPage />} />
        <Route path="reminders" element={<RemindersPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}

export default AppRoutes