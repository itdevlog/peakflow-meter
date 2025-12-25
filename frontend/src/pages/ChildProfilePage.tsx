import React from 'react'
import {
  Box,
  VStack,
  Heading,
} from '@chakra-ui/react'
import ChildProfileForm from '../components/ChildProfileForm'

const ChildProfilePage: React.FC = () => {
  return (
    <VStack spacing={6} align="stretch">
      <Heading size="lg">Профиль ребенка</Heading>
      <ChildProfileForm childId={1} />
    </VStack>
  )
}

export default ChildProfilePage