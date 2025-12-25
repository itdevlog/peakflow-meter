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
  Spacer,
  Button,
  useToast
} from '@chakra-ui/react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

// Типы для данных
interface Reminder {
  id: number
  time_of_day: string // HH:MM
  days_of_week: number[] // [1,2,3,4,5,6,7] - понедельник-воскресенье
  is_active: boolean
  notification_type: 'telegram' | 'email' | 'both'
}

interface RemindersListProps {
  childId: number
 onEdit: (reminder: Reminder) => void
}

const RemindersList: React.FC<RemindersListProps> = ({ childId, onEdit }) => {
 const toast = useToast()
  const queryClient = useQueryClient()

  const { data: reminders, isLoading, error } = useQuery<Reminder[]>({
    queryKey: ['reminders', childId],
    queryFn: async () => {
      // В реальной системе здесь будет вызов API
      // const response = await fetch(`/api/reminders?child_id=${childId}`, {
      //   headers: {
      //     'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      //   }
      // })
      // return response.json()
      
      // Заглушка для демонстрации
      return new Promise<Reminder[]>((resolve) => {
        setTimeout(() => {
          resolve([
            { id: 1, time_of_day: '08:00', days_of_week: [1, 3, 5], is_active: true, notification_type: 'telegram' },
            { id: 2, time_of_day: '20:00', days_of_week: [2, 4, 6], is_active: false, notification_type: 'email' },
            { id: 3, time_of_day: '12:30', days_of_week: [1, 2, 3, 4, 5], is_active: true, notification_type: 'both' },
          ])
        }, 500)
      })
    },
    staleTime: 5 * 60 * 1000, // 5 минут
  })

 const deleteMutation = useMutation({
    mutationFn: async (reminderId: number) => {
      // В реальной системе здесь будет вызов API
      // const response = await fetch(`/api/reminders/${reminderId}`, {
      //   method: 'DELETE',
      //   headers: {
      //     'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      //   }
      // })
      // return response.json()
      
      // Заглушка для демонстрации
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({})
        }, 300)
      })
    },
    onSuccess: () => {
      toast({
        title: 'Напоминание удалено',
        description: 'Настройки напоминания успешно удалены',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
      queryClient.invalidateQueries({ queryKey: ['reminders', childId] })
    },
    onError: (error) => {
      toast({
        title: 'Ошибка удаления',
        description: 'Не удалось удалить напоминание',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  })

  const toggleMutation = useMutation({
    mutationFn: async ({ reminderId, isActive }: { reminderId: number, isActive: boolean }) => {
      // В реальной системе здесь будет вызов API
      // const response = await fetch(`/api/reminders/${reminderId}/toggle`, {
      //   method: 'PUT',
      //   headers: {
      //     'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      //   }
      // })
      // return response.json()
      
      // Заглушка для демонстрации
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({})
        }, 300)
      })
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reminders', childId] })
    },
    onError: (error) => {
      toast({
        title: 'Ошибка обновления',
        description: 'Не удалось обновить статус напоминания',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  })

  const dayNames = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

  const getDaysText = (days: number[]) => {
    if (days.length === 0) return 'Нет'
    if (days.length === 7) return 'Каждый день'
    return days.map(day => dayNames[day - 1]).join(', ')
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
          <Heading size="md">Настройки напоминаний</Heading>
          <Text fontSize="sm" color="gray.500">
            Управление напоминаниями для ребенка
          </Text>
        </HStack>

        {reminders && reminders.length > 0 ? (
          <TableContainer>
            <Table variant="simple">
              <Thead>
                <Tr>
                  <Th>Время</Th>
                  <Th>Дни недели</Th>
                  <Th>Тип уведомления</Th>
                  <Th>Статус</Th>
                  <Th>Действия</Th>
                </Tr>
              </Thead>
              <Tbody>
                {reminders.map((reminder) => (
                  <Tr key={reminder.id}>
                    <Td fontWeight="bold">{reminder.time_of_day}</Td>
                    <Td>{getDaysText(reminder.days_of_week)}</Td>
                    <Td>
                      {reminder.notification_type === 'telegram' && 'Telegram'}
                      {reminder.notification_type === 'email' && 'Email'}
                      {reminder.notification_type === 'both' && 'Оба'}
                    </Td>
                    <Td>
                      <Badge colorScheme={reminder.is_active ? 'green' : 'red'}>
                        {reminder.is_active ? 'Активно' : 'Неактивно'}
                      </Badge>
                    </Td>
                    <Td>
                      <HStack spacing={2}>
                        <Button 
                          size="sm" 
                          onClick={() => onEdit(reminder)}
                        >
                          Редактировать
                        </Button>
                        <Button 
                          size="sm" 
                          colorScheme="red"
                          onClick={() => deleteMutation.mutate(reminder.id)}
                          isLoading={deleteMutation.isPending && deleteMutation.variables === reminder.id}
                        >
                          Удалить
                        </Button>
                        <Button 
                          size="sm" 
                          variant={reminder.is_active ? 'outline' : 'solid'}
                          colorScheme={reminder.is_active ? 'red' : 'green'}
                          onClick={() => toggleMutation.mutate({ 
                            reminderId: reminder.id, 
                            isActive: !reminder.is_active 
                          })}
                          isLoading={toggleMutation.isPending && toggleMutation.variables?.reminderId === reminder.id}
                        >
                          {reminder.is_active ? 'Отключить' : 'Включить'}
                        </Button>
                      </HStack>
                    </Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </TableContainer>
        ) : (
          <Alert status="info">
            <AlertIcon />
            <AlertDescription>Нет настроенных напоминаний</AlertDescription>
          </Alert>
        )}
      </VStack>
    </Box>
  )
}

export default RemindersList