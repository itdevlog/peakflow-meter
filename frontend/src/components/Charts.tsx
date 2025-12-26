import React, { useState } from 'react'
import {
  Box,
  Heading,
  VStack,
  HStack,
  Text,
  Select,
  Card,
  CardBody,
  Flex
} from '@chakra-ui/react'
import { useQuery } from '@tanstack/react-query'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  Cell
} from 'recharts'

// Типы для данных
interface Measurement {
  id: number
  value: number
  timestamp: string
  zone: 'green' | 'yellow' | 'red'
  notes?: string
}

interface ChartDataPoint {
  date: string
  value: number
  zone: 'green' | 'yellow' | 'red'
  formattedDate: string
}

interface ChartsProps {
  childId: number
}

const Charts: React.FC<ChartsProps> = ({ childId }) => {
  const [timeRange, setTimeRange] = useState<'week' | 'month' | 'quarter'>('week')

  const { data: measurements, isLoading } = useQuery<Measurement[]>({
    queryKey: ['measurements', childId, timeRange],
    queryFn: async () => {
      const response = await fetch(`/api/?child_id=${childId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch measurements');
      }

      return response.json();
    },
    staleTime: 5 * 60 * 1000, // 5 минут
  })

 // Преобразуем данные для графиков
  const chartData: ChartDataPoint[] = measurements?.map(m => ({
    date: m.timestamp,
    value: m.value,
    zone: m.zone,
    formattedDate: new Date(m.timestamp).toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: 'short'
    })
  })) || []

  // Цвета для зон
  const zoneColors = {
    green: '#48bb78',
    yellow: '#ecc94b',
    red: '#f56565'
  }

 return (
    <VStack spacing={6} align="stretch">
      <HStack justifyContent="space-between">
        <Heading size="md">Графики измерений</Heading>
        <Select 
          w="200px" 
          value={timeRange} 
          onChange={(e) => setTimeRange(e.target.value as any)}
        >
          <option value="week">Последние 7 дней</option>
          <option value="month">Последний месяц</option>
          <option value="quarter">Последние 3 месяца</option>
        </Select>
      </HStack>

      {/* Линейный график */}
      <Card>
        <CardBody>
          <Heading size="sm" mb={4}>Динамика показателей</Heading>
          <Box h="400px">
            <ResponsiveContainer width="10%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="formattedDate" />
                <YAxis />
                <Tooltip 
                  formatter={(value) => [`${value} л/мин`, 'Значение']}
                  labelFormatter={(label) => `Дата: ${label}`}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#3182ce" 
                  strokeWidth={2}
                  name="Пикфлоу (л/мин)"
                  dot={{ r: 6 }}
                  activeDot={{ r: 8 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </Box>
        </CardBody>
      </Card>

      {/* Столбчатая диаграмма по зонам */}
      <Card>
        <CardBody>
          <Heading size="sm" mb={4}>Распределение по зонам</Heading>
          <Box h="400px">
            <ResponsiveContainer width="10%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="formattedDate" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" name="Пикфлоу">
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={zoneColors[entry.zone]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Box>
        </CardBody>
      </Card>

      {/* Статистика */}
      <Card>
        <CardBody>
          <Heading size="sm" mb={4}>Статистика</Heading>
          <HStack spacing={8} wrap="wrap">
            <Flex direction="column" align="center">
              <Text fontSize="2xl" fontWeight="bold" color="green.500">
                {measurements?.filter(m => m.zone === 'green').length || 0}
              </Text>
              <Text fontSize="sm">Зеленых зон</Text>
            </Flex>
            <Flex direction="column" align="center">
              <Text fontSize="2xl" fontWeight="bold" color="yellow.500">
                {measurements?.filter(m => m.zone === 'yellow').length || 0}
              </Text>
              <Text fontSize="sm">Желтых зон</Text>
            </Flex>
            <Flex direction="column" align="center">
              <Text fontSize="2xl" fontWeight="bold" color="red.500">
                {measurements?.filter(m => m.zone === 'red').length || 0}
              </Text>
              <Text fontSize="sm">Красных зон</Text>
            </Flex>
            <Flex direction="column" align="center">
              <Text fontSize="2xl" fontWeight="bold" color="blue.500">
                {measurements && measurements.length > 0 
                  ? Math.round(measurements.reduce((sum, m) => sum + m.value, 0) / measurements.length) 
                  : 0}
              </Text>
              <Text fontSize="sm">Среднее значение</Text>
            </Flex>
          </HStack>
        </CardBody>
      </Card>
    </VStack>
  )
}

export default Charts