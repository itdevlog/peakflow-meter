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
  Link,
  Flex,
  Center
} from '@chakra-ui/react'
import { useNavigate, Link as RouterLink } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'

// Типы для данных
interface LoginCredentials {
  username: string
  password: string
}

interface LoginResponse {
  access_token: string
  token_type: string
}

const LoginForm: React.FC = () => {
  const [credentials, setCredentials] = useState<LoginCredentials>({ username: '', password: '' })
  const navigate = useNavigate()
  const toast = useToast()

  const loginMutation = useMutation({
    mutationFn: async (loginData: LoginCredentials) => {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData)
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      return response.json();
    },
    onSuccess: (data) => {
      // Сохраняем токен в localStorage
      localStorage.setItem('access_token', data.access_token)
      toast({
        title: 'Успешный вход',
        description: 'Добро пожаловать в систему!',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
      // Перенаправляем на главную страницу
      navigate('/')
    },
    onError: (error) => {
      toast({
        title: 'Ошибка входа',
        description: 'Неправильное имя пользователя или пароль',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    loginMutation.mutate(credentials)
 }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setCredentials(prev => ({ ...prev, [name]: value }))
  }

  return (
    <Flex minH="100vh" align="center" justify="center" bg="gray.50">
      <Box 
        p={8} 
        maxW="md" 
        borderWidth={1} 
        borderRadius="lg" 
        boxShadow="lg"
        bg="white"
      >
        <VStack spacing={6} align="stretch">
          <Center>
            <Heading size="xl" color="teal.600">Пикфлоуметр</Heading>
          </Center>
          <Heading size="lg" textAlign="center">Вход в систему</Heading>
          
          <form onSubmit={handleSubmit}>
            <VStack spacing={4} align="stretch">
              <FormControl id="username" isRequired>
                <FormLabel>Имя пользователя</FormLabel>
                <Input
                  name="username"
                  type="text"
                  value={credentials.username}
                  onChange={handleChange}
                  placeholder="Введите имя пользователя"
                />
              </FormControl>
              
              <FormControl id="password" isRequired>
                <FormLabel>Пароль</FormLabel>
                <Input
                  name="password"
                  type="password"
                  value={credentials.password}
                  onChange={handleChange}
                  placeholder="Введите пароль"
                />
              </FormControl>
              
              <Button
                type="submit"
                colorScheme="teal"
                size="lg"
                isLoading={loginMutation.isPending}
                loadingText="Вход..."
              >
                Войти
              </Button>
            </VStack>
          </form>
          
          <Text textAlign="center" mt={4}>
            Нет аккаунта?{' '}
            <Link as={RouterLink} to="/register" color="teal.500">
              Зарегистрироваться
            </Link>
          </Text>
        </VStack>
      </Box>
    </Flex>
  )
}

export default LoginForm