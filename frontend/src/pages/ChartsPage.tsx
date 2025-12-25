import React from 'react'
import {
  Box,
  VStack,
  Heading,
} from '@chakra-ui/react'
import Charts from '../components/Charts'

const ChartsPage: React.FC = () => {
  return (
    <VStack spacing={6} align="stretch">
      <Heading size="lg">Графики и статистика</Heading>
      <Charts childId={1} />
    </VStack>
  )
}

export default ChartsPage