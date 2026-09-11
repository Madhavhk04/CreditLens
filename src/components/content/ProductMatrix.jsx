import CategoryBadge from '../interactive/CategoryBadge'
import GlassCard from '../cards/GlassCard'

const products = [
  { name: 'Personal loan', icon: 'briefcase', badge: 'badge-orange', volume: '$42.5M', wair: '15.00%', par30: '3.90%', npl: '1.80%', risk: true },
  { name: 'Auto loan', icon: 'car', badge: 'badge-green', volume: '$35.4M', wair: '10.00%', par30: '0.45%', npl: '0.25%', risk: false },
  { name: 'Home loan', icon: 'home', badge: 'badge-blue', volume: '$51.2M', wair: '8.50%', par30: '0.22%', npl: '0.10%', risk: false },
  { name: 'Education loan', icon: 'graduation', badge: 'badge-violet', volume: '$16.1M', wair: '11.00%', par30: '1.15%', npl: '0.55%', risk: false },
]

export default function ProductMatrix() {
  return (
    <GlassCard>
      <div className="card-title">Product category performance</div>
      <div style={{ overflowX: 'auto' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Product</th>
              <th>Disbursed volume</th>
              <th>WAIR (%)</th>
              <th>PAR 30 (%)</th>
              <th>NPL rate (%)</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p) => (
              <tr key={p.name} className={p.risk ? 'risk-row' : ''}>
                <td className="td-label">
                  <CategoryBadge icon={p.icon} colorClass={p.badge} />
                  {p.name}
                </td>
                <td>{p.volume}</td>
                <td>{p.wair}</td>
                <td className={p.risk ? 'risk-val' : ''}>{p.par30}</td>
                <td className={p.risk ? 'risk-val' : ''}>{p.npl}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </GlassCard>
  )
}
