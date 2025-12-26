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
  const { data: currentUser, isLoading: userLoading, isError, error } = useQuery<User>({
    queryKey: ['currentUser'],
    queryFn: async () => {
      const token = localStorage.getItem('access_token');
      // If no token, don't make the API call
      if (!token) {
        // Return null or undefined to indicate no user is logged in, rather than throwing an error
        return null;
      }

      const response = await fetch('/api/profile', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        // If not authenticated, just throw error to be handled by onError
        if (response.status === 401 || response.status === 403) {
          localStorage.removeItem('access_token');
          throw new Error('Unauthorized');
        }
        throw new Error('Failed to fetch user profile');
      }

      return response.json();
    },
    staleTime: 5 * 60 * 1000, // 5 минут
    retry: false, // Don't retry on auth errors
    onError: (err) => {
      console.error('Error fetching user profile:', err);
      // Handle error appropriately
      if (err.message === 'Unauthorized' || err.message.includes('401') || err.message.includes('403')) {
        localStorage.removeItem('access_token');
      }
    },
    // Only run this query if there's a token
    enabled: !!localStorage.getItem('access_token')
  })

 // Запрос профиля ребенка
  const { data: childProfile, isLoading: profileLoading } = useQuery<ChildProfile>({
    queryKey: ['childProfile'],
    queryFn: async () => {
      const token = localStorage.getItem('access_token');
      // If no token, don't make the API call
      if (!token) {
        return null;
      }

      const response = await fetch('/api/child-profile', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        // Handle unauthorized access
        if (response.status === 401 || response.status === 403) {
          localStorage.removeItem('access_token');
          throw new Error('Unauthorized');
        }
        throw new Error('Failed to fetch child profile');
      }

      return response.json();
    },
    staleTime: 10 * 60 * 1000, // 10 минут
    enabled: !!localStorage.getItem('access_token') && !!currentUser && currentUser !== null, // Выполняется только если есть токен и пользователь
    retry: false, // Don't retry on errors
    onError: (err) => {
      console.error('Error fetching child profile:', err);
      // Handle error appropriately
      if (err.message === 'Unauthorized' || err.message.includes('401') || err.message.includes('403')) {
        localStorage.removeItem('access_token');
      }
    }
  })

  const handleLogout = () => {
    // В реальной системе здесь будет логика выхода
    // apiService.logout()
    localStorage.removeItem('access_token');
    queryClient.clear();
    navigate('/login');
  }

  // Show loading state while checking authentication
  if (userLoading && localStorage.getItem('access_token')) {
    return (
      <Flex direction="column" minH="100vh" align="center" justify="center">
        <Heading size="md" color="teal.600">Пикфлоуметр</Heading>
        <Text mt={4}>Загрузка...</Text>
      </Flex>
    );
  }

  // If there's an error with authentication, clear token and redirect to login
  if (isError && localStorage.getItem('access_token')) {
    localStorage.removeItem('access_token');
    navigate('/login');
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
              {currentUser && !userLoading && (
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
              {currentUser && !userLoading ? (
                <VStack spacing={0} alignItems="flex-start">
                  <Text fontSize="sm">{currentUser.username}</Text>
                  <Text fontSize="xs" color="gray.500">{currentUser.role === 'parent' ? 'Родитель' : 'Ребенок'}</Text>
                </VStack>
              ) : null}
              {currentUser && !userLoading && (
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