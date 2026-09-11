import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

const COLORS = ['#3b82f6', '#06b6d4', '#f59e0b', '#22c55e']

const renderLegend = (props) => {
  const { payload } = props
  return (
    <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: 6 }}>
      {payload.map((entry, i) => (
        <li key={i} style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 12, color: '#a1a1b5' }}>
          <span style={{ width: 8, height: 8, borderRadius: '50%', background: entry.color, flexShrink: 0 }} />
          {entry.value}
        </li>
      ))}
    </ul>
  )
}

export default function ChannelDonut({ data }) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie
          data={data}
          cx="40%"
          cy="50%"
          innerRadius="55%"
          outerRadius="85%"
          dataKey="value"
          nameKey="name"
          animationBegin={0}
          animationDuration={800}
          animationEasing="ease-out"
          stroke="none"
        >
          {data.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} />
          ))}
        </Pie>
        <Legend
          layout="vertical"
          align="right"
          verticalAlign="middle"
          content={renderLegend}
        />
        <Tooltip
          contentStyle={{
            background: '#1a1a2e',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: 12,
            color: '#f0f0f5',
            fontSize: 12,
            fontFamily: 'Inter'
          }}
        />
      </PieChart>
    </ResponsiveContainer>
  )
}
