import React, { useState } from 'react'
import {
  Box,
  VStack,
  Heading,
  Button,
  HStack,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
} from '@chakra-ui/react'
import { FiPlus } from 'react-icons/fi'
import ReminderForm from '../components/ReminderForm'
import RemindersList from '../components/RemindersList'

const RemindersPage: React.FC = () => {
  const { isOpen, onOpen, onClose } = useDisclosure()
  const [editingReminder, setEditingReminder] = useState<any>(null)

  const handleEdit = (reminder: any) => {
    setEditingReminder(reminder)
    onOpen()
  }

  const handleCreate = () => {
    setEditingReminder(null)
    onOpen()
  }

  const handleClose = () => {
    setEditingReminder(null)
    onClose()
 }

  return (
    <VStack spacing={6} align="stretch">
      <HStack justifyContent="space-between">
        <Heading size="lg">Напоминания</Heading>
        <Button leftIcon={<FiPlus />} colorScheme="teal" onClick={handleCreate}>
          Добавить напоминание
        </Button>
      </HStack>
      
      <RemindersList childId={1} onEdit={handleEdit} />
      
      <Modal isOpen={isOpen} onClose={handleClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>
            {editingReminder ? 'Редактировать напоминание' : 'Создать напоминание'}
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <ReminderForm 
              childId={1} 
              reminder={editingReminder || undefined} 
              onSuccess={handleClose} 
            />
          </ModalBody>
          <ModalFooter>
            {/* Кнопки будут в форме */}
          </ModalFooter>
        </ModalContent>
      </Modal>
    </VStack>
  )
}

export default RemindersPage