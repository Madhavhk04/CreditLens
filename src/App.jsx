import { useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import Sidebar from './components/layout/Sidebar'
import ExecutiveOverview from './pages/ExecutiveOverview'
import UnderwritingFunnel from './pages/UnderwritingFunnel'
import PortfolioPerformance from './pages/PortfolioPerformance'
import RiskIntelligence from './pages/RiskIntelligence'
import CollectionAnalytics from './pages/CollectionAnalytics'
import GeographicIntelligence from './pages/GeographicIntelligence'

const pageComponents = {
  overview: ExecutiveOverview,
  funnel: UnderwritingFunnel,
  portfolio: PortfolioPerformance,
  risk: RiskIntelligence,
  collections: CollectionAnalytics,
  geography: GeographicIntelligence,
}

const pageTransition = {
  initial: { opacity: 0, y: 8 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -4 },
  transition: { duration: 0.25, ease: 'easeOut' }
}

export default function App() {
  const [activePage, setActivePage] = useState('overview')
  const ActivePage = pageComponents[activePage]

  return (
    <div className="app-shell">
      <Sidebar activePage={activePage} onPageChange={setActivePage} />
      <main className="main-content">
        <AnimatePresence mode="wait">
          <motion.div
            key={activePage}
            className="page-content"
            {...pageTransition}
          >
            <ActivePage />
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  )
}
