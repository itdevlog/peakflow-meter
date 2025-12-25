import React from 'react'
import {
  Box,
  VStack,
  Heading,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
} from '@chakra-ui/react'
import MeasurementForm from '../components/MeasurementForm'
import MeasurementsList from '../components/MeasurementsList'

const MeasurementsPage: React.FC = () => {
  return (
    <VStack spacing={6} align="stretch">
      <Heading size="lg">Измерения пикфлоу</Heading>
      
      <Tabs variant="enclosed">
        <TabList>
          <Tab>Добавить измерение</Tab>
          <Tab>История измерений</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <MeasurementForm childId={1} />
          </TabPanel>
          <TabPanel>
            <MeasurementsList childId={1} />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </VStack>
  )
}

export default MeasurementsPage