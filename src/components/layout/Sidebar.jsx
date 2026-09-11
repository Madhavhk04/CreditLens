import { motion } from 'framer-motion'
import { LayoutDashboard, Filter, Activity, AlertTriangle, Target, MapPin, Shield } from 'lucide-react'

const navItems = [
  { id: 'overview', label: 'Executive overview', icon: LayoutDashboard },
  { id: 'funnel', label: 'Underwriting funnel', icon: Filter },
  { id: 'portfolio', label: 'Portfolio performance', icon: Activity },
  { id: 'risk', label: 'Risk intelligence', icon: AlertTriangle },
  { id: 'collections', label: 'Collection analytics', icon: Target },
  { id: 'geography', label: 'Geographic intelligence', icon: MapPin },
]

export default function Sidebar({ activePage, onPageChange }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-brand-icon">
          <Shield size={18} strokeWidth={2} />
        </div>
        <div className="sidebar-brand-text">
          <h2>CreditLens</h2>
          <span>Lending portfolio intelligence</span>
        </div>
      </div>

      <div className="sidebar-divider" />

      <div className="sidebar-section-label">Workspaces</div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <motion.button
            key={item.id}
            className={`nav-item ${activePage === item.id ? 'active' : ''}`}
            onClick={() => onPageChange(item.id)}
            whileHover={{ x: 2 }}
            whileTap={{ scale: 0.98 }}
            transition={{ duration: 0.15 }}
          >
            <item.icon className="nav-icon" size={18} strokeWidth={1.6} />
            {item.label}
          </motion.button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-engine">
          <div className="sidebar-engine-title">PostgreSQL warehouse</div>
          <div className="sidebar-engine-info">5.8M payment records loaded</div>
          <div className="sidebar-engine-status">Engine: operational</div>
        </div>
      </div>
    </aside>
  )
}
