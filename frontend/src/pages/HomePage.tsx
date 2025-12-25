import React from 'react'
import {
  Box,
  VStack,
  Heading,
  Text,
  HStack,
  Card,
  CardBody,
  Grid,
  GridItem,
  Button,
  useColorModeValue,
  Icon,
  Flex
} from '@chakra-ui/react'
import { FiActivity, FiUser, FiBarChart2, FiBell, FiPlus } from 'react-icons/fi'
import { Link } from 'react-router-dom'

const HomePage: React.FC = () => {
  const bgColor = useColorModeValue('white', 'gray.700')
  const textColor = useColorModeValue('gray.800', 'white')

  return (
    <VStack spacing={6} align="stretch">
      {/* Приветственный блок */}
      <Card bg={bgColor}>
        <CardBody>
          <Flex justifyContent="space-between" alignItems="center">
            <VStack align="start" spacing={2}>
              <Heading size="lg">Добро пожаловать в Пикфлоуметр!</Heading>
              <Text color={textColor}>
                Следите за состоянием здоровья вашего ребенка с помощью системы мониторинга пикфлоу
              </Text>
            </VStack>
            <Button
              as={Link}
              to="/measurements/add"
              colorScheme="teal"
              leftIcon={<Icon as={FiPlus} />}
            >
              Добавить измерение
            </Button>
          </Flex>
        </CardBody>
      </Card>

      {/* Краткая статистика */}
      <Grid templateColumns={{ base: '1fr', md: 'repeat(3, 1fr)' }} gap={6}>
        <GridItem>
          <Card bg={bgColor}>
            <CardBody>
              <HStack spacing={4}>
                <Box p={3} bg="teal.100" borderRadius="md">
                  <Icon as={FiActivity} w={6} h={6} color="teal.600" />
                </Box>
                <VStack align="start" spacing={1}>
                  <Text fontSize="sm" color="gray.500">Последнее измерение</Text>
                  <Heading size="md">450 л/мин</Heading>
                  <Text fontSize="xs" color="green.500">Зеленая зона</Text>
                </VStack>
              </HStack>
            </CardBody>
          </Card>
        </GridItem>
        
        <GridItem>
          <Card bg={bgColor}>
            <CardBody>
              <HStack spacing={4}>
                <Box p={3} bg="yellow.100" borderRadius="md">
                  <Icon as={FiBarChart2} w={6} h={6} color="yellow.600" />
                </Box>
                <VStack align="start" spacing={1}>
                  <Text fontSize="sm" color="gray.500">Среднее значение</Text>
                  <Heading size="md">420 л/мин</Heading>
                  <Text fontSize="xs" color="yellow.500">Желтая зона</Text>
                </VStack>
              </HStack>
            </CardBody>
          </Card>
        </GridItem>
        
        <GridItem>
          <Card bg={bgColor}>
            <CardBody>
              <HStack spacing={4}>
                <Box p={3} bg="red.100" borderRadius="md">
                  <Icon as={FiBell} w={6} h={6} color="red.600" />
                </Box>
                <VStack align="start" spacing={1}>
                  <Text fontSize="sm" color="gray.500">Активных напоминаний</Text>
                  <Heading size="md">2</Heading>
                  <Text fontSize="xs" color="teal.500">Настроено</Text>
                </VStack>
              </HStack>
            </CardBody>
          </Card>
        </GridItem>
      </Grid>

      {/* Основные действия */}
      <Heading size="md" mt={4}>Быстрые действия</Heading>
      <Grid templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)' }} gap={6}>
        <GridItem>
          <Card bg={bgColor} h="100%">
            <CardBody>
              <VStack align="start" spacing={4}>
                <HStack spacing={3}>
                  <Icon as={FiActivity} w={5} h={5} color="teal.500" />
                  <Heading size="sm">Добавить измерение</Heading>
                </HStack>
                <Text fontSize="sm" color={textColor}>
                  Быстро введите результат последнего измерения пикфлоу
                </Text>
                <Button
                  as={Link}
                  to="/measurements/add"
                  colorScheme="teal"
                  variant="outline"
                  size="sm"
                  w="fit-content"
                >
                  Ввести результат
                </Button>
              </VStack>
            </CardBody>
          </Card>
        </GridItem>
        
        <GridItem>
          <Card bg={bgColor} h="100%">
            <CardBody>
              <VStack align="start" spacing={4}>
                <HStack spacing={3}>
                  <Icon as={FiBarChart2} w={5} h={5} color="blue.500" />
                  <Heading size="sm">Графики и статистика</Heading>
                </HStack>
                <Text fontSize="sm" color={textColor}>
                  Просмотрите историю измерений и динамику показателей
                </Text>
                <Button
                  as={Link}
                  to="/charts"
                  colorScheme="blue"
                  variant="outline"
                  size="sm"
                  w="fit-content"
                >
                  Открыть графики
                </Button>
              </VStack>
            </CardBody>
          </Card>
        </GridItem>
      </Grid>
      
      <Grid templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)' }} gap={6}>
        <GridItem>
          <Card bg={bgColor} h="100%">
            <CardBody>
              <VStack align="start" spacing={4}>
                <HStack spacing={3}>
                  <Icon as={FiUser} w={5} h={5} color="green.500" />
                  <Heading size="sm">Профиль ребенка</Heading>
                </HStack>
                <Text fontSize="sm" color={textColor}>
                  Просмотрите и обновите информацию о ребенке
                </Text>
                <Button
                  as={Link}
                  to="/child-profile"
                  colorScheme="green"
                  variant="outline"
                  size="sm"
                  w="fit-content"
                >
                  Открыть профиль
                </Button>
              </VStack>
            </CardBody>
          </Card>
        </GridItem>
        
        <GridItem>
          <Card bg={bgColor} h="100%">
            <CardBody>
              <VStack align="start" spacing={4}>
                <HStack spacing={3}>
                  <Icon as={FiBell} w={5} h={5} color="purple.500" />
                  <Heading size="sm">Напоминания</Heading>
                </HStack>
                <Text fontSize="sm" color={textColor}>
                  Настройте автоматические напоминания об измерениях
                </Text>
                <Button
                  as={Link}
                  to="/reminders"
                  colorScheme="purple"
                  variant="outline"
                  size="sm"
                  w="fit-content"
                >
                  Настроить напоминания
                </Button>
              </VStack>
            </CardBody>
          </Card>
        </GridItem>
      </Grid>
    </VStack>
  )
}

export default HomePage