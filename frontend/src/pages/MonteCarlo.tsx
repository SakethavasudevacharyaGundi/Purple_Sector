import { Card, CardContent } from "@/components/ui/card"
import { StatCard } from "@/components/StatCard"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const distributionData = [
  { position: 'P1', probability: 18 },
  { position: 'P2', probability: 35 },
  { position: 'P3', probability: 19 },
  { position: 'P4', probability: 15 },
  { position: 'P5', probability: 8 },
  { position: 'P6+', probability: 5 },
]

export function MonteCarlo() {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Monte Carlo Analysis</h1>
        <p className="text-muted-foreground mt-2">Probabilistic outcome based on 10,000 simulations.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-[#1D1D1D] border-border/50">
          <CardContent className="p-6 text-center space-y-2">
            <p className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Win Probability</p>
            <p className="text-5xl font-bold text-white">18%</p>
          </CardContent>
        </Card>
        <Card className="bg-[#1D1D1D] border-border/50">
          <CardContent className="p-6 text-center space-y-2">
            <p className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Podium Probability</p>
            <p className="text-5xl font-bold text-primary">72%</p>
          </CardContent>
        </Card>
        <Card className="bg-[#1D1D1D] border-border/50">
          <CardContent className="p-6 text-center space-y-2">
            <p className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Points Probability</p>
            <p className="text-5xl font-bold text-success">98%</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="bg-[#1D1D1D] border-border/50 lg:col-span-2">
          <CardContent className="p-6">
            <p className="text-sm font-medium text-muted-foreground mb-6">Position Distribution</p>
            <div className="w-full h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={distributionData} layout="vertical" margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={false} />
                  <XAxis 
                    type="number" 
                    stroke="#666" 
                    tick={{fill: '#888'}} 
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(val) => `${val}%`}
                  />
                  <YAxis 
                    type="category" 
                    dataKey="position" 
                    stroke="#666" 
                    tick={{fill: '#fff', fontWeight: 500}}
                    tickLine={false}
                    axisLine={false}
                  />
                  <Tooltip 
                    cursor={{fill: '#ffffff0a'}}
                    contentStyle={{ backgroundColor: '#111', borderColor: '#333', borderRadius: '8px' }}
                    itemStyle={{ color: '#fff' }}
                    formatter={(value: any) => [`${value}%`, 'Probability']}
                  />
                  <Bar dataKey="probability" radius={[0, 4, 4, 0]}>
                    {distributionData.map((_entry, index) => (
                      <Cell key={`cell-${index}`} fill={index < 3 ? '#7E57FF' : '#333'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <div className="space-y-6">
          <StatCard title="Expected Finish" value="3.2" />
          <StatCard title="Median Position" value="3" />
          <StatCard title="Standard Deviation" value="1.8" subtitle="Positions" />
        </div>
      </div>
    </div>
  )
}
