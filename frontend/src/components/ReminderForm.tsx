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
  HStack,
  Card,
  CardBody,
  Switch,
  CheckboxGroup,
  Checkbox,
  Stack
} from '@chakra-ui/react'
import { useMutation, useQueryClient } from '@tanstack/react-query'

// Типы для данных
interface Reminder {
  id?: number
  time_of_day: string // HH:MM
  days_of_week: number[] // [1,2,3,4,5,6,7] - понедельник-воскресенье
  is_active: boolean
  notification_type: 'telegram' | 'email' | 'both'
}

interface ReminderFormProps {
  childId: number
 reminder?: Reminder
  onSuccess?: () => void
}

const ReminderForm: React.FC<ReminderFormProps> = ({ childId, reminder, onSuccess }) => {
  const [formData, setFormData] = useState<Reminder>(reminder || {
    time_of_day: '08:00',
    days_of_week: [1, 3, 5], // по умолчанию понедельник, среда, пятница
    is_active: true,
    notification_type: 'telegram'
  })
  
  const toast = useToast()
  const queryClient = useQueryClient()

  const reminderMutation = useMutation({
    mutationFn: async (reminderData: Reminder) => {
      // В реальной системе здесь будет вызов API
      // const method = reminder?.id ? 'PUT' : 'POST'
      // const url = reminder?.id ? `/api/reminders/${reminder.id}` : '/api/reminders'
      // 
      // const response = await fetch(url, {
      //   method,
      //   headers: {
      //     'Content-Type': 'application/json',
      //     'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      //   },
      //   body: JSON.stringify({
      //     ...reminderData,
      //     child_id: childId
      //   })
      // })
      // return response.json()
      
      // Заглушка для демонстрации
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({ ...reminderData, id: Math.floor(Math.random() * 1000) })
        }, 300)
      })
    },
    onSuccess: () => {
      toast({
        title: 'Напоминание сохранено',
        description: 'Настройки напоминания успешно обновлены',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
      queryClient.invalidateQueries({ queryKey: ['reminders', childId] })
      if (onSuccess) onSuccess()
    },
    onError: (error) => {
      toast({
        title: 'Ошибка сохранения',
        description: 'Не удалось сохранить настройки напоминания',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    reminderMutation.mutate(formData)
 }

  const handleDayToggle = (day: number) => {
    setFormData(prev => {
      const newDays = [...prev.days_of_week]
      const dayIndex = newDays.indexOf(day)
      if (dayIndex >= 0) {
        newDays.splice(dayIndex, 1)
      } else {
        newDays.push(day)
      }
      return { ...prev, days_of_week: newDays.sort((a, b) => a - b) }
    })
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    }))
  }

  const dayNames = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

  return (
    <Card>
      <CardBody>
        <VStack spacing={6} align="stretch">
          <Heading size="md">
            {reminder?.id ? 'Редактировать напоминание' : 'Создать напоминание'}
          </Heading>
          
          <form onSubmit={handleSubmit}>
            <VStack spacing={4} align="stretch">
              <HStack spacing={4}>
                <FormControl id="time_of_day" isRequired flex={1}>
                  <FormLabel>Время напоминания</FormLabel>
                  <Input
                    name="time_of_day"
                    type="time"
                    value={formData.time_of_day}
                    onChange={handleInputChange}
                  />
                </FormControl>
                
                <FormControl id="notification_type" isRequired flex={1}>
                  <FormLabel>Тип уведомления</FormLabel>
                  <Select
                    name="notification_type"
                    value={formData.notification_type}
                    onChange={handleInputChange}
                  >
                    <option value="telegram">Telegram</option>
                    <option value="email">Email</option>
                    <option value="both">Оба</option>
                  </Select>
                </FormControl>
              </HStack>
              
              <FormControl id="days_of_week">
                <FormLabel>Дни недели</FormLabel>
                <CheckboxGroup colorScheme="teal">
                  <Stack spacing={[1, 4]} direction={['column', 'row']}>
                    {dayNames.map((day, index) => (
                      <Checkbox
                        key={index}
                        isChecked={formData.days_of_week.includes(index + 1)}
                        onChange={() => handleDayToggle(index + 1)}
                      >
                        {day}
                      </Checkbox>
                    ))}
                  </Stack>
                </CheckboxGroup>
              </FormControl>
              
              <HStack spacing={4} align="center">
                <Switch
                  name="is_active"
                  isChecked={formData.is_active}
                  onChange={(e) => setFormData(prev => ({ ...prev, is_active: e.target.checked }))}
                />
                <FormLabel mb={0}>Активно</FormLabel>
              </HStack>
              
              <Button
                type="submit"
                colorScheme="teal"
                size="lg"
                isLoading={reminderMutation.isPending}
                loadingText="Сохранение..."
                alignSelf="flex-start"
              >
                {reminder?.id ? 'Обновить' : 'Создать'} напоминание
              </Button>
            </VStack>
          </form>
        </VStack>
      </CardBody>
    </Card>
  )
}

export default ReminderForm