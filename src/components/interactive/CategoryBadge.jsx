import { Home, Car, Briefcase, GraduationCap, CreditCard, Building2 } from 'lucide-react'

const iconMap = {
  home: Home,
  car: Car,
  briefcase: Briefcase,
  graduation: GraduationCap,
  credit: CreditCard,
  building: Building2,
}

export default function CategoryBadge({ icon = 'briefcase', colorClass = 'badge-orange' }) {
  const Icon = iconMap[icon] || Briefcase

  return (
    <div className={`category-badge ${colorClass}`}>
      <Icon size={16} strokeWidth={1.8} />
    </div>
  )
}
