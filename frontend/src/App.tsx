import React from 'react'
import { 
 Box, 
  Container, 
  Heading, 
  VStack, 
  HStack, 
  Button, 
  useColorMode,
  Text,
  Flex
} from '@chakra-ui/react'
import { Outlet, Link, useNavigate } from 'react-router-dom'
import { useQuery, useQueryClient } from '@tanstack/react-query'

// Типы для данных
interface User {
  id: number
  username: string
  email: string
  role: 'parent' | 'child'
}

interface ChildProfile {
  id: number
  first_name: string
  last_name: string
 birth_date: string
  height: number
  gender: string
  best_result?: number
}

interface Measurement {
  id: number
 value: number
 timestamp: string
 zone: 'green' | 'yellow' | 'red'
  notes?: string
}

const App: React.FC = () => {
  const { colorMode, toggleColorMode } = useColorMode()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  // Запрос текущего пользователя
  const { data: currentUser, isLoading: userLoading } = useQuery<User>({
    queryKey: ['currentUser'],
    queryFn: async () => {
      // В реальной системе здесь будет запрос к API
      // return await apiService.getCurrentUser()
      return {
        id: 1,
        username: 'parent123',
        email: 'parent@example.com',
        role: 'parent'
      }
    },
    staleTime: 5 * 60 * 100, // 5 минут
  })

 // Запрос профиля ребенка
  const { data: childProfile, isLoading: profileLoading } = useQuery<ChildProfile>({
    queryKey: ['childProfile'],
    queryFn: async () => {
      // В реальной системе здесь будет запрос к API
      // return await apiService.getChildProfile()
      return {
        id: 1,
        first_name: 'Анна',
        last_name: 'Иванова',
        birth_date: '2015-05-15',
        height: 130,
        gender: 'female',
        best_result: 450
      }
    },
    staleTime: 10 * 60 * 1000, // 10 минут
    enabled: !!currentUser, // Выполняется только если есть пользователь
 })

  const handleLogout = () => {
    // В реальной системе здесь будет логика выхода
    // apiService.logout()
    queryClient.clear()
    navigate('/login')
  }

  return (
    <Flex direction="column" minH="100vh">
      {/* Шапка */}
      <Box bg="gray.100" px={4} py={3} boxShadow="md">
        <Container maxW="container.xl">
          <Flex justifyContent="space-between" alignItems="center">
            <HStack spacing={6}>
              <Link to="/">
                <Heading size="md" color="teal.600">Пикфлоуметр</Heading>
              </Link>
              {currentUser && (
                <HStack spacing={4}>
                  <Link to="/measurements">
                    <Button size="sm" variant="ghost">Измерения</Button>
                  </Link>
                  <Link to="/child-profile">
                    <Button size="sm" variant="ghost">Профиль ребенка</Button>
                  </Link>
                  {currentUser.role === 'parent' && (
                    <Link to="/reminders">
                      <Button size="sm" variant="ghost">Напоминания</Button>
                    </Link>
                  )}
                </HStack>
              )}
            </HStack>
            
            <HStack spacing={3}>
              <Button onClick={toggleColorMode} size="sm" variant="ghost">
                {colorMode === 'light' ? '🌙' : '☀️'}
              </Button>
              {currentUser ? (
                <VStack spacing={0} alignItems="flex-start">
                  <Text fontSize="sm">{currentUser.username}</Text>
                  <Text fontSize="xs" color="gray.500">{currentUser.role === 'parent' ? 'Родитель' : 'Ребенок'}</Text>
                </VStack>
              ) : null}
              {currentUser && (
                <Button onClick={handleLogout} size="sm" colorScheme="red">
                  Выйти
                </Button>
              )}
            </HStack>
          </Flex>
        </Container>
      </Box>

      {/* Основной контент */}
      <Box flex={1} py={8}>
        <Container maxW="container.xl">
          <Outlet />
        </Container>
      </Box>

      {/* Футер */}
      <Box bg="gray.100" px={4} py={6} borderTop="1px" borderColor="gray.200">
        <Container maxW="container.xl">
          <Text textAlign="center" color="gray.600" fontSize="sm">
            Медицинский трекер "Пикфлоуметр" для контроля состояния детей с астмой
          </Text>
        </Container>
      </Box>
    </Flex>
  )
}

export default App