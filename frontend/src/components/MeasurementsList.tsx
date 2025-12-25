import React from 'react'
import {
  Box,
  VStack,
  HStack,
  Text,
  Badge,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableContainer,
  Spinner,
  Alert,
  AlertIcon,
  AlertDescription,
  Flex,
  Spacer
} from '@chakra-ui/react'
import { useQuery } from '@tanstack/react-query'
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'

// Типы для данных
interface Measurement {
  id: number
  value: number
  timestamp: string
  zone: 'green' | 'yellow' | 'red'
  notes?: string
}

interface MeasurementsListProps {
  childId: number
}

const MeasurementsList: React.FC<MeasurementsListProps> = ({ childId }) => {
  const { data: measurements, isLoading, error } = useQuery<Measurement[]>({
    queryKey: ['measurements', childId],
    queryFn: async () => {
      // В реальной системе здесь будет вызов API
      // const response = await fetch(`/api/measurements?child_id=${childId}`, {
      //   headers: {
      //     'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      //   }
      // })
      // return response.json()
      
      // Заглушка для демонстрации
      return new Promise<Measurement[]>((resolve) => {
        setTimeout(() => {
          resolve([
            { id: 1, value: 450, timestamp: '2023-12-25T10:30:00Z', zone: 'green', notes: 'Хороший результат утром' },
            { id: 2, value: 380, timestamp: '2023-12-24T15:45:00Z', zone: 'yellow', notes: 'После физической активности' },
            { id: 3, value: 320, timestamp: '2023-12-23T08:15:00Z', zone: 'red', notes: 'Были симптомы' },
            { id: 4, value: 470, timestamp: '2023-12-22T09:00Z', zone: 'green' },
          ])
        }, 500)
      })
    },
    staleTime: 5 * 60 * 1000, // 5 минут
  })

  const getZoneColor = (zone: string) => {
    switch (zone) {
      case 'green': return 'green'
      case 'yellow': return 'yellow'
      case 'red': return 'red'
      default: return 'gray'
    }
  }

  const getZoneText = (zone: string) => {
    switch (zone) {
      case 'green': return 'Зеленая зона (отлично)'
      case 'yellow': return 'Желтая зона (осторожно)'
      case 'red': return 'Красная зона (тревожно)'
      default: return 'Неизвестно'
    }
 }

  if (isLoading) {
    return (
      <Flex justify="center" align="center" py={10}>
        <Spinner size="xl" />
      </Flex>
    )
  }

 if (error) {
    return (
      <Alert status="error">
        <AlertIcon />
        <AlertDescription>Ошибка загрузки данных: {(error as Error).message}</AlertDescription>
      </Alert>
    )
  }

  return (
    <Box borderWidth={1} borderRadius="lg" boxShadow="md" bg="white" p={6}>
      <VStack spacing={6} align="stretch">
        <HStack justifyContent="space-between">
          <Heading size="md">История измерений</Heading>
          <Text fontSize="sm" color="gray.500">
            Последние измерения для ребенка
          </Text>
        </HStack>

        {measurements && measurements.length > 0 ? (
          <TableContainer>
            <Table variant="simple">
              <Thead>
                <Tr>
                  <Th>Дата и время</Th>
                  <Th>Значение</Th>
                  <Th>Зона</Th>
                  <Th>Примечания</Th>
                </Tr>
              </Thead>
              <Tbody>
                {measurements.map((measurement) => (
                  <Tr key={measurement.id}>
                    <Td>
                      {format(new Date(measurement.timestamp), 'dd MMMM yyyy, HH:mm', { locale: ru })}
                    </Td>
                    <Td fontWeight="bold">{measurement.value} л/мин</Td>
                    <Td>
                      <Badge colorScheme={getZoneColor(measurement.zone)}>
                        {getZoneText(measurement.zone)}
                      </Badge>
                    </Td>
                    <Td>
                      {measurement.notes ? measurement.notes : '-'}
                    </Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </TableContainer>
        ) : (
          <Alert status="info">
            <AlertIcon />
            <AlertDescription>Нет данных об измерениях</AlertDescription>
          </Alert>
        )}
      </VStack>
    </Box>
  )
}

export default MeasurementsList