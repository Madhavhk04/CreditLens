import { useEffect, useRef } from 'react'
import { useSpring, useMotionValue, motion } from 'framer-motion'
import { arc as d3Arc } from 'd3-shape'
import { interpolateRgb } from 'd3-interpolate'

const TAU = Math.PI * 2
const START_ANGLE = -Math.PI * 0.75
const END_ANGLE = Math.PI * 0.75
const ARC_RANGE = END_ANGLE - START_ANGLE

function scoreToColor(score) {
  if (score <= 40) return interpolateRgb('#ef4444', '#f59e0b')(score / 40)
  if (score <= 70) return interpolateRgb('#f59e0b', '#22c55e')((score - 40) / 30)
  return interpolateRgb('#22c55e', '#22c55e')((score - 70) / 30)
}

export default function RadialGauge({ score = 68, size = 160, label = 'Portfolio risk score' }) {
  const canvasRef = useRef(null)
  const animatedScore = useMotionValue(0)
  const spring = useSpring(animatedScore, { stiffness: 60, damping: 20 })

  useEffect(() => {
    animatedScore.set(score)
  }, [score, animatedScore])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    const dpr = window.devicePixelRatio || 1
    canvas.width = size * dpr
    canvas.height = size * dpr
    ctx.scale(dpr, dpr)

    const unsub = spring.on('change', (val) => {
      ctx.clearRect(0, 0, size, size)
      const cx = size / 2
      const cy = size / 2
      const radius = (size / 2) - 16
      const thickness = 10

      // Background track
      ctx.beginPath()
      ctx.arc(cx, cy, radius, START_ANGLE, END_ANGLE)
      ctx.strokeStyle = 'rgba(255,255,255,0.06)'
      ctx.lineWidth = thickness
      ctx.lineCap = 'round'
      ctx.stroke()

      // Filled arc
      const progress = Math.min(val / 100, 1)
      const currentAngle = START_ANGLE + ARC_RANGE * progress
      ctx.beginPath()
      ctx.arc(cx, cy, radius, START_ANGLE, currentAngle)
      ctx.strokeStyle = scoreToColor(val)
      ctx.lineWidth = thickness
      ctx.lineCap = 'round'
      ctx.stroke()

      // Score text
      ctx.fillStyle = '#f0f0f5'
      ctx.font = `500 ${size * 0.2}px "DM Mono", monospace`
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      ctx.fillText(Math.round(val), cx, cy - 4)

      // "/100" sub
      ctx.fillStyle = '#5a5a72'
      ctx.font = `500 ${size * 0.09}px "Inter", sans-serif`
      ctx.fillText('/100', cx, cy + size * 0.13)
    })

    return () => unsub()
  }, [spring, size])

  return (
    <div className="gauge-container">
      <canvas
        ref={canvasRef}
        style={{ width: size, height: size }}
      />
      <div className="gauge-label">{label}</div>
      <div className="gauge-sublabel">Composite: PAR30 + NPL + concentration</div>
    </div>
  )
}
