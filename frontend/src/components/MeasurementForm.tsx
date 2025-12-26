import React, { useState } from 'react'
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Heading,
  Text,
  useToast,
  Select,
  Textarea,
  HStack
} from '@chakra-ui/react'
import { useMutation, useQueryClient } from '@tanstack/react-query'

// Типы для данных
interface MeasurementData {
  value: number
  timestamp: string
  notes?: string
}

interface MeasurementFormProps {
  childId: number
  onSuccess?: () => void
}

const MeasurementForm: React.FC<MeasurementFormProps> = ({ childId, onSuccess }) => {
  const [measurement, setMeasurement] = useState<MeasurementData>({ 
    value: 0, 
    timestamp: new Date().toISOString().slice(0, 16), // Формат для datetime-local
    notes: ''
  })
  const toast = useToast()
  const queryClient = useQueryClient()

  const measurementMutation = useMutation({
    mutationFn: async (measurementData: MeasurementData) => {
      const response = await fetch('/api/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          ...measurementData,
          child_id: childId
        })
      });

      if (!response.ok) {
        throw new Error('Failed to save measurement');
      }

      return response.json();
    },
    onSuccess: () => {
      toast({
        title: 'Измерение сохранено',
        description: 'Результат успешно добавлен в систему',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
      queryClient.invalidateQueries({ queryKey: ['measurements', childId] })
      if (onSuccess) onSuccess()
    },
    onError: (error) => {
      toast({
        title: 'Ошибка сохранения',
        description: 'Не удалось сохранить измерение',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (measurement.value <= 0) {
      toast({
        title: 'Некорректное значение',
        description: 'Значение пикфлоу должно быть положительным',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
      return
    }
    measurementMutation.mutate(measurement)
  }

 const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setMeasurement(prev => ({ ...prev, [name]: name === 'value' ? Number(value) : value }))
  }

 return (
    <Box p={6} borderWidth={1} borderRadius="lg" boxShadow="md" bg="white">
      <VStack spacing={6} align="stretch">
        <Heading size="md">Добавить результат измерения</Heading>
        
        <form onSubmit={handleSubmit}>
          <VStack spacing={4} align="stretch">
            <HStack spacing={4}>
              <FormControl id="value" isRequired flex={1}>
                <FormLabel>Значение пикфлоу (л/мин)</FormLabel>
                <Input
                  name="value"
                  type="number"
                  min="0"
                  max="999"
                  value={measurement.value || ''}
                  onChange={handleChange}
                  placeholder="Введите значение"
                />
              </FormControl>
              
              <FormControl id="timestamp" isRequired flex={1}>
                <FormLabel>Время измерения</FormLabel>
                <Input
                  name="timestamp"
                  type="datetime-local"
                  value={measurement.timestamp}
                  onChange={handleChange}
                />
              </FormControl>
            </HStack>
            
            <FormControl id="notes">
              <FormLabel>Примечания (необязательно)</FormLabel>
              <Textarea
                name="notes"
                value={measurement.notes}
                onChange={handleChange}
                placeholder="Дополнительная информация об измерении"
                rows={3}
              />
            </FormControl>
            
            <Button
              type="submit"
              colorScheme="teal"
              size="lg"
              isLoading={measurementMutation.isPending}
              loadingText="Сохранение..."
              alignSelf="flex-start"
            >
              Сохранить измерение
            </Button>
          </VStack>
        </form>
      </VStack>
    </Box>
  )
}

export default MeasurementForm