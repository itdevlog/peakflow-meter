import { extendTheme, type ThemeConfig } from '@chakra-ui/react'

// Определяем цвета для зон пикфлоу
const peakflowColors = {
  peakflow: {
    green: {
      50: '#f0f9f0',
      100: '#d1eacd',
      200: '#b3dcb0',
      300: '#84c784',
      400: '#55b355',
      500: '#26a026',
      600: '#1f801f',
      70: '#176017',
      800: '#0f400f',
      900: '#082008',
    },
    yellow: {
      50: '#fdf9f0',
      100: '#f9e9c1',
      200: '#f5d992',
      300: '#f0c963',
      40: '#ecb934',
      500: '#e8a905',
      600: '#ba8704',
      70: '#8c6503',
      800: '#5e4302',
      900: '#2f2101',
    },
    red: {
      50: '#fdf0f0',
      10: '#f9c1c1',
      200: '#f59292',
      300: '#f06363',
      400: '#ec3434',
      500: '#e80505',
      600: '#ba0404',
      700: '#8c0303',
      800: '#5e0202',
      900: '#2f0101',
    },
  },
}

const config: ThemeConfig = {
  initialColorMode: 'system',
  useSystemColorMode: false,
}

const theme = extendTheme({
  config,
  colors: {
    ...peakflowColors,
  },
  components: {
    Button: {
      baseStyle: {
        borderRadius: 'md',
      },
    },
    Input: {
      baseStyle: {
        field: {
          borderRadius: 'md',
        },
      },
    },
    Textarea: {
      baseStyle: {
        borderRadius: 'md',
      },
    },
    Card: {
      baseStyle: {
        container: {
          borderRadius: 'lg',
          boxShadow: 'md',
        },
      },
    },
  },
})

export default theme