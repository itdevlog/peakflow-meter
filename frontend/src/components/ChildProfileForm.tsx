import React, { useState, useEffect } from 'react'
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
  CardBody
} from '@chakra-ui/react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

// Типы для данных
interface ChildProfile {
  id?: number
  first_name: string
 last_name: string
  birth_date: string
  height: number
  gender: 'male' | 'female'
  best_result?: number
}

interface ChildProfileFormProps {
  childId?: number
 onSuccess?: () => void
}

const ChildProfileForm: React.FC<ChildProfileFormProps> = ({ childId, onSuccess }) => {
  const [profile, setProfile] = useState<ChildProfile>({
    first_name: '',
    last_name: '',
    birth_date: '',
    height: 0,
    gender: 'male',
    best_result: undefined
  })
  
  const toast = useToast()
  const queryClient = useQueryClient()

  // Загрузка профиля, если childId предоставлен
  const { data: existingProfile, isLoading } = useQuery<ChildProfile>({
    queryKey: ['childProfile', childId],
    queryFn: async () => {
      // В реальной системе здесь будет вызов API
      // const response = await fetch(`/api/users/child-profile`, {
      //   headers: {
      //     'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      //   }
      // })
      // return response.json()
      
      // Заглушка для демонстрации
      return new Promise<ChildProfile>((resolve) => {
        setTimeout(() => {
          resolve({
            id: 1,
            first_name: 'Анна',
            last_name: 'Иванова',
            birth_date: '2015-05-15',
            height: 130,
            gender: 'female',
            best_result: 450
          })
        }, 300)
      })
    },
    enabled: !!childId,
    staleTime: 5 * 60 * 1000, // 5 минут
  })

 // Загружаем данные профиля при его получении
  useEffect(() => {
    if (existingProfile) {
      setProfile(existingProfile)
    }
  }, [existingProfile])

  const profileMutation = useMutation({
    mutationFn: async (profileData: ChildProfile) => {
      // В реальной системе здесь будет вызов API
      // const method = childId ? 'PUT' : 'POST'
      // const url = childId ? `/api/users/child-profile/${childId}` : '/api/users/child-profile'
      // 
      // const response = await fetch(url, {
      //   method,
      //   headers: {
      //     'Content-Type': 'application/json',
      //     'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      //   },
      //   body: JSON.stringify(profileData)
      // })
      // return response.json()
      
      // Заглушка для демонстрации
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({ ...profileData, id: 1 })
        }, 300)
      })
    },
    onSuccess: () => {
      toast({
        title: 'Профиль сохранен',
        description: 'Данные профиля успешно обновлены',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
      queryClient.invalidateQueries({ queryKey: ['childProfile', childId] })
      if (onSuccess) onSuccess()
    },
    onError: (error) => {
      toast({
        title: 'Ошибка сохранения',
        description: 'Не удалось сохранить профиль',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  })

 const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!profile.first_name || !profile.last_name || !profile.birth_date || profile.height <= 0) {
      toast({
        title: 'Неполные данные',
        description: 'Пожалуйста, заполните все обязательные поля',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
      return
    }
    profileMutation.mutate(profile)
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setProfile(prev => ({
      ...prev,
      [name]: name === 'height' ? Number(value) : value
    }))
  }

  if (childId && isLoading) {
    return (
      <Card>
        <CardBody>
          <Text>Загрузка данных профиля...</Text>
        </CardBody>
      </Card>
    )
  }

  return (
    <Card>
      <CardBody>
        <VStack spacing={6} align="stretch">
          <Heading size="md">
            {childId ? 'Редактировать профиль ребенка' : 'Создать профиль ребенка'}
          </Heading>
          
          <form onSubmit={handleSubmit}>
            <VStack spacing={4} align="stretch">
              <HStack spacing={4}>
                <FormControl id="first_name" isRequired flex={1}>
                  <FormLabel>Имя</FormLabel>
                  <Input
                    name="first_name"
                    type="text"
                    value={profile.first_name}
                    onChange={handleChange}
                    placeholder="Введите имя"
                  />
                </FormControl>
                
                <FormControl id="last_name" isRequired flex={1}>
                  <FormLabel>Фамилия</FormLabel>
                  <Input
                    name="last_name"
                    type="text"
                    value={profile.last_name}
                    onChange={handleChange}
                    placeholder="Введите фамилию"
                  />
                </FormControl>
              </HStack>
              
              <HStack spacing={4}>
                <FormControl id="birth_date" isRequired flex={1}>
                  <FormLabel>Дата рождения</FormLabel>
                  <Input
                    name="birth_date"
                    type="date"
                    value={profile.birth_date}
                    onChange={handleChange}
                  />
                </FormControl>
                
                <FormControl id="height" isRequired flex={1}>
                  <FormLabel>Рост (см)</FormLabel>
                  <Input
                    name="height"
                    type="number"
                    min="0"
                    max="300"
                    value={profile.height || ''}
                    onChange={handleChange}
                    placeholder="Введите рост в см"
                  />
                </FormControl>
              </HStack>
              
              <HStack spacing={4}>
                <FormControl id="gender" isRequired flex={1}>
                  <FormLabel>Пол</FormLabel>
                  <Select
                    name="gender"
                    value={profile.gender}
                    onChange={handleChange}
                  >
                    <option value="male">Мальчик</option>
                    <option value="female">Девочка</option>
                  </Select>
                </FormControl>
                
                <FormControl id="best_result" flex={1}>
                  <FormLabel>Лучший результат пикфлоу (л/мин)</FormLabel>
                  <Input
                    name="best_result"
                    type="number"
                    min="0"
                    max="999"
                    value={profile.best_result || ''}
                    onChange={handleChange}
                    placeholder="Введите лучший результат"
                  />
                </FormControl>
              </HStack>
              
              <Button
                type="submit"
                colorScheme="teal"
                size="lg"
                isLoading={profileMutation.isPending}
                loadingText="Сохранение..."
                alignSelf="flex-start"
              >
                {childId ? 'Обновить профиль' : 'Создать профиль'}
              </Button>
            </VStack>
          </form>
        </VStack>
      </CardBody>
    </Card>
  )
}

export default ChildProfileForm