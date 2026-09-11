export default function TopBar({ title }) {
  const now = new Date()
  const ts = now.toISOString().slice(0, 16).replace('T', ' ') + ' UTC'

  return (
    <div className="top-bar">
      <h1>{title}</h1>
      <div className="top-bar-right">
        <span className="top-bar-sync">Sync: {ts}</span>
        <div className="top-bar-status">
          <span className="status-dot" />
          Portfolio batch active
        </div>
      </div>
    </div>
  )
}
