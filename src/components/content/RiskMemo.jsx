import { motion } from 'framer-motion'

const listVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.12 } }
}

const itemVariants = {
  hidden: { opacity: 0, x: -8 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.3, ease: 'easeOut' } }
}

export default function RiskMemo({ title, subtitle, body, items = [] }) {
  return (
    <div className="risk-memo">
      <div className="risk-memo-header">{title}</div>
      <div className="risk-memo-title">{subtitle}</div>
      <div className="risk-memo-body" dangerouslySetInnerHTML={{ __html: body }} />
      <motion.ul
        className="risk-memo-list"
        variants={listVariants}
        initial="hidden"
        animate="visible"
      >
        {items.map((item, i) => (
          <motion.li key={i} variants={itemVariants} dangerouslySetInnerHTML={{ __html: item }} />
        ))}
      </motion.ul>
    </div>
  )
}
